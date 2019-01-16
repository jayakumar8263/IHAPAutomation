import pandas as pd

class rpmLogOperation(object):


    def __int__(self):
        pass

    def rmpRawValue(self, adbLogs):

        # print len(adbLogs)
        p = ",".join(adbLogs)

        o = p.split("--")
        o = map(str.strip, o)

        # print o
        return o

    def rpmWeight(self, rawValues):
        weightIndex = [i for i, x in enumerate(rawValues) if x == 'WEIGHT']

        weightValue = []
        weightTimeStamp = []

        for freq in weightIndex:
            weightValue.append(rawValues[freq + 1])
            weightTimeStamp.append(rawValues[freq + 2])

        weightValue = [float(x) for x in weightValue]


        print "Weight: ", weightValue
        print "Weight Timestamp: ", weightTimeStamp
        return weightValue, weightTimeStamp

    def rpmPOValues(self, rawPOValues):
        poIndex = [i for i, x in enumerate(rawPOValues) if x == 'PO']

        poBPMValue = []
        poSPOValue = []
        poTimeStamp = []
        poDeviceName = []
        for poValue in poIndex:
            poBPMValue.append(rawPOValues[poValue + 2])
            poSPOValue.append(rawPOValues[poValue + 1])
            poTimeStamp.append(rawPOValues[poValue + 3])
            # poDeviceName.append(rawPOValues[poValue+6])

        poBPMValue = [float(x) for x in poBPMValue]
        poSPOValue = [float(x) for x in poSPOValue]


        # poDevice = ','.join(poDeviceName)
        # poDevice = poDevice.split(',')
        # poDevice = poDevice[::2]

        print "POBPM : ", poBPMValue
        print "POSPO : ", poSPOValue
        print "PO Timestamp : ", poTimeStamp

        return poBPMValue, poSPOValue, poTimeStamp

    def rpmBPValues(self, rawBPValues):
        bpIndex = [i for i, x in enumerate(rawBPValues) if x == 'BP']

        bpSysValue = []
        bpPulseValue = []
        bpDiaValue = []
        bpTimeStamp = []
        bpDeviceName = []
        for bpValue in bpIndex:
            bpSysValue.append(rawBPValues[bpValue + 1])
            bpPulseValue.append(rawBPValues[bpValue + 2])
            bpDiaValue.append(rawBPValues[bpValue + 3])
            bpTimeStamp.append(rawBPValues[bpValue + 4])
            # bpDeviceName.append(rawBPValues[bpValue + 5])

        bpSysValue = [float(x) for x in bpSysValue]
        bpPulseValue = [float(x) for x in bpPulseValue]
        bpDiaValue = [float(x) for x in bpDiaValue]

        # bpDevice = ','.join(bpDeviceName)
        # bpDevice = bpDevice.split(',')
        # bpDevice = bpDevice[::2]

        print "BP SYS Value: ", bpSysValue
        print "BP Pulse Value : ", bpPulseValue
        print "BP Dia Value : ", bpDiaValue
        print "BP TimeStamp : ", bpTimeStamp

        return bpSysValue, bpPulseValue, bpDiaValue, bpTimeStamp

    def rpmValuesExcelPharse(self, filePath, rpmWeightValue , weightTimeStamp ,poBPMValue,poSPOValue ,
                                   poTimeStamp, bpSYSValue, bpPulseValue, bpDiaValue, bpTimeStamp):

        df = pd.DataFrame({'RPM Weight': rpmWeightValue, 'RPM Weight Timestamp': weightTimeStamp})
        df1 = pd.DataFrame({'RPM PO BPM': poBPMValue, 'RPM PO SPO': poSPOValue, 'RPM PO Timestamp' : poTimeStamp})
        df2 = pd.DataFrame({'RPM BP Systolic': bpSYSValue, 'RPM BP Pulse':bpPulseValue, 'RPM BP Diastolic':bpDiaValue,
                            'RPM BP Timestamp': bpTimeStamp})

        df4 = pd.concat([df, df1, df2], axis=1)

        writer = pd.ExcelWriter(filePath + 'RPMResult.xlsx', engine='xlsxwriter')
        df4.to_excel(writer, sheet_name='Sheet1' , index = False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})

        worksheet.set_column('A:A', 11, format1)
        worksheet.set_column('B:B', 21, format1)
        worksheet.set_column('C:C', 12, format1)
        worksheet.set_column('D:D', 11, format1)
        worksheet.set_column('E:E', 17, format1)
        worksheet.set_column('F:F', 15, format1)
        worksheet.set_column('G:G', 12, format1)
        worksheet.set_column('H:H', 14, format1)
        worksheet.set_column('I:I', 17, format1)
        worksheet.set_column('J:J', 14, format1)
        worksheet.set_column('K:K', 17, format1)

        writer.save()
        writer.close()