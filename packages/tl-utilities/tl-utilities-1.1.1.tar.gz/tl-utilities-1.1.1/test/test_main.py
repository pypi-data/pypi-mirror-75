from utilities import *
import vrmjobs
from datetime import datetime


def test_check_heartbeat(db_manager: 'TinyDbWrapper', hostname: str, interval: int):
    try:
        result = db_manager.check_heartbeat(hostname, datetime.now(), interval)

        if result:
            print("Still good.")
        else:
            print("Need to update.")
    except HeartbeatError as err:
        print(err)


def test_update_heartbeat(db_manager: 'TinyDbWrapper', hostname: str):
    try:
        db_manager.update_host_heartbeat(hostname)
        host = db_manager.get_host_by_hostname(hostname)
        print("Latest info: {}".format(host))
    except UpdateError as err:
        print(err)


def test_get_host(db_manager: 'TinyDbWrapper', hostname: str):
    try:
        host = db_manager.get_host_by_hostname(hostname)
        print(host)
    except GetError as err:
        print(err)


def test_insert_hosts(db_manager: 'TinyDbWrapper', hostname: str, inet_addr:str,
                      ports: ['vrmjobs.PortInfo'], hosttype: 'vrmjobs.HostType'):
    try:
        host = vrmjobs.HostInfo(hostname, inet_addr, ports, hosttype)
        result = db_manager.insert_host(host)
        if result:
            print("Insert {} to db successfully.".format(host))

    except InsertError as err:
        print(err)


def main():
    # create db
    db = TinyDbWrapper('test_db.json')

    # insert a new host (if possible)
    #test_insert_hosts(db, 'worker1', '192.168.1.11', [vrmjobs.PortInfo('workerd', 10300),
    #                            vrmjobs.PortInfo('builderd', 5000)], vrmjobs.HostType.WORKER)

    #test_insert_hosts(db, 'worker2', '192.168.1.12', [vrmjobs.PortInfo('workerd', 10300),
    #                                                  vrmjobs.PortInfo('builderd', 5000)], vrmjobs.HostType.WORKER)

    #test_get_host(db, 'worker1')
    #test_get_host(db, 'worker3')
    #test_update_heartbeat(db, 'worker1')
    #test_update_heartbeat(db, 'worker2')
    test_check_heartbeat(db, 'worker1', 3600)


if __name__ == '__main__':
    main()
