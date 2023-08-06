from tinydb import TinyDB, Query
from typing import List, Dict
from threading import RLock
from .singleton import SingletonMeta
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

    def insert_host(self, info: 'vrmjobs.HostInfo') -> bool:
        """
        Insert a new host into db
        :param info: an instance of HostInfo
        :return: True if success, False otherwise
        """
        with self.lock:
            success = False
            try:
                worker = self.get_host_by_hostname(info.hostname)

                if not worker:
                    ports = []
                    for p in info.ports:
                        ports.append({"daemon": p.daemon, "port": p.port})

                    self.table.insert({"hostname": info.hostname,
                                       "inet_addr": info.inet_addr,
                                       "ports": ports,
                                       "type": info.type.name})
                    success = True
            except Exception as ex:
                print(ex)
                return success
            finally:
                return success

    def get_host_by_hostname(self, hostname: str) -> vrmjobs.HostInfo:
        """
        Get info of a host by its hostname
        :param hostname: hostname of a worker/controller/monitor
        :return: hostname
        """
        with self.lock:
            try:
                Host = Query()
                record = self.table.search(Host.hostname == hostname)[0]

                if not record:
                    return None

                port_infos = []
                for info in record["ports"]:
                    port_infos.append(vrmjobs.PortInfo(info["daemon"], info["port"]))

                return vrmjobs.HostInfo(record["hostname"],
                                        record["inet_addr"],
                                        port_infos,
                                        # https://stackoverflow.com/questions/41407414/convert-string-to-enum-in-python
                                        vrmjobs.HostType.__dict__[record["type"]])
            except Exception as ex:
                print(ex)
                return None

    def get_daemon_by_name(self, hostname: str, daemon: str) -> vrmjobs.PortInfo:
        """
        Get daemon information of a worker/collector/monitor by its hostname
        :param hostname: hostname of a host
        :param daemon: name of daemon
        :return: an instance of PortInfo
        """
        with self.lock:
            try:
                Host = Query()
                record = self.table.search(Host.hostname == hostname)[0]

                if not record:
                    return None

                for info in record["ports"]:
                    if info["daemon"] == daemon:
                        return vrmjobs.PortInfo(info["daemon"],
                                                info["port"])

                return None
            except Exception:
                return None

    def update_host_metrics(self, hostname, metrics: List[Dict]) -> bool:
        """
        Update metrics information of a worker of a certain hostname
        :param hostname: hostname of host
        :param metrics: list of PortInfo
        :return: True if succeed, False otherwise
        """
        with self.lock:
            try:
                Host = Query()
                self.table.upsert({'metrics': metrics},
                                  Host.hostname.matches(hostname))

                return True
            except Exception:
                return False