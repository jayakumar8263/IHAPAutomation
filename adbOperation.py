'''
Created on May-10-2017

@author: Jayakumar M
'''

import subprocess
import time
import os

class adbOperation(object):

    def __init__(self):
        pass


    def checkDeviceConnection(self, deviceId):

        adb_cmd = "adb devices"
        output = subprocess.Popen(adb_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell = True)
        stdout, stderr = output.communicate()


        stdout = '\n'.join([x for x in stdout.split("\n") if x.strip() != ''])

        stdout = stdout.split()

        if len(stdout) == 6:
            if stdout[4] == deviceId and stdout[5] == "device":

                print stdout[4], "Device is Connected"
                return True
            elif stdout[4] == deviceId and stdout[5] == "offline":
                print "Device is offline"
                return False
            else:
                print "Error Connecting the device"
                return False
        else:
            print "Device is not connected"
            return False

    def rebootDevice(self,deviceId):

        adb_cmd = "adb -s "+deviceId+" reboot"
        subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print 'Waiting for the device (' + deviceId + ') to reboot...'
        time.sleep(50)

        if self.checkDeviceConnection(deviceId):
            print deviceId, " Device Rebooted successfully"
            return True
        else:
            print deviceId," Device reboot unsuccessful"
            return False

    def pushFileToDevice(self, deviceId, filePath, deviceLocation):

        # print pathWin
        adb_cmd = 'adb -s '+deviceId+' push '+filePath+' '+deviceLocation
        output = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        time.sleep(2)
        stdout, stderr = output.communicate()

        # print stdout

        stdout1 = '\n'.join([x for x in stdout.split("\n") if x.strip() != ''])
        stdout1 = stdout1.split()

        if "pushed" in stdout1[-7] and stdout1[-9] > 0:
            print "File pushed successfully"
            print stdout
            return True

        else:
            print "File not pushed \n", " ".join(stdout1)
            return False

    def installAPK(self, deviceId, apkPath, reInstall = False):

        app_install = False

        if self.checkDeviceConnection(deviceId):
            #FNULL=open(os.devnull, "w")
            if reInstall:
                adb_cmd = "adb -s "+ deviceId + " install -r " + apkPath
            else:
                adb_cmd = "adb -s "+ deviceId + " install " + apkPath

            output = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            stdout, stderr = output.communicate()
            stdout = '\n'.join([x for x in stdout.split("\n") if x.strip() != ''])

            stdout = stdout.split()

            if "Success" in stdout:
                # app_install = True
                print "Application "+apkPath+" successfully installed in the device"
                return True
                # quit()
            else:
                app_install = False
                print "Application "+apkPath+" not installed on connected device, Check the device settings and restart the script"

        else:
            print "Device disconnected"
            return False

        if not app_install:
            return False

    def startActivity(self, deviceId, activityName):

        adb_cmd = "adb -s " + deviceId + " shell am start -n " + activityName  # com.intel.austonio.rpm/.MainActivity
        installOutput = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        for line in installOutput.stdout:
            print line

    def unInstallAPK(self,deviceId, pkgName):

        adb_cmd = "adb -s "+deviceId+" uninstall "+pkgName
        app_install = False


        # FNULL=open(os.devnull, "w")

        output = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout, stderr = output.communicate()
        stdout = '\n'.join([x for x in stdout.split("\n") if x.strip() != ''])

        stdout = stdout.split()

        if "Success" in stdout:
            # app_install = True
            print "Application successfully uninstalled in the device"
            return True
            # quit()
        else:
            app_install = False
            print "Application not uninstalled on connected device, Check the device settings and restart the script"

        if not app_install:
            return False



