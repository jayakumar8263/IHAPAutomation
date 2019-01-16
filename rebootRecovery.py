'''
Created on Oct-16-2017


@author: Jayakumar M
'''

import subprocess
import time
import os
import sys
from subprocess import Popen, PIPE, STDOUT


class adbOperation(object):
    def __init__(self):
        pass

    def checkDeviceConnection(self, deviceId, deviceMode="none"):

        adb_cmd = "adb devices"
        output = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout, stderr = output.communicate()

        stdout = '\n'.join([x for x in stdout.split("\n") if x.strip() != ''])

        stdout = stdout.split()

        if len(stdout) == 6:
            if stdout[4] == deviceId and stdout[5] == "device" and deviceMode == "normal":

                print stdout[4], "Device is Connected"
                return True
            elif stdout[4] == deviceId and stdout[5] == "offline":
                print "Device is offline"
                return False
            elif stdout[4] == deviceId and stdout[5] == "recovery" and deviceMode == "recovery":
                print "Device in Recovery"
                return True
            else:
                print "Error Connecting the device"
                return False
        else:
            print "Device is not connected"
            return False

    def rebootDeviceRecovery(self, deviceId):

        adb_cmd = "adb -s " + deviceId + " shell"
        DEVNULL = open(os.devnull, 'wb')
        proc = Popen(['adb', 'shell'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        proc.stdin.write('reboot recovery' + "\n")

        # subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print 'Waiting for the device (' + deviceId + ') to reboot...'
        time.sleep(30)

        if self.checkDeviceConnection(deviceId, deviceMode="recovery"):
            print deviceId, " Device Rebooted to recovery"
            time.sleep(20)
            return True
        else:
            print deviceId, " Device reboot recovery unsuccessful"
            return False

    def rebootDevice(self, deviceId):

        adb_cmd = "adb -s " + deviceId + " reboot"
        subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print 'Waiting for the device (' + deviceId + ') to reboot...'
        time.sleep(50)

        if self.checkDeviceConnection(deviceId, deviceMode="normal"):
            print deviceId, " Device Rebooted successfully"
            time.sleep(20)
            return True
        else:
            print deviceId, " Device reboot unsuccessful"
            return False


def deviceReboot():
    deviceId = str(raw_input("Enter device ID: "))
    adbObj = adbOperation()
    i = 1
    try:
        while True:
            print "--------------------------------------------------------"
            print "Reboot Count: ", i
            print "--------------------------------------------------------"
            adbResult = adbObj.checkDeviceConnection(deviceId, deviceMode="normal")
            if adbResult:
                time.sleep(2)
                adbObj.rebootDeviceRecovery(deviceId)
                time.sleep(2)
                adbObj.rebootDevice(deviceId)
                i = i + 1

    except KeyboardInterrupt:
        sys.exit()


deviceReboot()