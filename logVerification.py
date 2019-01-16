'''
Created on May-02-2017

@author: Jayakumar M
'''

import subprocess

import threading
import time
import datetime
import re
from os import path
import os
from austonioLibraries import Search
import htmlReport
import pandas as pd

from austonioLibraries import serverOperation
from austonioLibraries import adbOperation

import Config
import runBP


FILTER_WIH_PID = True
logSearch = Search.logSearch()

class adbLogcat(threading.Thread):
    def __init__(self, mainlog, deviceId):
        threading.Thread.__init__(self)
        self._mainlog = mainlog
        self._deviceId = deviceId

    def run(self):
        clearCMD  = 'adb -s '+self._deviceId+' logcat -c'
        adbLogsCMD = 'adb -s '+self._deviceId+' logcat'
        subprocess.call(clearCMD, shell=True)
        self._process = subprocess.Popen(adbLogsCMD, stdout=self._mainlog)

    def stop(self):
        self._process.terminate()
        print 'Wait for logcat stopped...'
        time.sleep(1)


def shellPIPE(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out


def readFile(filename):
    try:
        with open(filename) as file:
            for line in file:
                return line
                break
    except IOError as e:
        print e


def writeFile(filename, str):
    file = open(filename,'w')
    file.write(str)
    file.close()

def get_date_time():
    """Return date_time"""
    dt_format = '%b %d %Y_%H-%M-%S'
    return datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)

def resultFolder(deviceId, osPlatform="Ubuntu"):

    date_time = get_date_time()
    deviceResult = deviceId+ "--" + date_time

    try:

        if osPlatform.lower() == "ubuntu":
            pathTo = os.getcwd()
            pathList = pathTo.split('/')
            del pathList[-1]

            pathTo = '/'.join(pathList) + '/Result/' + deviceResult + '/'
            reultpathTo = '/'.join(pathList) + '/Result/'

            if not os.path.exists(reultpathTo):
                os.mkdir(reultpathTo)
                os.chmod(reultpathTo, 0777)

            if not os.path.exists(pathTo):
                os.mkdir(pathTo)
                os.chmod(pathTo, 0777)

            return deviceResult, pathTo
        elif osPlatform.lower() == "windows":

            pathWin = os.getcwd()
            pathWinList = pathWin.split(os.sep)
            del pathWinList[-1]

            winPathTo = "\\".join(pathWinList) + "\\Result\\" + deviceResult + "\\"
            winResultPath = "\\".join(pathWinList) + "\\Result\\"

            if not os.path.exists(winResultPath):
                os.makedirs(winResultPath)

            if not os.path.exists(winPathTo):
                os.makedirs(winPathTo)

            return deviceResult, winPathTo

        else:

            raise Exception

    except:

        raise "Invalid OS Platform"


def keywordFilter(filename, pid):
    # keyword reference are ["OpenGLRenderer", "MALI", "IMGSRV", "ViewRootImpl", "View", "SurfaceFlinger"]
    LineContent = r'(\d+-\d+)\s+([\d\:\.]+)\s+(\d+)\s+(\d+)\s+\w\s+(\w*):(.*)'
    lineContentCompiled = re.compile(LineContent)

    # Load previous keywords
    keywordFilename = path.join(PATH_BASE, "keywrods.txt")
    keywordsInFile = readFile(keywordFilename)
    if keywordsInFile:
        print "Previous keyword list: " + keywordsInFile

    # Get current keywords
    keywords = raw_input('Please insert keyword separeted by space (Enter to use previous / * for all): ') or keywordsInFile
    if not (keywords == keywordsInFile):
        writeFile(keywordFilename, keywords)

    keepAll = False
    keywordList = keywords.split(" ")
    lower = lambda input: input.lower()
    keywordList = map(lower, keywordList)
    if "*" in keywordList:
        keepAll = True
    print keywordList

    # Filter file and output to another file
    filteredFilename = filename.split(".")[0] + "_filter.log"
    filteredFile = open(filteredFilename, 'w+')

    with open(filename) as file:
        for line in file:
            if FILTER_WIH_PID:
                # Drop line with incorrect pid
                m = lineContentCompiled.match(line)
                if m:
                    if pid != m.group(3):
                        continue
                else:
                    continue

            # Keep lines with correct pid
            if keepAll:
                filteredFile.write(line)
                continue

            # Keep line with specific keywords
            for currKeyword in keywordList:
                if line.lower().find(currKeyword.lower()) >= 0:
                    filteredFile.write(line)
                    break

    filteredFile.close()
    return filteredFilename


def getProcessId():
    out = shellPIPE("adb shell dumpsys activity top")
    topProcessFile = path.join(PATH_BASE, "top.txt")
    myFile = open(topProcessFile, 'w+')
    myFile.write(out)
    myFile.seek(0, 0);

    activity = ""
    pid = ""

    for eachLine in myFile:
      if "pid=" in eachLine:
          activity = eachLine.split(" ")[3].strip()
          pid = eachLine.split("pid=")[-1].strip()
          break
    myFile.close()

    print 'Handling Process <' + activity.split("/")[0] + '> & PID <'+ pid + '>...\n'
    return pid


def main():
    # Launch the asynchronous readers of the process' stdout.
    deviceId = str(raw_input("Enter Device ID (e.g:0123456789012345): "))
    osPlatform = str(raw_input("Enter OS Platform (e.g: Windows or Ubuntu): "))

    resultPath, PATH_BASE = resultFolder(deviceId, osPlatform)
    print resultPath
    filename = resultPath+"-adbLogs.log"
    mainFile = path.join(PATH_BASE, filename)
    print "Target Log Path: %s" % mainFile
    print PATH_BASE
    print resultPath

    userServerDataobj = serverOperation.serverOperation()
    serverDataLst = userServerDataobj.deleteUserDataByUserId(Config.SERVERUSERPROFILEID, Config.DATASERVERIP)
    if serverDataLst:
        pass
    else:
        sys.exit(0)

    # # print "Installing Austonio APKs..."
    # # instAPKObj = installAPK.installAPK()
    adbObj = adbOperation.adbOperation()
    # # #
    # # instAPKObj.installAustonioAPKs(deviceId,Config.APKPATH)
    # # #
    # # adbObj.rebootDevice(deviceId)
    # # # time.sleep(30)
    # #
    # time.sleep(20)
    #
    # print "Pushing Validation Config File..."
    #
    # adbObj.pushFileToDevice(deviceId,Config.MANGAMENTCONFIG, "/sdcard/Management/")
    # adbObj.pushFileToDevice(deviceId, Config.COMMUNICATIONCONFIG, "/sdcard/Communication/")
    # time.sleep(5)
    #
    # print "Installing Validation Apk..."
    #
    # adbObj.installAPK(deviceId,Config.VALIDATIONAPK, reInstall=True)
    # time.sleep(5)

    # print "Launching Validation Apk..."
    # validationActivity = "com.intel.ese.validation/.ValidationActivity"
    # adbObj.startActivity(deviceId,validationActivity)
    # time.sleep(15)

    # adbObj.rebootDevice(deviceId)
    # time.sleep(2)
    #
    mainlog = open(mainFile, 'w+')
    stdout_reader = adbLogcat(mainlog, deviceId)
    # thread1 = threading.Thread(target=stdout_reader.start())
    # thread2 = threading.Thread(target=repeatedTimer.RepeatedTimer, args = (10,hello,"hello"))
    #
    # # p = multiprocessing.Process(target=repeatedTimer.RepeatedTimer, args = (10,hello,"hello"))
    #
    # thread1.start()
    # # p.start()
    # thread2.start()
    #
    #     # thread2.join()
    # #
    stdout_reader.start()

    print 'Start logging...\n'
    raw_input('Press Enter key to Stop logging...')

    print 'Stopping logcat ...'
    stdout_reader.stop()
    mainlog.close()
    #
    # print "Uninstalling Validation Apk..."
    # validationPkgName = "com.intel.ese.validation"
    # adbObj.unInstallAPK(deviceId, validationPkgName)

    # mainFile = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_New\Result\FZAUS173500020--Nov 15 2017_11-34-13\FZAUS173500020--Nov 15 2017_11-34-13-adbLogs.log"
    # PATH_BASE ="C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_New\Result\FZAUS173500020--Nov 15 2017_11-34-13"

    filename = open(
        mainFile,
        'r').read()
    runBPObj = runBP.runBP()
    # runPOObj = runPO.runPO()
    serverDataLst = userServerDataobj.fetchValuebyUserId(Config.SERVERUSERPROFILEID, Config.DATASERVERIP, PATH_BASE)
    print serverDataLst
    MEDIVAL = []
    for j in Config.MEDICALDEVICES.keys():
        MEDIVAL.append(Config.MEDICALDEVICES[j])

    for i in range(len(Config.DEVICES)):
        runBPObj.executeBP(filename, serverDataLst, MEDIVAL[i], Config.DEFINITIONFILES[i], Config.DEVICES[i],PATH_BASE, i)

    ex1 = pd.read_excel(PATH_BASE + 'WeightResult.xlsx',
                        keep_default_na=True, na_values=[" "])

    ex2 = pd.read_excel(PATH_BASE + 'POResult.xlsx',
                        keep_default_na=True, na_values=[" "])

    ex3 = pd.read_excel(PATH_BASE + 'BPResult.xlsx',
                        keep_default_na=True, na_values=[" "])

    # val1 = pd.read_excel(PATH_BASE + 'WeightValResult.xlsx',
    #                     keep_default_na=True, na_values=[" "])
    #
    # val2 = pd.read_excel(PATH_BASE + 'BPValResult.xlsx',
    #                     keep_default_na=True, na_values=[" "])
    #
    # val3 = pd.read_excel(PATH_BASE + 'POValResult.xlsx',
    #                     keep_default_na=True, na_values=[" "])

    h = pd.concat([ex1, ex2, ex3])

    # valex = pd.concat([val1, val2, val3])

    # df1 = h.sort_values(by='FDA Timestamp', ascending=1)
    df4 = h.reindex_axis(ex1.columns, axis=1)
    df1 = df4.sort_values(by='RPM', ascending=1)
    writer = pd.ExcelWriter(PATH_BASE + 'FinalResult.xlsx',
                            engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Report', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Report']

    # Add a format. Light red fill with dark red text.
    format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})

    # Add a format. Green fill with dark green text.
    format2 = workbook.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})

    format3 = workbook.add_format({'align': 'center'})

    worksheet.set_column('A:A', 11)
    worksheet.set_column('B:B', 14)
    worksheet.set_column('C:C', 17)
    worksheet.set_column('D:D', 11)
    worksheet.set_column('E:E', 17)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 14)
    worksheet.set_column('H:H', 17)
    worksheet.set_column('I:I', 14)
    worksheet.set_column('J:J', 17)
    worksheet.set_column('K:K', 10)
    worksheet.set_column('L:L', 14)
    worksheet.set_column('M:M', 17)
    worksheet.set_column('N:N', 14)
    worksheet.set_column('O:O', 17)
    worksheet.set_column('P:P', 10)
    maxValues = str(9 + 2)
    col = 'A1:P' + maxValues
    worksheet.conditional_format(col, {'type': 'text',
                                       'criteria': 'containing',
                                       'value': 'Fail',
                                       'format': format1})

    worksheet.conditional_format(col, {'type': 'text',
                                       'criteria': 'containing',
                                       'value': 'Pass',
                                       'format': format2})

    writer.save()
    writer.close()

    # valdf = valex.reindex_axis(val1.columns, axis=1)
    # valdf1 = valdf.sort_values(by='RPM', ascending=1)
    # writer1 = pd.ExcelWriter(PATH_BASE + 'ValidationResult.xlsx',
    #                         engine='xlsxwriter')
    # valdf1.to_excel(writer1, sheet_name='Report', index=False)
    #
    # workbook1 = writer1.book
    # # worksheet1 = writer1.sheets['Report']
    #
    # # Add a format. Light red fill with dark red text.
    # format1 = workbook1.add_format({'bg_color': '#FFC7CE',
    #                                'font_color': '#9C0006'})
    #
    # # Add a format. Green fill with dark green text.
    # format2 = workbook1.add_format({'bg_color': '#C6EFCE',
    #                                'font_color': '#006100'})
    #
    # format3 = workbook1.add_format({'align': 'center'})
    #
    # writer1.save()
    # writer1.close()


    generateReport = htmlReport.htmlReport()
    finalResultPath = PATH_BASE + 'FinalResult.xlsx'
    # validationPath = PATH_BASE + 'ValidationResult.xlsx'
    generateReport.generateHTML(finalResultPath,  PATH_BASE)

    # print valex



if __name__ == '__main__':
    main()