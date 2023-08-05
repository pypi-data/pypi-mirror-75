# pylint: disable=C0103,W1202

from __future__ import print_function
import time as _time
from exoedge.sources import ExoEdgeSource
from exoedge import logger
import psutil
import time
import datetime
import subprocess
import json
from re import search

SUCCESSFUL_READ = 0
ERR_FILE_NOT_FOUND = 1
ERR_EMPTY_FILE = 2

APPLICATION_NAME = "LinuxStats"

LOG = logger.getLogger(__name__)

try:
    from sys_info import thread
except ImportError:
    LOG.warning("Unable to import thread. Please install in order to use the sys_info ExoEdge source.")


class LinuxstatsExoEdgeSource(ExoEdgeSource):
    def prune_interfaces(self, string, interface_name_location, line_num):
        LOG.critical("Pruning: \n" + string)
        mylist = string.splitlines()
        length = len(mylist)

        return_obj = {}
        values = []

        headers = []
        headers.append("Interface")
        headers.append("Address")
        return_obj["headers"] = headers

        for i in range(length):
            # Indented all the way left is the interface name, metadata has whitespace first
            if (search("^(?! )", mylist[i]) and len(mylist[i]) > 0):
                value = []
                interface = mylist[i].split(' ')[interface_name_location]
                try:
                    ip_address = search("(?<=inet )[^ ]*", mylist[i+line_num]).group(0)
                except AttributeError:
                    ip_address = "address not found"
                value.append(interface)
                value.append(ip_address)
                values.append(value)

        return_obj["values"] = values
        return return_obj

    def run(self):
        while not self.is_stopped():
            while not self._Q_DATA_OUT.empty():
                obj = self._Q_DATA_OUT.safe_get(timeout=0.1)
                if obj:
                    LOG.critical(
                         "Processing data_out on channel {} with value {}".format(obj.channel, obj.data_out_value)
                    )

                    # thread = Thread(target = self.handle_data_out, args=(obj,))
                    # thread.start()

            for channel in self.get_channels_by_application(APPLICATION_NAME):
                if channel.is_sample_time():
                    LOG.warning("sample_time for: {}" .format(channel.name))
                    function = channel.protocol_config.app_specific_config['function']

                    if (function == "cpu"):
                        channel.put_sample(psutil.cpu_percent())
                    elif (function == "mem"):
                        channel.put_sample(dict(psutil.virtual_memory()._asdict())['percent'])
                    elif (function == "mem_full"):
                        channel.put_sample(psutil.virtual_memory())
                    elif (function == "time"):
                        channel.put_sample(time.strftime("%H:%M:%S"))
                    elif (function == "datetime"):
                        output = datetime.datetime.now()
                        channel.put_sample(output)
                    elif (function == "interfaces"):
                        pruned = {}
                        try:
                            output = subprocess.run(['/sbin/ifconfig'], stdout=subprocess.PIPE).stdout.decode('UTF-8').replace("\n", "\r\n")
                            LOG.critical("ifconfig done")
                            ip_on_next_line = 1
                            name_is_first = 0
                            pruned = json.dumps(self.prune_interfaces(output, name_is_first, ip_on_next_line))
                        except:
                            try:
                                output = subprocess.run(["ip a"], shell=True, stdout=subprocess.PIPE).stdout.decode('UTF-8').replace("\n", "\r\n")
                                LOG.critical("ip a done")
                                LOG.critical(output)
                                ip_on_second_line = 2
                                name_is_second = 1 # 1: eth0 xyz
                                pruned = json.dumps(self.prune_interfaces(output, name_is_second, ip_on_second_line))
                                LOG.critical("DONE")
                            except Exception as inst:
                                print(inst)

                        channel.put_sample(pruned)

            _time.sleep(0.1)

        LOG.critical("ExoLinuxStats EXITING!")

#    Add logic to handle data_out if implemented
#    def handle_data_out(self, data_out_obj):
