#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
#

from talos.consumer.MessageProcessor import MessageProcessor
from talos.consumer.SimpleConsumer import SimpleConsumer
from talos.thrift.topic.ttypes import TopicAndPartition
from talos.thrift.message.ttypes import MessageOffset
from talos.client.TalosClientFactory import ConsumerClient
from talos.client.TalosClientConfig import TalosClientConfig
from atomic import AtomicLong
from talos.utils import Utils
import traceback
import logging
import abc
import time


class MessageReader:
    logger = logging.getLogger("MessageReader")
    commitThreshold = int
    commitInterval = int
    fetchInterval = int

    lastCommitTime = int
    lastFetchTime = int

    startOffset = AtomicLong
    finishedOffset = int
    lastCommitOffset = int
    messageProcessor = MessageProcessor

    workerId = str
    consumerGroup = str
    topicAndPartition = TopicAndPartition
    consumerConfig = TalosClientConfig
    simpleConsumer = SimpleConsumer
    consumerClient = ConsumerClient

    # outer - checkPoint can be used only one time, burn after reading to prevent
    # partitionFetcher re - lock() and re - use outer - checkPoint again by consumer re - balance
    outerCheckPoint = int

    def __init__(self, consumerConfig=None):
        self.consumerConfig = consumerConfig
        self.lastCommitOffset = self.finishedOffset = -1
        self.lastCommitTime = self.lastFetchTime = Utils.current_time_mills()
        self.startOffset = AtomicLong(-1)
        if consumerConfig:
            self.commitThreshold = consumerConfig.get_commit_offset_threshold()
            self.commitInterval = consumerConfig.get_commit_offset_interval()
            self.fetchInterval = consumerConfig.get_fetch_message_interval()
        self.outerCheckPoint = None

    def set_worker_id(self, workerId=None):
        self.workerId = workerId

    def set_consumer_group(self, consumerGroup=None):
        self.consumerGroup = consumerGroup

    def set_topic_and_partition(self, topicAndPartition=None):
        self.topicAndPartition = topicAndPartition

    def set_simple_consumer(self, simpleConsumer=None):
        self.simpleConsumer = simpleConsumer

    def set_message_processor(self, messageProcessor=None):
        self.messageProcessor = messageProcessor

    def set_consumer_client(self, consumerClient=None):
        self.consumerClient = consumerClient

    def set_outer_checkpoint(self, outerCheckpoint=None):
        self.outerCheckPoint = outerCheckpoint

    def get_start_offset(self):
        return self.startOffset.value

    def get_cur_checkpoint(self):
        # init state or before the first committing
        if self.lastCommitOffset <= self.startOffset.value:
            return self.startOffset.value

        # from lastCommitOffset + 1 when reading next time
        return self.lastCommitOffset + 1

    def should_commit(self, isContinuous=None):
        interval = Utils.current_time_mills() - self.lastCommitTime
        if isContinuous:
            return interval >= self.commitInterval or self.finishedOffset - self.lastCommitOffset >= self.commitThreshold
        else:
            return interval >= self.commitInterval and self.finishedOffset - self.lastCommitOffset >= self.commitThreshold

    def clean_reader(self):
        # wait task quit gracefully: stop reading, commit offset, clean and shutdown
        if self.finishedOffset > self.lastCommitOffset:
            try:
                self.commit_check_point()
            except Exception as e:
                self.logger.error("Error when commit offset for topic: " +
                                  str(self.topicAndPartition.topicTalosResourceName) +
                                  " partition: " + str(self.topicAndPartition.partitionId)
                                  + str(traceback.format_exc()))

    def process_fetch_exception(self, e=None):
        # delay when partitionNotServing
        if Utils.is_partition_not_serving(e):
            self.logger.warn("Partition: " + str(self.topicAndPartition.partitionId) +
                             " is not serving state, sleep a while for waiting it work."
                             + str(traceback.format_exc()))
            time.sleep(self.consumerConfig.get_wait_partition_working_time())

        # if process message offset out of range, reset start offset
        if Utils.is_offset_out_of_range(e):
            if self.consumerConfig.is_reset_latest_offset_out_of_range():
                self.logger.warn("Got PartitionOutOfRange error, " +
                                 " offset by current latest offset"
                                 + str(traceback.format_exc()))
                self.startOffset.get_and_set(MessageOffset.LATEST_OFFSET)
                self.lastCommitOffset = self.finishedOffset = - 1
                self.lastCommitTime = Utils.current_time_mills()
            else:
                self.logger.warn("Got PartitionOutOfRange error," +
                                 " reset offset by current start offset"
                                 + str(traceback.format_exc()))
                self.startOffset.get_and_set(MessageOffset.START_OFFSET)
                self.lastCommitOffset = self.finishedOffset = - 1
                self.lastCommitTime = Utils.current_time_mills()

        self.logger.warn("process unexcepted fetchException:" + str(traceback.format_exc()))

    #
    # query start offset to read, if failed, throw the exception
    #
    @abc.abstractmethod
    def init_start_offset(self):
        pass

    #
    # commit the last processed offset and update the startOffset
    # throw the Exception when appear error
    #
    @abc.abstractmethod
    def commit_check_point(self):
        pass

    #
    # you should implement this method as follow process:
    # 1.control fetch qps by fetchInterval
    # 2.fetchMessage with try / catch structure and process exception
    # 2.1 catch chunk process PARTITION_NOT_SERVING by sleep a while
    # 2.2 catch chunk process MESSAGE_OFFSET_OUT_OF_RANGE by fixOffsetOutofRange()
    # 2.3 reset lastFetchTime
    # 3.process fetched message by MessageProcessor and update finishedOffset / startOffset
    # 4.check whether should commit offset
    #
    @abc.abstractmethod
    def fetch_data(self):
        pass

