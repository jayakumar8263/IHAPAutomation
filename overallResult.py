from austonioLibraries import fdaDBLogOperation
from austonioLibraries import commLogOperation
from austonioLibraries import rpmLogOperation
import pandas as pd
from austonioLibraries import serverOperation

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

    def executionResult(self,PATH_BASE, rpmList, fdaList, comList, serverList):
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


        if len(rpmWeightValue) == len(fdaWeighValue) and len(rpmWeightValue) == len(comWeighValue):

            for i in range(len(rpmWeightValue)):
                DATATYPE.append("Weight")
                RPMVALUES.append(rpmWeightValue[i])
                RPMTIMESTAMP.append(weightTimeStamp[i])
                FDAVALUES.append(fdaWeighValue[i])
                FDATIMESTAMP.append(fdaWeightTimeStamp[i])
                COMVALUES.append(comWeighValue[i])
                COMTIMESTAMP.append(comWeightTimeStamp[i])
                SERVERDATATYPE.append("Weight")
                SERVERVALUES.append(serverWeightValue[i])
                SERVERTIMESTAMP.append(serverweightTimeStamp[i])
                PASSNFAIL.append("Pass")

        else:
            print "Length is not matching"

        if len(poBPMValue) == len(fdapoBPMValue) and len(poBPMValue) == len(compoBPMValue):
            print len(comWeightTimeStamp)
            print len(compoBPMValue)
            for i in range(len(poBPMValue)):
                DATATYPE.append("PO")
                RPMVALUES.append(str(poBPMValue[i])+'/'+str(poSPOValue[i]))
                RPMTIMESTAMP.append(poTimeStamp[i])
                FDAVALUES.append(str(fdapoBPMValue[i])+'/'+str(fdapoSPOValue[i]))
                FDATIMESTAMP.append(fdapoTimeStamp[i])
                COMVALUES.append(str(compoBPMValue[i])+'/'+str(compoSPOValue[i]))
                COMTIMESTAMP.append(compoTimeStamp[i])
                SERVERDATATYPE.append("PO")
                SERVERVALUES.append(str(serverpoBPMValue[i])+'/'+str(serverpoSPOValue[i]))
                SERVERTIMESTAMP.append(serverpoTimeStamp[i])
                PASSNFAIL.append("Fail")


        if len(bpSYSValue) == len(fdabpSystolicValue) and len(bpSYSValue) == len(combpSystolicValue):

            for i in range(len(bpSYSValue)):
                DATATYPE.append("BP")
                RPMVALUES.append(str(bpSYSValue[i]) + '/' + str(bpPulseValue[i])+'/'+str(bpDiaValue[i]))
                RPMTIMESTAMP.append(bpTimeStamp[i])
                FDAVALUES.append(str(fdabpSystolicValue[i]) + '/' + str(fdabpPulseValue[i])+'/'+str(fdabpDiastolicValue[i]))
                FDATIMESTAMP.append(fdabpTimeStamp[i])
                COMVALUES.append(str(combpSystolicValue[i])+'/'+str(combpPulseValue[i])+'/'+str(combpDiastolicValue[i]))
                COMTIMESTAMP.append(combpTimeStamp[i])
                SERVERDATATYPE.append("BP")
                SERVERVALUES.append(str(serverbpSYSValue[i])+'/'+str(serverbpPulseValue[i])+'/'+str(serverbpDiaValue[i]))
                SERVERTIMESTAMP.append(serverbpTimeStamp[i])
                PASSNFAIL.append("Pass")

        print "DATA: ", DATATYPE
        print "RPM Values: ", RPMVALUES
        print "RPM TimeStamp: ", RPMTIMESTAMP
        print "FDA: ", FDAVALUES
        print "FDA TimeStamp:", FDATIMESTAMP
        print "Com Values: ", COMVALUES
        print "Com TimeStamp:", COMTIMESTAMP
        print "Server Data Type: ", SERVERDATATYPE
        print "Server Values: ", SERVERVALUES
        print "Server TimeStamp: ", SERVERTIMESTAMP

        print "DATA: ", len(DATATYPE)
        print "RPM Values: ", len(RPMVALUES)
        print "RPM TimeStamp: ", len(RPMTIMESTAMP)
        print "FDA: ", len(FDAVALUES)
        print "FDA TimeStamp:", len(FDATIMESTAMP)
        print "Com Values: ", len(COMVALUES)
        print "Com TimeStamp:", len(COMTIMESTAMP)
        print "Server Data Type: ", len(SERVERDATATYPE)
        print "Server Values: ", len(SERVERVALUES)
        print "Server TimeStamp: ", len(SERVERTIMESTAMP)

        df = pd.DataFrame()
        df2 = pd.DataFrame()
        df['Data Type'] = DATATYPE
        df['RPM Values'] = RPMVALUES
        df['RPM TimeStamp'] = RPMTIMESTAMP
        df['FDA Values'] = FDAVALUES
        df['FDA TimeStamp'] = FDATIMESTAMP
        df['Com. Values'] = COMVALUES
        df['Com. TimeStamp'] = COMTIMESTAMP
        df['Server Data Type'] = SERVERDATATYPE
        df['Server Value'] = SERVERVALUES
        df['Server TimeStamp'] = SERVERTIMESTAMP
        df['Result'] = PASSNFAIL
        df2['Summary'] = ['Total','Pass','Fail']
        countList = [str(len(DATATYPE)),str(PASSNFAIL.count("Pass")),str(PASSNFAIL.count("Fail"))]
        df2['Count'] = countList
        df.style.set_properties(**{'text-align': 'right'})
        df1 = df.sort_values(by='RPM TimeStamp', ascending=1)
        # df.sort('RPM TimeStamp')
        writer = pd.ExcelWriter(PATH_BASE + 'FinalResult.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Report', index=False)
        df2.to_excel(writer, sheet_name='Report', startcol=12, startrow=4, index=False)

        workbook = writer.book
        worksheet = writer.sheets['Report']
        format1 = workbook.add_format()
        format2 = workbook.add_format({'bg_color': '#88DD99', 'font_color': '#006100'})
        format3 = workbook.add_format({'bg_color': '#FF99A5', 'bold': True, 'font_color': '#9C0006'})

        format1.set_align('left')
        # format1.set_align('vcenter')
        l = str(len(PASSNFAIL)+1)
        worksheet.conditional_format('K1:K'+l, {'type': 'text',
                                               'criteria': 'containing',
                                               'value': 'Pass',
                                               'format': format2})
        worksheet.conditional_format('K1:K'+l, {'type': 'text',
                                                 'criteria': 'containing',
                                                 'value': 'Fail',
                                                 'format': format3})
        # worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})
        worksheet.set_column('A:A', 12, format1)
        worksheet.set_column('B:B', 13, format1)
        worksheet.set_column('C:C', 18, format1)
        worksheet.set_column('D:D', 13, format1)
        worksheet.set_column('E:E', 18, format1)
        worksheet.set_column('F:F', 13, format1)
        worksheet.set_column('G:G', 18, format1)
        worksheet.set_column('H:H', 19, format1)
        worksheet.set_column('I:I', 15, format1)
        worksheet.set_column('J:J', 17, format1)
        worksheet.set_column('K:K', 12, format1)
        worksheet.set_column('M:M', 14, format1)
        worksheet.set_column('N:N', 14, format1)

        writer.save()
        writer.close()