import re
import ast
import json
import time
from itertools import chain
import logPharser
import pandas as pd

class validationPharser(object):
    def __init__(self):
        pass

    def matchListEqual(self, listOne, listTwo, matchingFDATemplate, matchingComTemplate):
        maxLength = max(len(listOne), len(listTwo))

        if len(listOne) == len(listTwo):
            pass
        else:
            if len(listOne) != maxLength:
                diff1 = maxLength - len(listOne)
                for i in range(diff1):
                    listOne.append(matchingFDATemplate)
            if len(listTwo) != maxLength:
                diff2 = maxLength - len(listTwo)
                for i in range(diff2):
                    listTwo.append(matchingComTemplate)
        return listOne, listTwo


    def extractValResult(self, valLogs, rpmLogs, valTemplate, rpmTemplate, valList, rpmList, rpmDate, valDate, devicesRunning, PATH_BASE):

        logObj = logPharser.logPharser()

        tempVal = logObj.extractDic(valLogs)
        valLst = logObj.extractDictofDict(tempVal)
        print valLst

        rpmLst = logObj.extractDic(rpmLogs)
        print rpmLst


        # match2 = '{"Weight":0,"unit":"NA","measurementTime":"0","receiptTime":"NA","date":"NA","model":"NA","manufacturer":"NA","serialnumber":"NA"}'
        # valmatch = '{"weightMax":0, "weightMin":0, "date":"0"}'

        validationTemp, rpmTemp = self.matchListEqual(valLst, rpmLst, valTemplate, rpmTemplate)


        print len(validationTemp)
        print len(rpmTemp)

        rpm = []

        match = []
        # for i in range(len(validationTemp)):
        #     j = dict((k, v) for k, v in ast.literal_eval(validationTemp[i]).iteritems())
        #     for m in range(len(rpmTemp)):
        #         p = dict((k, v) for k, v in ast.literal_eval(rpmTemp[m]).iteritems())
        #
        #         if j[valDate] == p[valDate]:
        #             for u in range(len(rpmList)):
        #                 val2 = float(p[rpmList[u]])
        #                 max = float(j[valList[u][0]])
        #                 min = float(j[valList[u][1]])
        #                 if val2 >= min and val2 <= max:
        #                     match.append(tuple((i, m)))
        for i in range(len(validationTemp)):
            j = dict((k, v) for k, v in ast.literal_eval(validationTemp[i]).iteritems())
            for m in range(len(rpmTemp)):
                p = dict((k, v) for k, v in ast.literal_eval(rpmTemp[m]).iteritems())

                if j[valDate] == p[rpmDate]:
                    print devicesRunning
                    if 'BP' in devicesRunning:
                        Diaval = p['Diastolic']
                        SysVal = p['Systolic']
                        PulseVal = p['Pulse']
                        diaMax = j[valList[0][0]]
                        diaMin = j[valList[0][1]]
                        sysMax = j[valList[1][0]]
                        sysMin = j[valList[1][1]]
                        pulseMax = j[valList[2][0]]
                        pulseMin = j[valList[2][1]]
                        if (float(Diaval) <= float(diaMax) and float(Diaval) >= float(diaMin) and float(
                                SysVal) <= float(sysMax) and float(SysVal) >= float(sysMin) and
                                    float(PulseVal) <= float(pulseMax) and float(PulseVal) >= float(pulseMin)):
                            match.append(tuple((i, m)))
                    if 'Weight' in devicesRunning:
                        weightVal = p['Weight']
                        print weightVal
                        weightMax = j[valList[0][0]]
                        weightMin = j[valList[0][1]]
                        if (float(weightVal) <= float(weightMax) and float(weightVal) >= float(weightMin)):
                            match.append(tuple((i, m)))

                    if 'PO' in devicesRunning:
                        spo2Val = p['spo2']
                        bpmVal = p['BPM']
                        spo2Max = j[valList[0][0]]
                        spo2Min = j[valList[0][1]]
                        bpmMax = j[valList[1][0]]
                        bpmMin = j[valList[1][1]]
                        if (float(spo2Val) >= float(spo2Min) and float(spo2Val) <= float(spo2Max) and float(bpmVal) >=
                            float(bpmMin) and float(bpmVal) <= float(bpmMax)):
                            match.append(tuple((i, m)))

        #match = set(match)
        print match
        matchvalWeight, matchrpmWeight = [e[0] for e in match], [e[1] for e in match]

        rpmMissingIndex = range(len(rpmTemp))
        valMissingIndex = range(len(validationTemp))
        rpmMatch = set(matchrpmWeight)
        valMatch = set(matchvalWeight)
        print valMatch
        print rpmMatch
        print set(match)
        print matchrpmWeight
        print matchvalWeight
        nonmatchRPMIndex = filter(lambda x: x not in rpmMatch, rpmMissingIndex)
        nonmatchvalIndex = filter(lambda x: x not in valMatch, valMissingIndex)
        vali = []

        for i in matchvalWeight:
            t = dict((k, v) for k, v in ast.literal_eval(validationTemp[i]).iteritems())
            vali.append(t.copy())
        li = list(chain(*valList))
        print li

        q = logObj.extractValPassData(li, vali)
        print q
        for i in matchrpmWeight:
            t = dict((k, v) for k, v in ast.literal_eval(rpmTemp[i]).iteritems())
            rpm.append(t.copy())
        r = logObj.extractPassData(rpmList, rpm)
        print r
        nonvali = []
        nonrpm = []
        for i in nonmatchvalIndex:
            t = dict((k, v) for k, v in ast.literal_eval(validationTemp[i]).iteritems())
            nonvali.append(t)
        for i in nonmatchRPMIndex:
            t = dict((k, v) for k, v in ast.literal_eval(rpmTemp[i]).iteritems())
            nonrpm.append(t)
        nonrpm = sorted(nonrpm, key=lambda k: k[rpmDate])
        nonvali = sorted(nonvali, key=lambda k: k[valDate])
        print q + nonvali
        print r + nonrpm

        valpasscount = logObj.addData('Pass', q)
        rpmPassCount = logObj.addData('Pass', r)
        valfailcount = logObj.addData('Fail', nonvali)
        rpmFailCount = logObj.addData('Fail', nonrpm)
        dataType = logObj.addData(devicesRunning, rpmPassCount)
        dataType1 = logObj.addData(devicesRunning, rpmFailCount)

        print len(rpmPassCount)
        print len(rpmFailCount)
        print len(q)
        print len(nonrpm)
        print len(nonvali)

        df = pd.DataFrame()
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df['Data type'] = dataType
        df['RPM'] = r
        df['Validation'] = q
        df['Result'] = rpmPassCount
        df1['Data type'] = dataType1
        df1['RPM'] = nonrpm
        df1['Validation'] = nonvali
        df1['Result'] = rpmFailCount


        h = df.append(df1, ignore_index=True)
        print h
        # df4 = pd.concat([h, h2], axis=1)
        writer = pd.ExcelWriter(PATH_BASE+devicesRunning+'ValResult.xlsx',
                                engine='xlsxwriter')
        h.to_excel(writer, sheet_name='Report', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Report']
        writer.save()
        writer.close()


# dict1 = '''
#
# Line 6241: 07-05 12:15:06.242  2216  2216 D Validation_automation: LN-1118 -- getBpRecord:: {"BPRecord": [{"sysMax":90, "sysMin":80, "diaMax":70, "diaMin":60, "pulseMax":50, "pulseMin":40, "date":"2017-07-05 12:15:06"}]}
# 	Line 10833: 07-05 12:16:06.320  2216  2216 D Validation_automation: LN-1118 -- getBpRecord:: {"BPRecord": [{"sysMax":40, "sysMin":20, "diaMax":70, "diaMin":60, "pulseMax":50, "pulseMin":40, "date":"2017-07-05 12:16:06"}]}
# 	Line 15107: 07-05 12:17:06.375  2216  2216 D Validation_automation: LN-1118 -- getBpRecord:: {"BPRecord": [{"sysMax":90, "sysMin":80, "diaMax":70, "diaMin":60, "pulseMax":50, "pulseMin":40, "date":"2017-07-05 12:17:06"}]}
# 	Line 18887: 07-05 12:18:06.461  2216  2216 D Validation_automation: LN-1118 -- getBpRecord:: {"BPRecord": [{"sysMax":90, "sysMin":80, "diaMax":70, "diaMin":60, "pulseMax":50, "pulseMin":40, "date":"2017-07-05 12:18:06"}]}
# 	Line 22015: 07-05 12:19:06.533  2216  2216 D Validation_automation: LN-1118 -- getBpRecord:: {"BPRecord": [{"sysMax":90, "sysMin":80, "diaMax":70, "diaMin":60, "pulseMax":50, "pulseMin":40, "date":"2017-07-05 12:19:06"}]}
#
# 	'''
# dict2 = '''
# 	Line 6553: 07-05 12:15:07.240  2138  2138 I RPM_DatabaseAccessor_automation: LN-187 -- insertBPDeviceData:: insertBPDeviceData deviceDataList data...{"Diastolic":"169.0","Systolic":"88.0","Pulse":"50.0","unit":"mmHg","measurementTime":"2017-07-05 12:15:06","receiptTime":"2017-07-05T12:15:07.007-07:00","date":1499282107000,"model":"2009","manufacturer":"CONTINUA","serialnumber":"SN_BP082"}
# 	Line 10941: 07-05 12:16:06.399  2138  2138 I RPM_DatabaseAccessor_automation: LN-187 -- insertBPDeviceData:: insertBPDeviceData deviceDataList data...{"Diastolic":"163.0","Systolic":"90.0","Pulse":"47.0","unit":"mmHg","measurementTime":"2017-07-05 12:16:06","receiptTime":"2017-07-05T12:16:06.006-07:00","date":1499282166000,"model":"2009","manufacturer":"CONTINUA","serialnumber":"SN_BP082"}
# 	Line 15215: 07-05 12:17:06.495  2138  2138 I RPM_DatabaseAccessor_automation: LN-187 -- insertBPDeviceData:: insertBPDeviceData deviceDataList data...{"Diastolic":"68.0","Systolic":"85.0","Pulse":"50.0","unit":"mmHg","measurementTime":"2017-07-05 12:17:06","receiptTime":"2017-07-05T12:17:06.006-07:00","date":1499282226000,"model":"2009","manufacturer":"CONTINUA","serialnumber":"SN_BP082"}
# 	Line 18997: 07-05 12:18:06.556  2138  2138 I RPM_DatabaseAccessor_automation: LN-187 -- insertBPDeviceData:: insertBPDeviceData deviceDataList data...{"Diastolic":"60.0","Systolic":"89.0","Pulse":"49.0","unit":"mmHg","measurementTime":"2017-07-05 12:18:06","receiptTime":"2017-07-05T12:18:06.006-07:00","date":1499282286000,"model":"2009","manufacturer":"CONTINUA","serialnumber":"SN_BP082"}
# 	Line 22123: 07-05 12:19:06.616  2138  2138 I RPM_DatabaseAccessor_automation: LN-187 -- insertBPDeviceData:: insertBPDeviceData deviceDataList data...{"Diastolic":"68.0","Systolic":"80.0","Pulse":"44.0","unit":"mmHg","measurementTime":"2017-07-05 12:19:06","receiptTime":"2017-07-05T12:19:06.006-07:00","date":1499282346000,"model":"2009","manufacturer":"CONTINUA","serialnumber":"SN_BP082"}
#
# '''
# match2 = '{"Diastolic":"0","Systolic":"0","Pulse":"0","unit":"NA","measurementTime":"0","receiptTime":"NA","date":"NA,"model":"NA","manufacturer":"NA","serialnumber":"NA"}'
# valmatch = '{"sysMax":0, "sysMin":0, "diaMax":0, "diaMin":0, "pulseMax":0, "pulseMin":0, "date":"0"}'
# rpmval = ['Diastolic','Systolic','Pulse']
# valiweight = [('diaMax','diaMin'),('sysMax','sysMin'),('pulseMax','pulseMin')]
# valDate = "date"
# rpmDate = "measurementTime"
#
# v = validationPharser()
# v.extractValResult(dict1,dict2, valmatch, match2, valiweight, rpmval, rpmDate, valDate, "BP")