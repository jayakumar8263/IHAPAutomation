import re
import pandas as pd
import time


class commLogOperation(object):

    def __int__(self):
        pass

    def comRawValues(self, comADBLogs):

        comStr = ' '.join(comADBLogs)
        comListFormat = re.sub('[^a-zA-Z0-9 \n\.]', ' ', comStr)

        comList = comListFormat.split(" ")
        comList = ' '.join(comList).split()

        return comList

    def comWeight(self, rawWeightValues):

        weightIndex = [i for i, x in enumerate(rawWeightValues) if x == 'Weight']


        weightValue = []
        weightTimeStamp = []
        # print rawWeightValues
        # print weightIndex
        for freq in weightIndex:
            weightValue.append(rawWeightValues[freq + 1])
            print freq
            gmtTime = time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(int(rawWeightValues[freq - 10])/1000.))
            weightTimeStamp.append(gmtTime)

        weightValue = [float(x) for x in weightValue]

        print "Com. Weight: ", weightValue
        print "Com. Weight Timestamp: ", weightTimeStamp
        return weightValue, weightTimeStamp

    def comPO(self, rawPOValues):

        poSPOIndex = [i for i, x in enumerate(rawPOValues) if x == 'spo2']
        poBPMIndex = [i for i, x in enumerate(rawPOValues) if x == 'BPM']

        poBPMValue = []
        poSPOValue = []
        poTimeStamp = []

        for poSPOi in poSPOIndex:
            poSPOValue.append(rawPOValues[poSPOi + 1])
            gmtTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(rawPOValues[poSPOi + 3]) / 1000.))
            poTimeStamp.append(gmtTime)

        for poBPMi in poBPMIndex:
            poBPMValue.append(rawPOValues[poBPMi + 1])

        poBPMValue = [float(x) for x in poBPMValue]
        poSPOValue = [float(x) for x in poSPOValue]

        print "Com. POBPM : ", poBPMValue
        print "Com. POSPO : ", poSPOValue
        print "Com. PO Timestamp : ", poTimeStamp

        return poBPMValue, poSPOValue, poTimeStamp

    def comBP(self, bpRawValues):

        bpDiastolicIndex = [i for i, x in enumerate(bpRawValues) if x == 'Diastolic']
        bpSystolicIndex = [i for i, x in enumerate(bpRawValues) if x == 'Systolic']
        bpPulseIndex = [i for i, x in enumerate(bpRawValues) if x == 'Pulse']

        bpDiastolicValue = []
        bpSystolicValue = []
        bpPulseValue = []
        bpTimeStamp = []

        for bpDia in bpDiastolicIndex:
            bpDiastolicValue.append(bpRawValues[bpDia + 1])
            gmtTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(bpRawValues[bpDia + 3]) / 1000.))
            bpTimeStamp.append(gmtTime)

        for bpSys in bpSystolicIndex:
            bpSystolicValue.append(bpRawValues[bpSys + 1])

        for bpPulse in bpPulseIndex:
            bpPulseValue.append(bpRawValues[bpPulse + 1])



        bpDiastolicValue = [float(x) for x in bpDiastolicValue]
        bpSystolicValue = [float(x) for x in bpSystolicValue]
        bpPulseValue = [float(x) for x in bpPulseValue]

        print "Com BP SYS Value: ", bpSystolicValue
        print "Com BP Pulse Value : ", bpPulseValue
        print "Com BP Dia Value : ", bpDiastolicValue
        print "Com BP TimeStamp : ", bpTimeStamp

        return bpDiastolicValue, bpSystolicValue, bpPulseValue, bpTimeStamp

    def comValuesExcelPharse(self, filePath, comWeightValue , comweightTimeStamp ,comPOBPMValue, comSPOValue ,
                                   comPOTimeStamp, comBPSYSValue, comBPPulseValue, comBPDiaValue, comBPTimeStamp):

        df = pd.DataFrame({'COM Weight': comWeightValue, 'COM Weight Timestamp': comweightTimeStamp})
        df1 = pd.DataFrame({'COM PO BPM': comPOBPMValue, 'COM PO SPO': comSPOValue, 'COM PO Timestamp' : comPOTimeStamp})
        df2 = pd.DataFrame({'COM BP Systolic': comBPSYSValue, 'COM BP Pulse':comBPPulseValue, 'COM BP Diastolic':comBPDiaValue,
                            'COM BP Timestamp': comBPTimeStamp})

        df4 = pd.concat([df, df1, df2], axis=1)

        writer = pd.ExcelWriter(filePath + 'CommunicationResult.xlsx', engine='xlsxwriter')
        df4.to_excel(writer, sheet_name='Sheet1', index = False)

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