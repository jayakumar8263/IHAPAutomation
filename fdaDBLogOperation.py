import re
import pandas as pd
import time


class fdaDBLogOperation(object):

    def __int__(self):
        pass

    def fdaRawValues(self, fdaADBLogs):

        fdaStr = ' '.join(fdaADBLogs)
        fdaListFormat = re.sub('[^a-zA-Z0-9 \n\.]', ' ', fdaStr)

        fdaList = fdaListFormat.split(" ")
        fdaList = ' '.join(fdaList).split()

        return fdaList

    def fdaWeight(self, rawWeightValues):

        weightIndex = [i for i, x in enumerate(rawWeightValues) if x == 'Weight']

        weightValue = []
        weightTimeStamp = []

        for freq in weightIndex:
            weightValue.append(rawWeightValues[freq + 1])
            gmtTime = time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(int(rawWeightValues[freq + 5])/1000.))
            weightTimeStamp.append(gmtTime)

        weightValue = [float(x) for x in weightValue]

        print "FDA Weight: ", weightValue
        print "FDA Weight Timestamp: ", weightTimeStamp
        return weightValue, weightTimeStamp

    def fdaPO(self, rawPOValues):

        poSPOIndex = [i for i, x in enumerate(rawPOValues) if x == 'spo2']
        poBPMIndex = [i for i, x in enumerate(rawPOValues) if x == 'BPM']

        poBPMValue = []
        poSPOValue = []
        poTimeStamp = []

        for poSPOi in poSPOIndex:
            poSPOValue.append(rawPOValues[poSPOi + 1])

        for poBPMi in poBPMIndex:
            poBPMValue.append(rawPOValues[poBPMi + 1])
            gmtTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(rawPOValues[poBPMi + 4]) / 1000.))
            poTimeStamp.append(gmtTime)

        poBPMValue = [float(x) for x in poBPMValue]
        poSPOValue = [float(x) for x in poSPOValue]

        print "FDA POBPM : ", poBPMValue
        print "FDA POSPO : ", poSPOValue
        print "FDA PO Timestamp : ", poTimeStamp

        return poBPMValue, poSPOValue, poTimeStamp

    def fdaBP(self, bpRawValues):

        bpDiastolicIndex = [i for i, x in enumerate(bpRawValues) if x == 'Diastolic']
        bpSystolicIndex = [i for i, x in enumerate(bpRawValues) if x == 'Systolic']
        bpPulseIndex = [i for i, x in enumerate(bpRawValues) if x == 'Pulse']

        bpDiastolicValue = []
        bpSystolicValue = []
        bpPulseValue = []
        bpTimeStamp = []

        for bpDia in bpDiastolicIndex:
            bpDiastolicValue.append(bpRawValues[bpDia + 1])

        for bpSys in bpSystolicIndex:
            bpSystolicValue.append(bpRawValues[bpSys + 1])

        for bpPulse in bpPulseIndex:
            bpPulseValue.append(bpRawValues[bpPulse + 1])

            gmtTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(bpRawValues[bpPulse + 5]) / 1000.))
            bpTimeStamp.append(gmtTime)

        bpDiastolicValue = [float(x) for x in bpDiastolicValue]
        bpSystolicValue = [float(x) for x in bpSystolicValue]
        bpPulseValue = [float(x) for x in bpPulseValue]

        print "FDA BP SYS Value: ", bpSystolicValue
        print "FDA BP Pulse Value : ", bpPulseValue
        print "FDA BP Dia Value : ", bpDiastolicValue
        print "FDA BP TimeStamp : ", bpTimeStamp

        return bpDiastolicValue, bpSystolicValue, bpPulseValue, bpTimeStamp

    def fdaValuesExcelPharse(self, filePath, fdaWeightValue , fdaweightTimeStamp ,fdaPOBPMValue, fdaSPOValue ,
                                   fdaPOTimeStamp, fdaBPSYSValue, fdaBPPulseValue, fdaBPDiaValue, fdaBPTimeStamp):

        df = pd.DataFrame({'FDA Weight': fdaWeightValue, 'FDA Weight Timestamp': fdaweightTimeStamp})
        df1 = pd.DataFrame({'FDA PO BPM': fdaPOBPMValue, 'FDA PO SPO': fdaSPOValue, 'FDA PO Timestamp' : fdaPOTimeStamp})
        df2 = pd.DataFrame({'FDA BP Systolic': fdaBPSYSValue, 'FDA BP Pulse':fdaBPPulseValue, 'FDA BP Diastolic':fdaBPDiaValue,
                            'FDA BP Timestamp': fdaBPTimeStamp})

        df4 = pd.concat([df, df1, df2], axis=1)

        writer = pd.ExcelWriter(filePath + 'FDAResult.xlsx', engine='xlsxwriter')
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