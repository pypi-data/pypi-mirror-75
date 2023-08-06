#pylint: disable=C0103,W1202

from __future__ import print_function
import time as _time
import sys
from exoedge.sources import ExoEdgeSource
from exoedge import logger
from threading import Thread, Lock
from pycomm3 import LogixDriver
import os
import time
import subprocess
import threading

SUCCESSFUL_READ = 0
ERR_FILE_NOT_FOUND = 1
ERR_EMPTY_FILE = 2

APPLICATION_NAME = "EtherNetIP"

LOG = logger.getLogger(__name__)

try:
    from sys_info import *
except ImportError:
    LOG.warning("Unable to import psutil. Please install in order to use the sys_info ExoEdge source.")

socket_mutex = Lock()

class EthernetipExoEdgeSource(ExoEdgeSource):
    def run(self):
        LOG.setLevel("DEBUG")
        while not self.is_stopped():
            while not self._Q_DATA_OUT.empty():
                obj = self._Q_DATA_OUT.safe_get(timeout=0.1)
                if obj:
                    LOG.critical(
                         "Processing data_out on channel {} with value {}"
                        .format(obj.channel, obj.data_out_value)
                    )

                    thread = Thread(target = self.handle_data_out, args=(obj,))
                    thread.start()

            for channel in self.get_channels_by_application(APPLICATION_NAME):
                if channel.is_sample_time():
                    self.handle_data_in(channel)

            _time.sleep(0.1)

        LOG.critical("ExoEtherNetIP EXITING!")

    def handle_data_in(self, channel):
        socket_mutex.acquire()
        LOG.warning("sample_time for: {}" .format(channel.name))
        path = channel.protocol_config.app_specific_config['path']
        tag = channel.protocol_config.app_specific_config['tag']

        try:
            with LogixDriver(path) as plc:
                    reading = plc.read(tag)
                    if reading.error == None:
                        channel.put_sample(reading.value)
                    else:
                        channel.put_channel_error(reading.error)
        except:
            channel.put_channel_error(sys.exc_info()[0])

        socket_mutex.release()

#    Add logic to handle data_out if implemented
    def handle_data_out(self, data_out_obj):
        LOG.critical(
            "Processing modbus data out: {}({}): {}"
            .format(
                channel.name,
                channel.eval_kwargs['data_address'],
                data_out_obj.data_out_value)
        )

        path = data_out_obj.channel.protocol_config.app_specific_config['path']
        tag = data_out_obj.channel.protocol_config.app_specific_config['tag']

        with LogixDriver(path) as plc:
            reading = plc.write((tag, data_out_obj.data_out_value))

            reading = plc.read(tag)
            if reading.error == None:
                channel.put_sample(reading.value)
            else:
                channel.put_channel_error(reading.error)
