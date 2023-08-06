from tinydb import TinyDB, Query
from typing import List, Dict
from threading import RLock
from datetime import datetime
from .singleton import SingletonMeta
from .tinydb_exceptions import *
import vrmjobs


class TinyDbWrapper(metaclass=SingletonMeta):
    """
    Wrapper class for TinyDB within VRM system
    """
    def __init__(self, db_path: str) -> None:
        # create db
        self.db = TinyDB(db_path, sort_keys=True, indent=2, separators=(',', ': '))
        # create worker table
        self.table = self.db.table('hosts')
        # create lock
        self.lock = RLock()
        # create timing-format
        self.time_format = '%H:%M:%S %d-%m-%Y'

    def insert_host(self, info: 'vrmjobs.HostInfo') -> bool:
        """
        Insert a new host into db
        :param info: an instance of HostInfo
        :return: True if success, False otherwise
        """
        with self.lock:
            try:
                host = self._check_host_existence(info.hostname)

                if not host:
                    ports = []
                    for p in info.ports:
                        ports.append({"daemon": p.daemon, "port": p.port})

                    self.table.insert({"hostname": info.hostname,
                                       "inet_addr": info.inet_addr,
                                       "ports": ports,
                                       "type": info.type.name,
                                       "latest_recv": datetime.now().strftime(self.time_format)})
                    return True
                return False
            except Exception as err:
                raise InsertError('Cannot insert new host {}'.format(str(info)), err)

    def _check_host_existence(self, hostname: str) -> bool:
        """
        Check whether a host with certain hostname is already included
        :param hostname: hostname of the host need to check
        :return: True if included, False otherwise
        """
        with self.lock:
            hosts = self.table.all()
            for host in hosts:
                if host['hostname'] == hostname:
                    return True
            return False

    def get_host_by_hostname(self, hostname: str) -> vrmjobs.HostInfo:
        """
        Get info of a host by its hostname
        :param hostname: hostname of a worker/controller/monitor
        :return: HostInfo instance
        """
        with self.lock:
            try:
                host = Query()
                record = self.table.search(host.hostname == hostname)

                if record:
                    port_infos = []
                    for info in record[0]["ports"]:
                        port_infos.append(vrmjobs.PortInfo(info["daemon"], info["port"]))

                    return vrmjobs.HostInfo(record[0]["hostname"],
                                            record[0]["inet_addr"],
                                            port_infos,
                                            # https://stackoverflow.com/questions/41407414/convert-string-to-enum-in-python
                                            vrmjobs.HostType.__dict__[record[0]["type"]])
                else:
                    raise Exception('Not found.')
            except Exception as err:
                raise GetError('Cannot find host by hostname={}'.format(hostname), err)

    def get_daemon_by_name(self, hostname: str, daemon: str) -> vrmjobs.PortInfo:
        """
        Get daemon information of a worker/collector/monitor by its hostname
        :param hostname: hostname of a host
        :param daemon: name of daemon
        :return: an instance of PortInfo
        """
        with self.lock:
            try:
                host = Query()
                record = self.table.search(host.hostname == hostname)[0]

                if not record:
                    return None

                for info in record["ports"]:
                    if info["daemon"] == daemon:
                        return vrmjobs.PortInfo(info["daemon"],
                                                info["port"])

                return None
            except Exception as err:
                raise GetError('Cannot get daemon name={} of host with hostname={}'.format(daemon, hostname), err)

    def update_host_metrics(self, hostname, metrics: List[Dict]) -> bool:
        """
        Update metrics information of a host with a certain hostname
        :param hostname: hostname of host
        :param metrics: list of PortInfo
        :return: True if succeed, False otherwise
        """
        with self.lock:
            try:
                host = Query()
                self.table.upsert({'metrics': metrics},
                                  host.hostname.matches(hostname))

                return True
            except Exception as err:
                raise UpdateError('Cannot update metrics: {} of host with hostname={}'.format(metrics, hostname), err)

    def update_host_heartbeat(self, hostname: str) -> bool:
        """
        Update latest_update information of a host with a certain hostname
        :param hostname: hostname of host
        :return: True if success, UpdateError otherwise
        """
        with self.lock:
            try:
                host = Query()
                self.table.update({'latest_recv': datetime.now().strftime(self.time_format)},
                                  host.hostname.matches(hostname))
                return True
            except Exception as err:
                raise UpdateError('Cannot update latest_recv of host with hostname={}'.format(hostname), err)

    def check_heartbeat(self, hostname: str, current_time, max_interval: int) -> bool:
        """
        Check whether latest_update information of a host with a certain hostname is overdue
        :param hostname: hostname of host
        :param current_time: time of the moment of checking
        :param max_interval: maximum seconds allowed between check
        :return:
        """
        with self.lock:
            try:
                host = Query()
                record = self.table.search(host.hostname == hostname)[0]

                if record:
                    latest_update = datetime.strptime(record['latest_recv'], self.time_format)
                    difference = current_time - latest_update

                    return difference.total_seconds() <= max_interval

            except Exception as err:
                raise HeartbeatError('Cannot check heartbeat of host with hostname={}'.format(hostname), err)
