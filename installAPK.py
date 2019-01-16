'''


@author: Jayakumar M
'''

import glob
from austonioLibraries import adbOperation
import time
from Constants import Config
class installAPK(object):

    def __init__(self):

        pass

    def installAustonioAPKs(self, deviceId, apkPath):

        activityNames = ['com.intel.austonio.appmanager/com.intel.austonio.appmanager.MainActivity', 'com.intel.bluetoothheadless/com.intel.austonio.bluetoothheadless.MainActivity',
                         'com.intel.austonio.communication/com.intel.austonio.communication.MainActivity',
                         'com.intel.austonio.display/com.intel.austonio.display.MainActivity',
                         'com.intel.austonio.hdo/com.intel.austonio.hdo.MainActivity',
                         'com.intel.austonio.rpm/com.intel.austonio.rpm.MainActivity',
                         'com.windriver.heartfield/com.windriver.heartfield.HeartfieldSettings',
                         'com.windriver.healthsampleui/com.windriver.healthsampleui.HealthUISample',
                         'com.windriver.healthui/com.windriver.healthui.frontend.LoginScreen',
                         'com.intel.austonio.management/com.intel.austonio.management.MainActivity'
                         ]

        adbObj = adbOperation.adbOperation()




        apkList = glob.glob(apkPath+"\*.apk")
        print apkList

        # for i in apkList:
        #     adbObj.installAPK(deviceId, i, True)

        adbObj.pushFileToDevice(deviceId, Config.COMMUNICATIONCONFIG, "/sdcard/")
        time.sleep(5)

        adbObj.pushFileToDevice(deviceId, Config.MANGAMENTCONFIG, "/sdcard/")
        time.sleep(5)

        # for j in activityNames:
        #     adbObj.startActivity(deviceId,j)



