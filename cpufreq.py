# coding=utf-8
'''
Created on Apr 20, 2017

@author: Jayakumar M
'''

import datetime, time, os, subprocess
import envoy
from operator import truediv
import pandas as pd
import shutil
import zipfile
import plotly.offline as offline


# from auslib import adbOperation

class cpuBenchmark(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def get_date_time(self):
        """Return date_time"""
        dt_format = '%Y%m%d_%H%M%S'
        return datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)

    def resultFolder(self, deviceId, osPlatform="Ubuntu"):

        date_time = self.get_date_time()
        deviceResult = deviceId + "_" + date_time

        try:

            if osPlatform.lower() == "ubuntu":

                pathTo = os.getcwd()
                pathList = pathTo.split('/')
                # del pathList[-1]

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
                # del pathWinList[-1]

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

    def checkDeviceConnection(self, deviceId):

        try:

            adb_cmd = "adb devices"
            output = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            stdout, stderr = output.communicate()

            # Removing the empty line from the result
            stdout = '\n'.join([x for x in stdout.split("\n") if x.strip() != ''])
            stdout = stdout.split()

            if len(stdout) == 6:
                if stdout[4] == deviceId and stdout[5] == "device":
                    print "Device is connected"
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

        except:
            raise "Error checking the device connection"

    def getResultFolder(self, osPlatform="ubuntu"):
        if osPlatform.lower() == "ubuntu":

            pathTo = os.getcwd()
            pathList = pathTo.split('/')
            del pathList[-1]

            reultpathTo = '/'.join(pathList) + '/Result/'
            return reultpathTo

        elif osPlatform.lower() == "windows":

            pathWin = os.getcwd()
            pathWinList = pathWin.split(os.sep)
            del pathWinList[-1]

            winResultPath = "\\".join(pathWinList) + "\\Result\\"
            return winResultPath
        else:
            print "Invalid Location"

    def moveFilesAndFolders(self, osPlatform):

        srcPath = self.getResultFolder(osPlatform)
        files = os.listdir(srcPath)
        files.sort()
        dest = srcPath.split('/')
        j = dest[:-2]
        dest1 = '/'.join(j)
        print dest1
        dest = dest1 + '/Backup/'
        print dest
        for f in files:
            src = srcPath + f
            dst = dest + f
            shutil.move(src, dst)

    def creatResultZip(self, osPlatform):
        path = self.getResultFolder(osPlatform)
        path = os.path.abspath(os.path.normpath(os.path.expanduser(path)))
        for folder in os.listdir(path):
            zipf = zipfile.ZipFile('{0}.zip'.format(os.path.join(path, folder)), 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(os.path.join(path, folder)):
                for filename in files:
                    zipf.write(os.path.abspath(os.path.join(root, filename)), arcname=filename)
            zipf.close()

    def cpuUsageInfo(self):

        # deviceId = str(raw_input("Enter Device ID (e.g:0123456789012345): "))
        # osPlatform = str(raw_input("Enter OS Platform (e.g: Windows or Ubuntu): "))
        # timeout1 = int(raw_input("How many hours the script should run?: "))
        # #timeout1 = timeout1 * 60* 60
        # delay = str(raw_input("How much sleep required on each Iteration?:"))
        # #         self.moveFilesAndFolders(osPlatform)
        # timeshell = str(timeout1/(60*60))
        # print 'Executing shell command for '+timeshell+' hour(s) with '+delay+' seconds delay.'
        # result, path = self.resultFolder(deviceId,osPlatform)
        # adb_logcat_file = open(path+ '/adb_logcat.txt', 'w')
        # #
        # #
        # #
        # # adb_cmd = 'adb -s '+deviceId+' shell "if true; then echo freq && cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq && echo battery && cat /sys/class/power_supply/battery/temp && echo temp && cat /sys/class/thermal/thermal_zone0/temp &&  echo time && echo \$EPOCHREALTIME && echo Voltage && cat /sys/class/power_supply/battery/voltage_now ; sleep 10; fi"'

        # # for i in range(timeout):
        # # output = subprocess.Popen(adb_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=False)

        # # time.sleep(0.5)
        # # for logcat_line in output.stdout:
        # # #print logcat_line
        # # adb_logcat_file.write(logcat_line + '\n')

        # # adb_logcat_file.close()
        # adb_cmd = 'adb -s '+deviceId+' shell "while true; do echo freq && cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq && echo temp && cat /sys/class/thermal/thermal_zone*/temp &&  echo time && echo $EPOCHREALTIME  ; sleep '+delay+'; done"'
        # print "Running cat Command : ", adb_cmd

        # r = envoy.run(adb_cmd, timeout=timeout1)

        # adb_logcat_file.write(r.std_out+ '\n')

        # adb_logcat_file.close()


        # path = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation\\austonioLibraries"
        rea = 'adb_logcat.txt'
        print rea
        print os.path.getsize(rea)

        #         lo = pathTo+'/adb_logcat.txt'

        os.chmod(rea, 0777)

        resultFileReader = open(rea, 'r+').read()
        l1 = resultFileReader.split("\n")
        l1 = [i.strip() for i in l1]
        l1 = list(filter(None, l1))
        #         print l1
        #         cpuList = l1[::11]
        #         cpuUsageLst = ' '.join(cpuList)
        #         cpuUsageLst = cpuUsageLst.split(" ")
        #
        #         cpuValue = [i for i, x in enumerate(cpuUsageLst) if x == "cpu"]
        #
        #         userValue = []
        #         systemValue = []
        #         idleValue = []
        #         for cpu in cpuValue:
        #             userValue.append(cpuUsageLst[cpu+2])
        #             systemValue.append(cpuUsageLst[cpu+4])
        #             idleValue.append(cpuUsageLst[cpu+5])
        #
        #         userValue = map(int, userValue)
        #         systemValue = map(int, systemValue)
        #         idleValue = map(int, idleValue)
        #         cpuUsage1 = map(sum,zip(userValue, systemValue))
        #         cpuUsage2 = map(sum,zip(userValue, systemValue, idleValue))
        #
        #         cpuUsageAvg = map(truediv, cpuUsage1, cpuUsage2)
        #         userAvg = map(truediv, userValue, cpuUsage2)
        #         systemAvg = map(truediv, systemValue, cpuUsage2)
        #
        #
        #         userperValue = [i*100 for i in userAvg]
        #         userformatperValue = [ '%.2f' % elem for elem in userperValue ]
        #         userformatperValue=[float(x) for x in userformatperValue]
        #         systemperValue = [i*100 for i in systemAvg]
        #         systemformatperValue = [ '%.2f' % elem for elem in systemperValue ]
        #         systemformatperValue=[float(x) for x in systemformatperValue]
        #         cpuUsageValue = [i*100 for i in cpuUsageAvg]
        #         cpuUsageformatValue = [ '%.2f' % elem for elem in cpuUsageValue ]
        #         cpuUsageformatValue=[float(x) for x in cpuUsageformatValue]
        #
        #
        freqIndex = [i for i, x in enumerate(l1) if x == "freq"]

        freqValue = []
        for freq in freqIndex:
            freqValue.append(l1[freq + 1])

        # print freqValue

        cpufreqinMhz = []
        for m in freqValue:
            cpufreqinMhz.append(float(m) / (1000))

        cpufreqinMhzformat = ['%.2f' % elem for elem in cpufreqinMhz]
        cpufreqinMhzformat = [float(x) for x in cpufreqinMhzformat]

        cpu1160Length = [i for i, x in enumerate(cpufreqinMhzformat) if x == 1160]

        cpufreqinMhzLength = len(cpufreqinMhzformat)
        cpu1160Length = len(cpu1160Length)
        cpu1160Averagelen = ((float(cpu1160Length) / cpufreqinMhzLength) * 100)
        cpu1160Average = str(round(cpu1160Averagelen, 2))

        cpu900Length = [i for i, x in enumerate(cpufreqinMhzformat) if x == 900]

        cpu900Length = len(cpu900Length)
        cpu900Averagelen = ((float(cpu900Length) / cpufreqinMhzLength) * 100)
        cpu900Average = str(round(cpu900Averagelen, 2))

        cpu728Length = [i for i, x in enumerate(cpufreqinMhzformat) if x == 728]

        cpu728Length = len(cpu728Length)
        cpu728Averagelen = ((float(cpu728Length) / cpufreqinMhzLength) * 100)
        cpu728Average = str(round(cpu728Averagelen, 2))

        cpu416Length = [i for i, x in enumerate(cpufreqinMhzformat) if x == 416]

        cpu416Length = len(cpu416Length)
        cpu416Averagelen = ((float(cpu416Length) / cpufreqinMhzLength) * 100)
        cpu416Average = str(round(cpu416Averagelen, 2))

        # batteryIndex = [i for i, x in enumerate(l1) if x == "battery"]
        # batteryValue = []
        # for bat in batteryIndex:
        # batteryValue.append(l1[bat+1])
        # #
        # batteryTemp = []
        # for b in batteryValue:
        # batteryTemp.append(float(b)/10.0)
        # batteryTempformat = [ '%.2f' % elem for elem in batteryTemp ]
        # batteryTempformat=[float(x) for x in batteryTempformat]

        # batteryAverage = str(round(reduce(lambda x, y: x + y, batteryTempformat) / len(batteryTempformat),2))

        tempIndex = [i for i, x in enumerate(l1) if x == "temp"]
        tempValue1 = []
        tempValue2 = []
        tempValue3 = []
        tempValue4 = []
        tempValue5 = []
        tempValue6 = []
        tempValue7 = []
        tempValue8 = []

        for tem in tempIndex:
            tempValue1.append(l1[tem + 1])
            tempValue2.append(l1[tem + 2])
            tempValue3.append(l1[tem + 3])
            tempValue4.append(l1[tem + 4])
            tempValue5.append(l1[tem + 5])
            tempValue6.append(l1[tem + 6])
            tempValue7.append(l1[tem + 7])
            tempValue8.append(l1[tem + 8])


        cpuTemp1 = []
        cpuTemp2 = []
        cpuTemp3 = []
        cpuTemp4 = []
        cpuTemp5 = []
        cpuTemp6 = []
        cpuTemp7 = []
        cpuTemp8 = []
        for cputemp in tempValue1:
            cpuTemp1.append(float(cputemp) / 1000.00)
        for cputemp in tempValue2:
            cpuTemp2.append(float(cputemp) / 1000.00)
        for cputemp in tempValue3:
            cpuTemp3.append(float(cputemp) / 1000.00)
        for cputemp in tempValue4:
            cpuTemp4.append(float(cputemp) / 1000.00)
        for cputemp in tempValue5:
            cpuTemp5.append(float(cputemp) / 1000.00)
        for cputemp in tempValue6:
            cpuTemp6.append(float(cputemp) / 1000.00)
        for cputemp in tempValue7:
            cpuTemp7.append(float(cputemp) / 1000.00)
        for cputemp in tempValue8:
            cpuTemp8.append(float(cputemp) / 1000.00)

        cpuTempformat1 = ['%.2f' % elem for elem in cpuTemp1]
        cpuTempformat2 = ['%.2f' % elem for elem in cpuTemp2]
        cpuTempformat3 = ['%.2f' % elem for elem in cpuTemp3]
        cpuTempformat4 = ['%.2f' % elem for elem in cpuTemp4]
        cpuTempformat5 = ['%.2f' % elem for elem in cpuTemp5]
        cpuTempformat6 = ['%.2f' % elem for elem in cpuTemp6]
        cpuTempformat7 = ['%.2f' % elem for elem in cpuTemp7]
        cpuTempformat8 = ['%.2f' % elem for elem in cpuTemp8]

        cpuTempformat1 = [float(x) for x in cpuTempformat1]
        cpuTempformat2 = [float(x) for x in cpuTempformat2]
        cpuTempformat3 = [float(x) for x in cpuTempformat3]
        cpuTempformat4 = [float(x) for x in cpuTempformat4]
        cpuTempformat5 = [float(x) for x in cpuTempformat5]
        cpuTempformat6 = [float(x) for x in cpuTempformat6]
        cpuTempformat7 = [float(x) for x in cpuTempformat7]
        cpuTempformat8 = [float(x) for x in cpuTempformat8]

        cpuTempAverage1 = str(round(reduce(lambda x, y: x + y, cpuTempformat1) / len(cpuTempformat1), 2))
        cpuTempAverage2 = str(round(reduce(lambda x, y: x + y, cpuTempformat2) / len(cpuTempformat2), 2))
        cpuTempAverage3 = str(round(reduce(lambda x, y: x + y, cpuTempformat3) / len(cpuTempformat3), 2))
        cpuTempAverage4 = str(round(reduce(lambda x, y: x + y, cpuTempformat4) / len(cpuTempformat4), 2))
        cpuTempAverage5 = str(round(reduce(lambda x, y: x + y, cpuTempformat5) / len(cpuTempformat5), 2))
        cpuTempAverage6 = str(round(reduce(lambda x, y: x + y, cpuTempformat6) / len(cpuTempformat6), 2))
        cpuTempAverage7 = str(round(reduce(lambda x, y: x + y, cpuTempformat7) / len(cpuTempformat7), 2))
        cpuTempAverage8 = str(round(reduce(lambda x, y: x + y, cpuTempformat7) / len(cpuTempformat8), 2))

        timeIndex = [i for i, x in enumerate(l1) if x == "time"]
        timeValue = []
        for tim in timeIndex:
            timeValue.append(l1[tim + 1])

        timeStampValue = []
        for t in timeValue:
            timeStampValue.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t))))

        # voltageIndex = [i for i, x in enumerate(l1) if x == "Voltage"]
        # voltValue = []
        # for vol in voltageIndex:
        # voltValue.append(l1[vol+1])

        # voltTemp = []
        # for volt in voltValue:
        # voltTemp.append(float(volt)/1000000.00)
        # voltTempformat = [ '%.2f' % elem for elem in voltTemp]
        # voltTempformat=[float(x) for x in voltTempformat]

    #         print "User : ", userformatperValue
    #         print "System : ", systemformatperValue
    #
    #         print "CPU Usage :", cpuUsageformatValue
        print "CPU Frequency : ", cpufreqinMhzformat

        # print "Battery :", batteryTempformat
        # print "CPU Temperature : ", cpuTempformat
        # print "Voltage : ", voltTempformat
        print "Time : ", timeStampValue
        print "CPU Average 1160 Mhz: ", cpu1160Average
        print "CPU Average 900 Mhz: ", cpu900Average
        print "CPU Average 728 Mhz: ", cpu728Average
        print "CPU Average 416 Mhz: ", cpu416Average
        # print 'Battery Temp C'+u"\u00b0"+' Average: ', batteryAverage
        print 'CPU Temp C' + u"\u00b0" + ' Average1: ', cpuTempAverage1
        print 'CPU Temp C' + u"\u00b0" + ' Average2: ', cpuTempAverage2
        print 'CPU Temp C' + u"\u00b0" + ' Average3: ', cpuTempAverage3
        print 'CPU Temp C' + u"\u00b0" + ' Average4: ', cpuTempAverage4
        print 'CPU Temp C' + u"\u00b0" + ' Average5: ', cpuTempAverage5
        print 'CPU Temp C' + u"\u00b0" + ' Average6: ', cpuTempAverage6
        print 'CPU Temp C' + u"\u00b0" + ' Average7: ', cpuTempAverage7
        print 'CPU Temp C' + u"\u00b0" + ' Average8: ', cpuTempAverage8
        cpu1160AverageList = cpu1160Average.split()
        cpu900AverageList = cpu900Average.split()
        cpu728AverageList = cpu728Average.split()
        cpu416AverageList = cpu416Average.split()
        # batteryAverageList = batteryAverage.split()
        cpuTempAverageList1 = cpuTempAverage1.split()
        cpuTempAverageList2 = cpuTempAverage2.split()
        cpuTempAverageList3 = cpuTempAverage3.split()
        cpuTempAverageList4 = cpuTempAverage4.split()
        cpuTempAverageList5 = cpuTempAverage5.split()
        cpuTempAverageList6 = cpuTempAverage6.split()
        cpuTempAverageList7 = cpuTempAverage7.split()
        cpuTempAverageList8 = cpuTempAverage8.split()
        # Create a Pandas dataframe from the data.
        df = pd.DataFrame()

        df2 = pd.DataFrame()
        #         {'CPU Frequency (Mhz)': cpufreqinMhz,'CPU Usage (%)': cpuUsage,'System (%)': systemLst,'User (%)': userLst}
        #         df['User (%)'] = userformatperValue
        #         df['User (%)'] = df['User (%)'].astype(float)
        #         df['System (%)'] = systemformatperValue
        #         df['System (%)'] = df['System (%)'].astype(float)
        #         df['CPU Usage (%)'] = cpuUsageformatValue
        #         df['CPU Usage (%)'] = df['CPU Usage (%)'].astype(float)
        df['CPU Frequency (Mhz)'] = cpufreqinMhzformat

        # df['Battery Temp (C'+u"\u00b0"+')'] = batteryTempformat

        df['CPU Temp1 (C' + u"\u00b0" + ')'] = cpuTempformat1
        df['CPU Temp2 (C' + u"\u00b0" + ')'] = cpuTempformat2
        df['CPU Temp3 (C' + u"\u00b0" + ')'] = cpuTempformat3
        df['CPU Temp4 (C' + u"\u00b0" + ')'] = cpuTempformat4
        df['CPU Temp5 (C' + u"\u00b0" + ')'] = cpuTempformat5
        df['CPU Temp6 (C' + u"\u00b0" + ')'] = cpuTempformat6
        df['CPU Temp7 (C' + u"\u00b0" + ')'] = cpuTempformat7
        df['CPU Temp8 (C' + u"\u00b0" + ')'] = cpuTempformat8
        df['CPU Temp1 (C' + u"\u00b0" + ')'] = df['CPU Temp1 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp2 (C' + u"\u00b0" + ')'] = df['CPU Temp2 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp3 (C' + u"\u00b0" + ')'] = df['CPU Temp3 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp4 (C' + u"\u00b0" + ')'] = df['CPU Temp4 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp5 (C' + u"\u00b0" + ')'] = df['CPU Temp5 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp6 (C' + u"\u00b0" + ')'] = df['CPU Temp6 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp7 (C' + u"\u00b0" + ')'] = df['CPU Temp7 (C' + u"\u00b0" + ')'].astype(float)
        df['CPU Temp8 (C' + u"\u00b0" + ')'] = df['CPU Temp8 (C' + u"\u00b0" + ')'].astype(float)
        # df['Voltage (V)'] = voltTempformat
        # df['Voltage (V)'] = df['Voltage (V)'].astype(float)
        df['Time stamp'] = timeStampValue

        #         df2['CPU Average 1160 Mhz'] =  cpu1160Average
        df2['CPU Average 1160 Mhz'] = cpu1160AverageList
        df2['CPU Average 900 Mhz'] = cpu900AverageList
        df2['CPU Average 728 Mhz'] = cpu728AverageList
        df2['CPU Average 416 Mhz'] = cpu416AverageList
        # df2['Battery Temp C'+u"\u00b0"+' Average'] = batteryAverageList
        df2['CPU Temp1 C' + u"\u00b0" + ' Average'] = cpuTempAverageList1
        df2['CPU Temp2 C' + u"\u00b0" + ' Average'] = cpuTempAverageList2
        df2['CPU Temp3 C' + u"\u00b0" + ' Average'] = cpuTempAverageList3
        df2['CPU Temp4 C' + u"\u00b0" + ' Average'] = cpuTempAverageList4
        df2['CPU Temp5 C' + u"\u00b0" + ' Average'] = cpuTempAverageList5
        df2['CPU Temp6 C' + u"\u00b0" + ' Average'] = cpuTempAverageList6
        df2['CPU Temp7 C' + u"\u00b0" + ' Average'] = cpuTempAverageList7
        df2['CPU Temp8 C' + u"\u00b0" + ' Average'] = cpuTempAverageList8
        # df.index += 1


        #         df2.index += +1
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('Result.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        #         frames = [df,df2]
        #         df.concat(frames)
        df.to_excel(writer, sheet_name='Sheet1')

        df2.to_excel(writer, sheet_name='Sheet1', startcol=12, startrow=4, index=False)

        #         df2.to_excel(writer, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        format1 = workbook.add_format({'num_format': '0.00'})
        #         worksheet.set_column('A:A', 20, format1)
        worksheet.set_column('B:B', 20, format1)
        worksheet.set_column('C:C', 18, format1)
        worksheet.set_column('D:D', 15, format1)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('I:I', 23)
        worksheet.set_column('J:J', 22)
        worksheet.set_column('K:K', 22)
        worksheet.set_column('L:L', 22)
        worksheet.set_column('M:M', 23)
        worksheet.set_column('N:N', 21)

        writer.save()
        writer.close()
        x_ax = len(cpufreqinMhzformat)
        x_ax = range(x_ax)
        y_ax = cpufreqinMhzformat
        #         trace = go.Scatter(x= x_ax, y = y_ax, name = 'CPU Frequency')
        #         data = [trace]


        offline.plot({'data': [{'x': x_ax, 'y': y_ax}],
                      'layout': {'title': 'CPU Frequency (Mhz)',
                                 'font': dict(size=16)}}, filename='CPU_Frequency.html', auto_open=False
                     )
        #         offline.plot({'data': [{'x':x_ax,'y': cpuUsageformatValue}],
        #                        'layout': {'title': 'CPU Usage',
        #                                   'font': dict(size=16)}}, filename = path+'CPU_Usage.html',auto_open=False
        #                      )
        # offline.plot({'data': [{'x':x_ax,'y': batteryTempformat}],
        # 'layout': {'title': 'Battery (C'+u"\u00b0"+')',
        # 'font': dict(size=16)}}, filename = path+'Battery.html',auto_open=False
        # )

        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat1}],
                      'layout': {'title': 'CPU Temp1 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename='CPU_Temperature1.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat2}],
                      'layout': {'title': 'CPU Temp2 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename='CPU_Temperature2.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat3}],
                      'layout': {'title': 'CPU Temp3 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename='CPU_Temperature3.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat4}],
                      'layout': {'title': 'CPU Temp4 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename= 'CPU_Temperature4.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat5}],
                      'layout': {'title': 'CPU Temp5 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename='CPU_Temperature5.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat6}],
                      'layout': {'title': 'CPU Temp6 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename= 'CPU_Temperature6.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat7}],
                      'layout': {'title': 'CPU Temp7 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename= 'CPU_Temperature7.html', auto_open=False
                     )
        offline.plot({'data': [{'x': x_ax, 'y': cpuTempformat8}],
                      'layout': {'title': 'CPU Temp8 (C' + u"\u00b0" + ')',
                                 'font': dict(size=16)}}, filename='CPU_Temperature8.html', auto_open=False
                     )

        #         self.creatResultZip(osPlatform)
        #         py.iplot(data, filename = "hello")
        # Close the Pandas Excel writer and output the Excel file.


exc = cpuBenchmark()
exc.cpuUsageInfo()
