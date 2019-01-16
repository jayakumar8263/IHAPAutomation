import argparse
import operator
from multiprocessing import Process, Queue
import numpy as np
import envoy
import time
import subprocess
import Search


def run_jobs(args):
    """Create several processes, start each one, and collect the results.
    """
    # deviceId = str(raw_input("Enter Device ID (e.g:0123456789012345): "))
    # timeout1 = int(raw_input("How many hours the script should run?: "))
    # timeout1 = timeout1 * 60 * 60
    # print "Enabling WIFI..."
    # wifiOn = "adb shell svc wifi enable"
    # envoy.run(wifiOn,timeout=1)
    queue01 = Queue()
    queue02 = Queue()
    adb_cmd = 'adb logcat -s AppManager_BTStateChangeReceiver, Synchronization'

    n = [1, 2, 3, 4, 5]
    process01 = Process(target=adbLog, args=(queue01, adb_cmd, 10))
    process02 = Process(target=btONOFF, args=(queue02, 10))

    process01.start()
    process02.start()

    process01.join()
    process02.join()


    print queue01.get()


    # print queue02.get()


def adbLog(queue, adb_cmd, timeout):
    r = envoy.run(adb_cmd, timeout=timeout)
    j = r.std_out
    queue.put(j)


def btONOFF(queue, sleepTime):
    btOff = "adb shell service call bluetooth_manager 8"
    btOn = "adb shell service call bluetooth_manager 6"
    btToggle = "ON"
    for i in range(sleepTime):
        print i
        queue.put(subprocess.Popen(btOn, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True))
        time.sleep(2)
        queue.put(subprocess.Popen(btOff, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True))
        time.sleep(2)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, )
    args = parser.parse_args()

    run_jobs(args)
    # logSearch = Search.logSearch()
    # btKeyword = ['AppManager_BTStateChangeReceiver', 'STATE_']
    # btONOFFValue = logSearch.keywordSearch(btLogPharsing, *btKeyword)

if __name__ == '__main__':

    main()