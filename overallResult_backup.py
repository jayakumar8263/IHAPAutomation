from austonioLibraries import fdaDBLogOperation
from austonioLibraries import commLogOperation
from austonioLibraries import rpmLogOperation
import pandas as pd
from austonioLibraries import Search
from austonioLibraries import serverOperation
# import numpy as np
import time
import re
from austonioLibraries import htmlReport

DATATYPE = []
PASSNFAIL = []
RPMVALUES = []
RPMTIMESTAMP = []
FDAVALUES = []
FDATIMESTAMP = []
COMVALUES = []
COMTIMESTAMP = []
SERVERDATATYPE = []
SERVERVALUES = []
SERVERTIMESTAMP = []

class overallResult(object):

    def __init__(self):
        pass

    def executionResult(self,PATH_BASE, logFile , rpmList, fdaList, comList, serverList):
        rpmLogObj = rpmLogOperation.rpmLogOperation()
        fdaObj = fdaDBLogOperation.fdaDBLogOperation()
        comObj = commLogOperation.commLogOperation()
        userServerDataobj = serverOperation.serverOperation()

        rpmWeightValue, weightTimeStamp = rpmLogObj.rpmWeight(rpmList)

        poBPMValue, poSPOValue, poTimeStamp = rpmLogObj.rpmPOValues(rpmList)

        bpSYSValue, bpPulseValue, bpDiaValue, bpTimeStamp = rpmLogObj.rpmBPValues(rpmList)

        rpmLogObj.rpmValuesExcelPharse(PATH_BASE, rpmWeightValue, weightTimeStamp, poBPMValue, poSPOValue,
                                       poTimeStamp, bpSYSValue, bpPulseValue, bpDiaValue, bpTimeStamp)

        fdaWeighValue, fdaWeightTimeStamp = fdaObj.fdaWeight(fdaList)

        fdapoBPMValue, fdapoSPOValue, fdapoTimeStamp = fdaObj.fdaPO(fdaList)

        fdabpDiastolicValue, fdabpSystolicValue, fdabpPulseValue, fdabpTimeStamp = fdaObj.fdaBP(fdaList)

        fdaObj.fdaValuesExcelPharse(PATH_BASE, fdaWeighValue, fdaWeightTimeStamp, fdapoBPMValue, fdapoSPOValue,
                                    fdapoTimeStamp,
                                    fdabpSystolicValue, fdabpPulseValue, fdabpDiastolicValue, fdabpTimeStamp)

        comWeighValue, comWeightTimeStamp = comObj.comWeight(comList)

        compoBPMValue, compoSPOValue, compoTimeStamp = comObj.comPO(comList)

        combpDiastolicValue, combpSystolicValue, combpPulseValue, combpTimeStamp = comObj.comBP(comList)

        comObj.comValuesExcelPharse(PATH_BASE, comWeighValue, comWeightTimeStamp, compoBPMValue, compoSPOValue,
                                    compoTimeStamp,
                                    combpSystolicValue, combpPulseValue, combpDiastolicValue, combpTimeStamp)

        serverWeightValue, serverweightTimeStamp = userServerDataobj.serverWeight(serverList)

        serverpoBPMValue, serverpoSPOValue, serverpoTimeStamp = userServerDataobj.serverPO(serverList)

        serverbpDiaValue, serverbpSYSValue, serverbpPulseValue, serverbpTimeStamp = userServerDataobj.serverBP(serverList)

        userServerDataobj.serverValuesExcelPharse(PATH_BASE, serverWeightValue, serverweightTimeStamp, serverpoBPMValue, serverpoSPOValue,
                                serverpoTimeStamp, serverbpSYSValue, serverbpPulseValue, serverbpDiaValue, serverbpTimeStamp)

        self.overallWeigthResult(PATH_BASE, rpmWeightValue,weightTimeStamp, fdaWeighValue, fdaWeightTimeStamp,
                            comWeighValue, comWeightTimeStamp, serverWeightValue, serverweightTimeStamp)

        self.overallPOResult(PATH_BASE, poBPMValue, poSPOValue, poTimeStamp, fdapoBPMValue,
                             fdapoSPOValue, fdapoTimeStamp, compoBPMValue,
                             compoSPOValue, compoTimeStamp, serverpoBPMValue,
                             serverpoSPOValue, serverpoTimeStamp)
        self.overallBPResult(PATH_BASE, bpSYSValue,bpPulseValue, bpDiaValue, bpTimeStamp,
                             fdabpSystolicValue, fdabpPulseValue, fdabpDiastolicValue,
                             fdabpTimeStamp, combpSystolicValue, combpPulseValue,
                             combpDiastolicValue, combpTimeStamp, serverbpSYSValue, serverbpPulseValue,
                             serverbpDiaValue, serverbpTimeStamp)
        rpmWeightValue = list(set(rpmWeightValue))
        poSPOValue = list(set(poSPOValue))
        bpSYSValue = list(set(bpSYSValue))
        comWeighValue = list(set(comWeighValue))
        compoSPOValue = list(set(compoSPOValue))
        combpSystolicValue = list(set(combpSystolicValue))
        fdaWeighValue = list(set(fdaWeighValue))
        fdapoSPOValue = list(set(fdapoSPOValue))
        fdabpSystolicValue = list(set(fdabpSystolicValue))
        serverWeightValue = list(set(serverWeightValue))
        serverpoSPOValue = list(set(serverpoSPOValue))
        serverbpSYSValue = list(set(serverbpSYSValue))
        lenRPM = len(rpmWeightValue)+len(poSPOValue)+len(bpSYSValue)
        lenFDA = len(fdaWeighValue)+len(fdapoSPOValue)+len(fdabpSystolicValue)
        lenCOM = len(comWeighValue)+len(compoSPOValue) +len(combpSystolicValue)
        lenServer = len(serverWeightValue)+len(serverpoSPOValue)+len(serverbpSYSValue)

        maxLength = max(lenRPM,lenFDA,lenCOM,lenServer)

        if lenRPM == lenFDA and lenRPM == lenCOM and lenRPM == lenServer:
            pass
        else:
            if lenRPM != maxLength:
                rpmDifference = maxLength - lenRPM
                for i in range(rpmDifference):
                    rpmWeightValue.append(0)
                    poSPOValue.append(0)
                    poBPMValue.append(0)
                    bpSYSValue.append(0)
                    bpPulseValue.append(0)
                    bpDiaValue.append(0)

        validationLst = self.validationLogPharse(logFile)

        rpmVal, rpmValResult, valValues, valdataType = self.validationPhrase(PATH_BASE, validationLst, rpmWeightValue, poSPOValue, poBPMValue,
                              bpSYSValue, bpPulseValue, bpDiaValue)
        time.sleep(5)


        ex1 = pd.read_excel(PATH_BASE+'WeightResult.xlsx',
                            keep_default_na=True, na_values=[" "])

        ex2 = pd.read_excel(PATH_BASE+'POResult.xlsx',
                            keep_default_na=True, na_values=[" "])

        ex3 = pd.read_excel(PATH_BASE+'BPResult.xlsx',
                            keep_default_na=True, na_values=[" "])

        h = pd.concat([ex1, ex2, ex3])

        # df1 = h.sort_values(by='FDA Timestamp', ascending=1)
        df4 = h.reindex_axis(ex1.columns, axis=1)
        df1 = df4.sort_values(by='FDA Timestamp', ascending=1)
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
        maxValues = str(maxLength+2)
        col = 'A1:P'+maxValues
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

        generateReport = htmlReport.htmlReport()
        finalResultPath= PATH_BASE + 'FinalResult.xlsx'
        validationPath = PATH_BASE + 'ValidationResult.xlsx'
        generateReport.generateHTML(finalResultPath, validationPath, PATH_BASE)


    def validationLogPharse(self, fileName):
        logSearch = Search.logSearch()
        valkeyword = ["Validation_automation", 'Max']
        valRawValue = logSearch.keywordSearch(fileName, *valkeyword)
        valResult = ' '.join(valRawValue)
        valResult = re.sub('[^a-zA-Z0-9 \n\.]', ' ', valResult)
        validationLst = valResult.split()
        return validationLst

    def validationPhrase(self, filePath, validationLst, rpmWeightValue, poSPOValue, poBPMValue, bpSYSValue, bpPulseValue, bpDiaValue):

        valWeightIndex = [i for i, x in enumerate(validationLst) if x == 'WeightRecord']
        valValues = []
        poVal = []
        bpVal = []
        weightMinVal = []
        weightMaxVal = []
        dataType = []

        for i in valWeightIndex:
            weightMaxVal.append(validationLst[i + 2])
            weightMinVal.append(validationLst[i + 4])

        valWeightResult = []
        print len(weightMinVal)
        print len(rpmWeightValue)
        for i in range(len(rpmWeightValue)):

            if rpmWeightValue[i] >= int(weightMinVal[i]) and rpmWeightValue[i] <= int(weightMaxVal[i]):
                valWeightResult.append("Pass")
                valValues.append(weightMinVal[i]+'-'+weightMaxVal[i])
                dataType.append("Weight")
            else:
                valWeightResult.append("Fail")
                valValues.append(weightMinVal[i] + '-' + weightMaxVal[i])
                dataType.append("Weight")

        valPOIndex = [i for i, x in enumerate(validationLst) if x == 'PORecord']

        minspoVal = []
        maxspoVal = []
        minbpmVal = []
        maxbpmVal = []

        for i in valPOIndex:
            minspoVal.append(validationLst[i + 4])
            maxspoVal.append(validationLst[i + 2])
            minbpmVal.append(validationLst[i + 8])
            maxbpmVal.append(validationLst[i + 6])

        valPOResult = []
        for i in range(len(poSPOValue)):

            if (poSPOValue[i] >= int(minspoVal[i]) and poSPOValue[i] <= int(maxspoVal[i]) and poBPMValue[i] >= int(minbpmVal[i])
                and poBPMValue[i] <= int(maxbpmVal[i])):
                valPOResult.append("Pass")
                valValues.append(minspoVal[i] + '-' + maxspoVal[i]+'|'+minbpmVal[i]+'-'+maxbpmVal[i])
                dataType.append("PO")
            else:
                valPOResult.append("Fail")
                valValues.append(minspoVal[i] + '-' + maxspoVal[i] + '|' + minbpmVal[i] + '-' + maxbpmVal[i])
                dataType.append("PO")

        valBPIndex = [i for i, x in enumerate(validationLst) if x == 'BPRecord']

        minSysVal = []
        maxSysVal = []
        minDiaVal = []
        maxDiaVal = []
        minPulseVal = []
        maxPulseVal = []

        for i in valBPIndex:
            minSysVal.append(validationLst[i + 4])
            maxSysVal.append(validationLst[i + 2])
            minDiaVal.append(validationLst[i + 8])
            maxDiaVal.append(validationLst[i + 6])
            minPulseVal.append(validationLst[i + 12])
            maxPulseVal.append(validationLst[i + 10])


        valBPResult = []


        for i in range(len(bpSYSValue)):

            if (bpSYSValue[i] >= int(minSysVal[i]) and bpSYSValue[i] <= int(maxSysVal[i])
                and bpPulseValue[i] >= int(minPulseVal[i]) and bpPulseValue[i] <= int(maxPulseVal[i])
                and bpDiaValue[i] >= int(minDiaVal[i]) and bpDiaValue[i] <= int(maxDiaVal[i])):

                valBPResult.append("Pass")
                valValues.append(minSysVal[i] + '-' + maxSysVal[i] + '|' + minPulseVal[i] + '-' + maxPulseVal[i]+'|'+minDiaVal[i]+'-'+maxDiaVal[i])
                dataType.append("BP")
            else:
                valBPResult.append("Fail")
                valValues.append(minSysVal[i] + '-' + maxSysVal[i] + '|' + minPulseVal[i] + '-' + maxPulseVal[
                    i] + '|' + minDiaVal[i] + '-' + maxDiaVal[i])
                dataType.append("BP")

        for i in range(len(poSPOValue)):
            poVal.append(str(poSPOValue[i]) + '-' + str(poBPMValue[i]))

        for i in range(len(bpSYSValue)):
            bpVal.append(str(bpSYSValue[i]) + '-' + str(bpPulseValue[i]) + '-' + str(bpDiaValue[i]))

        print "Min & Max Values: ", valValues
        rpmValResult = valWeightResult + valPOResult + valBPResult
        rpmVal = rpmWeightValue + poVal + bpVal
        print "Validation Values: ", rpmVal

        df = pd.DataFrame()
        df['Datatype'] = dataType
        df['RPM Values'] = rpmVal
        df['Min-Max'] = valValues
        df['Validation Result'] = rpmValResult

        writer = pd.ExcelWriter(filePath + 'ValidationResult.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})

        worksheet.set_column('A:A', 12, format1)
        worksheet.set_column('B:B', 11, format1)
        worksheet.set_column('C:C', 21, format1)
        worksheet.set_column('D:D', 12, format1)

        writer.save()
        writer.close()

        return rpmVal, rpmValResult, valValues, dataType


    def overallWeigthResult(self,PATH_BASE, rpmWeightValue, rpmWeightTimeStamp, fdaWeighValue, fdaWeightTimeStamp,
                            comWeighValue, comWeightTimeStamp, serverWeightValue, serverweightTimeStamp):

        rpmWeightValues = []
        fdaWeightValues = []
        comWeightValues = []
        serverWeightValues = []

        for l1, l2 in zip(rpmWeightValue, rpmWeightTimeStamp):
            rpmWeightValues.append(str(l1) + '|' + l2)

        for l1, l2 in zip(fdaWeighValue, fdaWeightTimeStamp):
            fdaWeightValues.append(str(l1) + '|' + l2)

        for l1, l2 in zip(comWeighValue, comWeightTimeStamp):
            comWeightValues.append(str(l1) + '|' + l2)

        for l1, l2 in zip(serverWeightValue, serverweightTimeStamp):
            serverWeightValues.append(str(l1) + '|' + l2)

        rpmWeightValues = list(set(rpmWeightValues))
        fdaWeightValues = list(set(fdaWeightValues))
        comWeightValues = list(set(comWeightValues))
        serverWeightValues = list(set(serverWeightValues))

        comWeightLength = len(comWeightValues)
        rpmWeightLength = len(rpmWeightValues)
        fdaWeightLength = len(fdaWeightValues)
        serverWeighLength = len(serverWeightValues)
        maxWeightLength = max(rpmWeightLength, fdaWeightLength, comWeightLength, serverWeighLength)
        if rpmWeightLength == fdaWeightLength and rpmWeightLength == comWeightLength and rpmWeightLength == serverWeighLength:
            pass
        else:
            if rpmWeightLength != maxWeightLength:
                rpmDifference = maxWeightLength - rpmWeightLength
                for i in range(rpmDifference):
                    rpmWeightValues.append('0|0')
            if fdaWeightLength != maxWeightLength:
                fdaDifference = maxWeightLength - fdaWeightLength
                for i in range(fdaDifference):
                    fdaWeightValues.append('0|0')
            if comWeightLength != maxWeightLength:
                comDifference = maxWeightLength - comWeightLength
                for i in range(comDifference):
                    comWeightValues.append('0|0')
            if serverWeighLength != maxWeightLength:
                serverDifference = maxWeightLength - serverWeighLength
                for i in range(serverDifference):
                    serverWeightValues.append('0|0')

        # print rpmWeightValues
        # print len(rpmWeightValues)
        #
        # print serverWeightValues
        # print len(serverWeightValues)
        #
        # print comWeightValues
        # print len(comWeightValues)
        #
        # print fdaWeightValues
        # print len(fdaWeightValues)

        # Common values from each list
        commonrpmfdaWeight = [(i, j) for i in range(len(rpmWeightValues)) for j in range(len(fdaWeightValues)) if
                              rpmWeightValues[i] == fdaWeightValues[j]]

        commonrpmcomWeight = [(i, j) for i in range(len(rpmWeightValues)) for j in range(len(comWeightValues)) if
                              rpmWeightValues[i] == comWeightValues[j]]

        commonrpmServerWeight = [(i, j) for i in range(len(rpmWeightValues)) for j in range(len(serverWeightValues)) if
                                 rpmWeightValues[i] == serverWeightValues[j]]

        # finding only matched list
        matchrpmWeight, matchfdaWeight = [e[0] for e in commonrpmfdaWeight], [e[1] for e in commonrpmfdaWeight]

        matchcomrpmWeight, matchcomWeight = [e[0] for e in commonrpmcomWeight], [e[1] for e in commonrpmcomWeight]

        matchserverrpmWeight, matchServerWeight = [e[0] for e in commonrpmServerWeight], [e[1] for e in
                                                                                          commonrpmServerWeight]

        rpmMissingIndex = range(len(rpmWeightValues))
        fdaMissingIndex = range(len(fdaWeightValues))
        comMissingIndex = range(len(comWeightValues))
        serverMissingIndex = range(len(serverWeightValues))

        rpmMatch = set(matchrpmWeight)
        fdaMatch = set(matchfdaWeight)
        comMatch = set(matchcomWeight)
        rpmComMatch = set(matchcomrpmWeight)
        serverWeightMatch = set(matchserverrpmWeight)
        serverMatch = set(matchServerWeight)

        nonmatchRPMIndex = filter(lambda x: x not in rpmMatch, rpmMissingIndex)
        nonmatchFDAIndex = filter(lambda x: x not in fdaMatch, fdaMissingIndex)
        nonmatchCOMIndex = filter(lambda x: x not in comMatch, comMissingIndex)
        nonmatchRPMCOMIndex = filter(lambda x: x not in rpmComMatch, rpmMissingIndex)
        nonmatchrpmServerIndex = filter(lambda x: x not in serverWeightMatch, rpmMissingIndex)
        nonmatchServerIndex = filter(lambda x: x not in serverMatch, serverMissingIndex)

        nonmatchRPMIndexLength = len(nonmatchRPMIndex)
        nonmatchFDAIndexLength = len(nonmatchFDAIndex)
        nonmatchCOMIndexLength = len(nonmatchCOMIndex)

        # rpmfdanonMatchIndex = nonmatchRPMIndexLength - nonmatchFDAIndexLength
        # fdarpmMatchIndex = nonmatchFDAIndexLength + len(matchfdaWeight)
        # comrpmMatchIndex = nonmatchCOMIndexLength - nonmatchRPMIndexLength
        # comrpmnonMatchIndex = nonmatchRPMIndexLength - nonmatchCOMIndexLength
        #
        # if len(rpmWeightValues) > fdarpmMatchIndex:
        #     fdaequal = len(rpmWeightValues) - fdarpmMatchIndex
        #     del

        # if nonmatchRPMIndexLength > nonmatchFDAIndexLength:
        # 	del nonmatchRPMIndex[-rpmfdanonMatchIndex]
        # # elif nonmatchFDAIndexLength > nonmatchRPMIndexLength:
        # # 	del nonmatchFDAIndex[-fdarpmMatchIndex]
        # elif nonmatchRPMIndexLength > nonmatchCOMIndexLength:
        #     del nonmatchCOMIndex[-rpmfdanonMatchIndex]
        # elif nonmatchCOMIndexLength > nonmatchRPMIndexLength:
        #     del nonmatchCOMIndex[-comrpmnonMatchIndex]

        rpmwe = []
        comrpmwe = []
        fdawe = []
        comwe = []
        serverwe = []
        serverpmwe = []

        for i in matchcomrpmWeight:
            comrpmwe.append(rpmWeightValues[i] + '|Pass|')
        for i in nonmatchRPMCOMIndex:
            comrpmwe.append(rpmWeightValues[i] + '|Fail|')
        for i in matchrpmWeight:
            rpmwe.append(rpmWeightValues[i] + '|Pass|')
        for j in matchfdaWeight:
            fdawe.append(fdaWeightValues[j] + '|Pass|')
        for i in matchcomWeight:
            comwe.append(comWeightValues[i] + '|Pass|')
        for i in nonmatchCOMIndex:
            comwe.append(comWeightValues[i] + '|Fail|')
        for i in nonmatchRPMIndex:
            rpmwe.append(rpmWeightValues[i] + '|Fail|')
        for i in nonmatchFDAIndex:
            fdawe.append(fdaWeightValues[i] + '|Fail|')
        for i in matchServerWeight:
            serverwe.append(serverWeightValues[i] + '|Pass|')
        for i in nonmatchServerIndex:
            serverwe.append(serverWeightValues[i] + '|Fail|')
        for i in matchserverrpmWeight:
            serverpmwe.append(rpmWeightValues[i] + '|Pass|')
        for i in nonmatchrpmServerIndex:
            serverpmwe.append(rpmWeightValues[i] + '|Fail|')

        # print rpmwe
        #
        # print fdawe
        #
        # print comwe
        #
        # print serverpmwe
        #
        # print serverwe

        rpmdatatype = []
        rpmD = ' '.join(rpmwe)
        rpmval = rpmD.split("|")
        rpmval[:] = [item for item in rpmval if item != '']
        for i in range(len(rpmwe)):
            rpmdatatype.append("Weight")

        rpmweight = rpmval[::3]
        rpmtime = rpmval[1::3]
        rpmresult = rpmval[2::3]

        rpmdifference = len(rpmweight) - len(rpmWeightValues)
        if len(rpmweight) > len(rpmWeightValues):
            del rpmweight[-rpmdifference]
            del rpmtime[-rpmdifference]
            del rpmresult[-rpmdifference]
            del rpmdatatype[-rpmdifference]

        fdadatatype = []
        fdaD = ' '.join(fdawe)
        fdaval = fdaD.split("|")
        fdaval[:] = [item for item in fdaval if item != '']
        for i in range(len(fdawe)):
            fdadatatype.append("Weight")

        fdaweight = fdaval[::3]
        fdatime = fdaval[1::3]
        fdaresult = fdaval[2::3]

        comdatatype = []
        comD = ' '.join(comwe)
        comval = comD.split("|")
        comval[:] = [item for item in comval if item != '']
        for i in range(len(comwe)):
            comdatatype.append("Weight")

        comweight = comval[::3]
        comtime = comval[1::3]
        comresult = comval[2::3]

        comrpmdatatype = []
        comrpmD = ' '.join(comrpmwe)
        comrpmval = comrpmD.split("|")
        comrpmval[:] = [item for item in comrpmval if item != '']
        for i in range(len(comrpmwe)):
            comrpmdatatype.append("Weight")

        comrpmweight = comrpmval[::3]
        comrpmtime = comrpmval[1::3]
        comrpmresult = comrpmval[2::3]

        serverpmdatatype = []
        serverrpmD = ' '.join(serverpmwe)
        serverrpmval = serverrpmD.split("|")
        serverrpmval[:] = [item for item in serverrpmval if item != '']
        for i in range(len(serverpmwe)):
            serverpmdatatype.append("Weight")

        serverrpmweight = serverrpmval[::3]
        serverrpmtime = serverrpmval[1::3]
        serverrpmresult = serverrpmval[2::3]

        serverdatatype = []
        serverD = ' '.join(serverwe)
        serverval = serverD.split("|")
        serverval[:] = [item for item in serverval if item != '']
        for i in range(len(serverwe)):
            serverdatatype.append("Weight")

        serverweight = serverval[::3]
        servertime = serverval[1::3]
        serverresult = serverval[2::3]

        df = pd.DataFrame()

        df['Data type'] = rpmdatatype
        df['RPM Val'] = rpmweight
        df['RPM Timestamp'] = rpmtime
        df['FDA Val'] = fdaweight
        df['FDA Timestamp'] = fdatime
        df['FDA Result'] = fdaresult
        df['Com. Val'] = comweight
        df['Com. Timestamp'] = comtime
        df['RPM--Com.Val'] = comrpmweight
        df['RPM--ComTimestamp'] = comrpmtime
        df['Com. Result'] = comrpmresult
        df['Server Val'] = serverweight
        df['Server Timestamp'] = servertime
        df['RPM--Server Val'] = serverrpmweight
        df['RPM--ServerTimestamp'] = serverrpmtime
        df['Server Result'] = serverresult
        df.style.set_properties(**{'text-align': 'right'})
        df1 = df.sort_values(by='Server Timestamp', ascending=1)
        writer = pd.ExcelWriter(PATH_BASE+'WeightResult.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        writer.save()
        writer.close()

        return rpmdatatype, rpmweight, rpmtime, fdaweight, fdatime, fdaresult, comweight, comtime, comrpmweight, comrpmtime,
        comrpmresult, serverweight, servertime, serverrpmweight, serverrpmtime, serverresult

    def overallPOResult(self, PATH_BASE, POBPM, POSPO, POTimestamp, FDAPOBPM,
                        FDAPOSPO, FDAPOTimestamp, COMPOBPM,
                        COMPOSPO, COMPOTimestamp, SERVERPOBPM,
                        SERVERPOSPO, SERVERPOTimestamp):

        rpmPOValues = []
        fdaPOValues = []
        comPOValues = []
        serverPOValues = []

        for l1, l2, l3 in zip(POBPM, POSPO, POTimestamp):
            rpmPOValues.append(str(l1) + '/' + str(l2) + '|' + l3)

        for l1, l2, l3 in zip(FDAPOBPM, FDAPOSPO, FDAPOTimestamp):
            fdaPOValues.append(str(l1) + '/' + str(l2) + '|' + l3)

        for l1, l2, l3 in zip(COMPOBPM, COMPOSPO, COMPOTimestamp):
            comPOValues.append(str(l1) + '/' + str(l2) + '|' + l3)

        for l1, l2, l3 in zip(SERVERPOBPM, SERVERPOSPO, SERVERPOTimestamp):
            serverPOValues.append(str(l1) + '/' + str(l2) + '|' + l3)

        rpmPOValues = list(set(rpmPOValues))
        fdaPOValues = list(set(fdaPOValues))
        comPOValues = list(set(comPOValues))
        serverPOValues = list(set(serverPOValues))

        rpmPOLength = len(rpmPOValues)
        fdaPOLength = len(fdaPOValues)
        comPOLength = len(comPOValues)
        serverPOLength = len(serverPOValues)

        maxPOLength = max(rpmPOLength, fdaPOLength, comPOLength, serverPOLength)
        if rpmPOLength == fdaPOLength and rpmPOLength == comPOLength and rpmPOLength == serverPOLength:
            pass
        else:
            if rpmPOLength != maxPOLength:
                rpmDifference = maxPOLength - rpmPOLength
                for i in range(rpmDifference):
                    rpmPOValues.append('0|0')
            if fdaPOLength != maxPOLength:
                fdaDifference = maxPOLength - fdaPOLength
                for i in range(fdaDifference):
                    fdaPOValues.append('0|0')
            if comPOLength != maxPOLength:
                comDifference = maxPOLength - comPOLength
                for i in range(comDifference):
                    comPOValues.append('0|0')
            if serverPOLength != maxPOLength:
                serverDifference = maxPOLength - serverPOLength
                for i in range(serverDifference):
                    serverPOValues.append('0|0')

        # print rpmPOValues
        # print len(rpmPOValues)
        #
        # print fdaPOValues
        # print len(fdaPOValues)

        commonrpmfdaPO = [(i, j) for i in range(len(rpmPOValues)) for j in range(len(fdaPOValues)) if
                          rpmPOValues[i] == fdaPOValues[j]]

        commonrpmcomPO = [(i, j) for i in range(len(rpmPOValues)) for j in range(len(comPOValues)) if
                          rpmPOValues[i] == comPOValues[j]]

        commonrpmserverPO = [(i, j) for i in range(len(rpmPOValues)) for j in range(len(serverPOValues)) if
                             rpmPOValues[i] == serverPOValues[j]]

        matchrpmPO, matchfdaPO = [e[0] for e in commonrpmfdaPO], [e[1] for e in commonrpmfdaPO]

        matchrpmcomPO, matchcomPO = [e[0] for e in commonrpmcomPO], [e[1] for e in commonrpmcomPO]
        matchrpmserverPO, matchserverPO = [e[0] for e in commonrpmserverPO], [e[1] for e in commonrpmserverPO]

        rpmMissingIndex = range(len(rpmPOValues))
        fdaMissingIndex = range(len(fdaPOValues))
        comMissingIndex = range(len(comPOValues))
        serverMissingIndex = range(len(serverPOValues))

        rpmMatch = set(matchrpmPO)
        fdaMatch = set(matchfdaPO)
        comMatch = set(matchcomPO)
        rpmComMatch = set(matchrpmcomPO)
        rpmserverMatch = set(matchrpmserverPO)
        serverMatch = set(matchserverPO)

        nonmatchRPMIndex = filter(lambda x: x not in rpmMatch, rpmMissingIndex)
        nonmatchFDAIndex = filter(lambda x: x not in fdaMatch, fdaMissingIndex)
        nonmatchCOMIndex = filter(lambda x: x not in comMatch, comMissingIndex)
        nonmatchRPMCOMIndex = filter(lambda x: x not in rpmComMatch, rpmMissingIndex)
        nonmatchrpmServerIndex = filter(lambda x: x not in rpmserverMatch, rpmMissingIndex)
        nonmatchServerIndex = filter(lambda x: x not in serverMatch, serverMissingIndex)

        nonmatchRPMIndexLength = len(nonmatchRPMIndex)
        nonmatchFDAIndexLength = len(nonmatchFDAIndex)
        nonmatchCOMIndexLength = len(nonmatchCOMIndex)

        rpmpo = []
        fdapo = []
        compo = []
        rpmcompo = []
        serverpo = []
        rpmserverpo = []

        for i in matchrpmPO:
            rpmpo.append(rpmPOValues[i] + '|Pass|')
        for j in matchfdaPO:
            fdapo.append(fdaPOValues[j] + '|Pass|')
        for i in nonmatchRPMIndex:
            rpmpo.append(rpmPOValues[i] + '|Fail|')
        for i in nonmatchFDAIndex:
            fdapo.append(fdaPOValues[i] + '|Fail|')
        for i in matchrpmcomPO:
            rpmcompo.append(rpmPOValues[i] + '|Pass|')
        for i in nonmatchRPMCOMIndex:
            rpmcompo.append(rpmPOValues[i] + '|Fail|')
        for i in matchcomPO:
            compo.append(comPOValues[i] + '|Pass|')
        for i in nonmatchCOMIndex:
            compo.append(comPOValues[i] + '|Fail|')
        for i in matchrpmserverPO:
            rpmserverpo.append(rpmPOValues[i] + '|Pass|')
        for i in nonmatchrpmServerIndex:
            rpmserverpo.append(rpmPOValues[i] + '|Fail|')
        for i in matchserverPO:
            serverpo.append(serverPOValues[i] + '|Pass|')
        for i in nonmatchServerIndex:
            serverpo.append(serverPOValues[i] + '|Fail|')
        #
        # print rpmpo
        #
        # print fdapo

        rpmdatatype = []
        rpmD = ' '.join(rpmpo)
        rpmval = rpmD.split("|")
        rpmval[:] = [item for item in rpmval if item != '']
        for i in range(len(rpmpo)):
            rpmdatatype.append("PO")

        rpmpoVal = rpmval[::3]
        rpmtime = rpmval[1::3]
        rpmresult = rpmval[2::3]

        fdadatatype = []
        fdaD = ' '.join(fdapo)
        fdaval = fdaD.split("|")
        fdaval[:] = [item for item in fdaval if item != '']
        for i in range(len(fdapo)):
            fdadatatype.append("PO")

        fdapoVal = fdaval[::3]
        fdatime = fdaval[1::3]
        fdaresult = fdaval[2::3]

        comdatatype = []
        comD = ' '.join(compo)
        comval = comD.split("|")
        comval[:] = [item for item in comval if item != '']
        for i in range(len(compo)):
            comdatatype.append("PO")

        comPOVal = comval[::3]
        comtime = comval[1::3]
        comresult = comval[2::3]

        rpmcomdatatype = []
        rpmcomD = ' '.join(rpmcompo)
        rpmcomval = rpmcomD.split("|")
        rpmcomval[:] = [item for item in rpmcomval if item != '']
        for i in range(len(rpmcompo)):
            comdatatype.append("PO")

        rpmcomPOVal = rpmcomval[::3]
        rpmcomtime = rpmcomval[1::3]
        rpmcomresult = rpmcomval[2::3]

        rpmserverdatatype = []
        rpmserverD = ' '.join(rpmserverpo)
        rpmserverval = rpmserverD.split("|")
        rpmserverval[:] = [item for item in rpmserverval if item != '']
        for i in range(len(rpmserverpo)):
            rpmserverdatatype.append("PO")

        rpmserverPOVal = rpmserverval[::3]
        rpmservertime = rpmserverval[1::3]
        rpmserverresult = rpmserverval[2::3]

        serverdatatype = []
        serverD = ' '.join(serverpo)
        serverval = serverD.split("|")
        serverval[:] = [item for item in serverval if item != '']
        for i in range(len(serverpo)):
            serverdatatype.append("PO")

        serverPOVal = serverval[::3]
        servertime = serverval[1::3]
        serverresult = serverval[2::3]

        df = pd.DataFrame()

        df['Data type'] = rpmdatatype
        df['RPM Val'] = rpmpoVal
        df['RPM Timestamp'] = rpmtime
        df['FDA Val'] = fdapoVal
        df['FDA Timestamp'] = fdatime
        df['FDA Result'] = fdaresult
        df['Com. Val'] = comPOVal
        df['Com. Timestamp'] = comtime
        df['RPM--Com.Val'] = rpmcomPOVal
        df['RPM--ComTimestamp'] = rpmcomtime
        df['Com. Result'] = rpmcomresult
        df['Server Val'] = serverPOVal
        df['Server Timestamp'] = servertime
        df['RPM--Server Val'] = rpmserverPOVal
        df['RPM--ServerTimestamp'] = rpmservertime
        df['Server Result'] = rpmserverresult

        df.style.set_properties(**{'text-align': 'right'})
        df1 = df.sort_values(by='FDA Timestamp', ascending=1)
        writer = pd.ExcelWriter(PATH_BASE+'POResult.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        writer.save()
        writer.close()

    def overallBPResult(self, PATH_BASE, BPSYSValue, BPPulseValue, BPDiaValue, BPTimeStamp,
                        FDABPSYSValue, FDABPPulseValue, FDABPDiaValue,
                        FDABPTimeStamp, ComBPSYSValue, ComBPPulseValue,
                        ComBPDiaValue, ComBPTimeStamp, ServerBPSYSValue, ServerBPPulseValue,
                        ServerBPDiaValue, ServerBPTimeStamp):

        rpmBPValues = []
        fdaBPValues = []
        comBPValues = []
        serverBPValues = []

        for l1, l2, l3, l4 in zip(BPSYSValue, BPPulseValue, BPDiaValue, BPTimeStamp):
            rpmBPValues.append(str(l1) + '/' + str(l2) + '/' + str(l3) + '|' + l4)

        for l1, l2, l3, l4 in zip(FDABPSYSValue, FDABPPulseValue, FDABPDiaValue, FDABPTimeStamp):
            fdaBPValues.append(str(l1) + '/' + str(l2) + '/' + str(l3) + '|' + l4)

        for l1, l2, l3, l4 in zip(ComBPSYSValue, ComBPPulseValue, ComBPDiaValue, ComBPTimeStamp):
            comBPValues.append(str(l1) + '/' + str(l2) + '/' + str(l3) + '|' + l4)

        for l1, l2, l3, l4 in zip(ServerBPSYSValue, ServerBPPulseValue, ServerBPDiaValue, ServerBPTimeStamp):
            serverBPValues.append(str(l1) + '/' + str(l2) + '/' + str(l3) + '|' + l4)

        rpmBPValues = list(set(rpmBPValues))
        fdaBPValues = list(set(fdaBPValues))
        comBPValues = list(set(comBPValues))
        serverBPValues = list(set(serverBPValues))

        rpmBPLength = len(rpmBPValues)
        fdaBPLength = len(fdaBPValues)
        comBPLength = len(comBPValues)
        serverBPLength = len(serverBPValues)

        maxBPLength = max(rpmBPLength, fdaBPLength, comBPLength, serverBPLength)
        if rpmBPLength == fdaBPLength and rpmBPLength == comBPLength and rpmBPLength == serverBPLength:
            pass
        else:
            if rpmBPLength != maxBPLength:
                rpmDifference = maxBPLength - rpmBPLength
                for i in range(rpmDifference):
                    rpmBPValues.append('0|0')
            if fdaBPLength != maxBPLength:
                fdaDifference = maxBPLength - fdaBPLength
                for i in range(fdaDifference):
                    fdaBPValues.append('0|0')
            if comBPLength != maxBPLength:
                comDifference = maxBPLength - comBPLength
                for i in range(comDifference):
                    comBPValues.append('0|0')
            if serverBPLength != maxBPLength:
                serverDifference = maxBPLength - serverBPLength
                for i in range(serverDifference):
                    serverBPValues.append('0|0')

        # print rpmBPValues
        # print len(rpmBPValues)
        #
        # print fdaBPValues
        # print len(fdaBPValues)

        commonrpmfdaBP = [(i, j) for i in range(len(rpmBPValues)) for j in range(len(fdaBPValues)) if
                          rpmBPValues[i] == fdaBPValues[j]]

        commonrpmcomBP = [(i, j) for i in range(len(rpmBPValues)) for j in range(len(comBPValues)) if
                          rpmBPValues[i] == comBPValues[j]]

        commonrpmserverBP = [(i, j) for i in range(len(rpmBPValues)) for j in range(len(serverBPValues)) if
                             rpmBPValues[i] == serverBPValues[j]]

        matchrpmBP, matchfdaBP = [e[0] for e in commonrpmfdaBP], [e[1] for e in commonrpmfdaBP]

        matchrpmcomBP, matchcomBP = [e[0] for e in commonrpmcomBP], [e[1] for e in commonrpmcomBP]
        matchrpmserverBP, matchserverBP = [e[0] for e in commonrpmserverBP], [e[1] for e in commonrpmserverBP]

        rpmMissingIndex = range(len(rpmBPValues))
        fdaMissingIndex = range(len(fdaBPValues))
        comMissingIndex = range(len(comBPValues))
        serverMissingIndex = range(len(serverBPValues))

        rpmMatch = set(matchrpmBP)
        fdaMatch = set(matchfdaBP)
        comMatch = set(matchcomBP)
        rpmComMatch = set(matchrpmcomBP)
        rpmserverMatch = set(matchrpmserverBP)
        serverMatch = set(matchserverBP)

        nonmatchRPMIndex = filter(lambda x: x not in rpmMatch, rpmMissingIndex)
        nonmatchFDAIndex = filter(lambda x: x not in fdaMatch, fdaMissingIndex)
        nonmatchCOMIndex = filter(lambda x: x not in comMatch, comMissingIndex)
        nonmatchRPMCOMIndex = filter(lambda x: x not in rpmComMatch, rpmMissingIndex)
        nonmatchrpmServerIndex = filter(lambda x: x not in rpmserverMatch, rpmMissingIndex)
        nonmatchServerIndex = filter(lambda x: x not in serverMatch, serverMissingIndex)

        nonmatchRPMIndexLength = len(nonmatchRPMIndex)
        nonmatchFDAIndexLength = len(nonmatchFDAIndex)
        nonmatchCOMIndexLength = len(nonmatchCOMIndex)

        rpmbp = []
        fdabp = []
        combp = []
        rpmcombp = []
        serverbp = []
        rpmserverbp = []

        for i in matchrpmBP:
            rpmbp.append(rpmBPValues[i] + '|Pass|')
        for j in matchfdaBP:
            fdabp.append(fdaBPValues[j] + '|Pass|')
        for i in nonmatchRPMIndex:
            rpmbp.append(rpmBPValues[i] + '|Fail|')
        for i in nonmatchFDAIndex:
            fdabp.append(fdaBPValues[i] + '|Fail|')
        for i in matchrpmcomBP:
            rpmcombp.append(rpmBPValues[i] + '|Pass|')
        for i in nonmatchRPMCOMIndex:
            rpmcombp.append(rpmBPValues[i] + '|Fail|')
        for i in matchcomBP:
            combp.append(comBPValues[i] + '|Pass|')
        for i in nonmatchCOMIndex:
            combp.append(comBPValues[i] + '|Fail|')
        for i in matchrpmserverBP:
            rpmserverbp.append(rpmBPValues[i] + '|Pass|')
        for i in nonmatchrpmServerIndex:
            rpmserverbp.append(rpmBPValues[i] + '|Fail|')
        for i in matchserverBP:
            serverbp.append(serverBPValues[i] + '|Pass|')
        for i in nonmatchServerIndex:
            serverbp.append(serverBPValues[i] + '|Fail|')

        rpmdatatype = []
        rpmD = ' '.join(rpmbp)
        rpmval = rpmD.split("|")
        rpmval[:] = [item for item in rpmval if item != '']
        for i in range(len(rpmbp)):
            rpmdatatype.append("BP")

        rpmbpVal = rpmval[::3]
        rpmtime = rpmval[1::3]
        rpmresult = rpmval[2::3]

        fdadatatype = []
        fdaD = ' '.join(fdabp)
        fdaval = fdaD.split("|")
        fdaval[:] = [item for item in fdaval if item != '']
        for i in range(len(fdabp)):
            fdadatatype.append("BP")

        fdabpVal = fdaval[::3]
        fdatime = fdaval[1::3]
        fdaresult = fdaval[2::3]

        comdatatype = []
        comD = ' '.join(combp)
        comval = comD.split("|")
        comval[:] = [item for item in comval if item != '']
        for i in range(len(combp)):
            comdatatype.append("BP")

        comBPVal = comval[::3]
        comtime = comval[1::3]
        comresult = comval[2::3]

        rpmcomdatatype = []
        rpmcomD = ' '.join(rpmcombp)
        rpmcomval = rpmcomD.split("|")
        rpmcomval[:] = [item for item in rpmcomval if item != '']
        for i in range(len(rpmcombp)):
            comdatatype.append("BP")

        rpmcomBPVal = rpmcomval[::3]
        rpmcomtime = rpmcomval[1::3]
        rpmcomresult = rpmcomval[2::3]

        rpmserverdatatype = []
        rpmserverD = ' '.join(rpmserverbp)
        rpmserverval = rpmserverD.split("|")
        rpmserverval[:] = [item for item in rpmserverval if item != '']
        for i in range(len(rpmserverbp)):
            rpmserverdatatype.append("BP")

        rpmserverBPVal = rpmserverval[::3]
        rpmservertime = rpmserverval[1::3]
        rpmserverresult = rpmserverval[2::3]

        serverdatatype = []
        serverD = ' '.join(serverbp)
        serverval = serverD.split("|")
        serverval[:] = [item for item in serverval if item != '']
        for i in range(len(serverbp)):
            serverdatatype.append("BP")

        serverBPVal = serverval[::3]
        servertime = serverval[1::3]
        serverresult = serverval[2::3]

        df = pd.DataFrame()

        df['Data type'] = rpmdatatype
        df['RPM Val'] = rpmbpVal
        df['RPM Timestamp'] = rpmtime
        df['FDA Val'] = fdabpVal
        df['FDA Timestamp'] = fdatime
        df['FDA Result'] = fdaresult
        df['Com. Val'] = comBPVal
        df['Com. Timestamp'] = comtime
        df['RPM--Com.Val'] = rpmcomBPVal
        df['RPM--ComTimestamp'] = rpmcomtime
        df['Com. Result'] = rpmcomresult
        df['Server Val'] = serverBPVal
        df['Server Timestamp'] = servertime
        df['RPM--Server Val'] = rpmserverBPVal
        df['RPM--ServerTimestamp'] = rpmservertime
        df['Server Result'] = rpmserverresult

        df.style.set_properties(**{'text-align': 'right'})
        df1 = df.sort_values(by='FDA Timestamp', ascending=1)
        writer = pd.ExcelWriter(PATH_BASE+'BPResult.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        writer.save()
        writer.close()