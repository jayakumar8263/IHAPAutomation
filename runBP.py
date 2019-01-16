import logPharser
import Search
import Config
import ast
import pandas as pd
import serverOperation
import validationPharser
class runBP(object):
    def __init__(self):
        pass

    def executeBP(self,  rawLogs , serverData, medicalDevices, definitionFiles, devicesRunning, PATH_BASE, count):
        logPharserObj = logPharser.logPharser()
        searchObj = Search.logSearch()

        bpDefFile = open(definitionFiles, 'r').read()
        serlst = []
        srvLst = logPharserObj.extractDictofServerDict(serverData)

        for i in range(len(srvLst)):
            l = dict((k, str(v)) for k, v in ast.literal_eval(srvLst[i]).iteritems())
            if l.has_key(Config.rpmDate):

                serlst.append(l[Config.rpmDate])
        fdaBPDefinition = logPharserObj.extractDic(bpDefFile, extractCommunicationTemplate=False,
                                                   extractFDATemplate=True)
        comBPDefinition = logPharserObj.extractDic(bpDefFile, extractCommunicationTemplate=True,
                                                   extractFDATemplate=False)
        print "FDA DEFINITION", fdaBPDefinition
        print "COM DEFINITION", comBPDefinition

        matchingFDABPTemplate, matchingComBPTemplate = logPharserObj.matchDictTemplate(fdaBPDefinition, comBPDefinition)

        print "FDA TEMPLATE", matchingFDABPTemplate
        print "COM TEMPLATE", matchingComBPTemplate

        rpmBPList = searchObj.keywordSearch(rawLogs, *Config.RPMKEYS)
        fdaBPList = searchObj.keywordSearch(rawLogs, *Config.FDAKEYS)
        comBPList = searchObj.keywordSearch(rawLogs, *Config.COMMUNICATIONKEYS)
        #valList = searchObj.keywordSearch(rawLogs, *Config.VALIDATIONKEYS[count])
        rpmValList = searchObj.keywordSearch(rawLogs, *Config.RPMVALIDATIONKEYS[count])
        rpmBPStr = '\n'.join(rpmBPList)
        fdaBPStr = '\n'.join(fdaBPList)
        comBPStr = '\n'.join(comBPList)
        #valStr = '\n'.join(valList)
        rpmValStr = '\n'.join(rpmValList)
        #print valStr
        print rpmValStr

        rpmBPLst = logPharserObj.extractDic(rpmBPStr)

        fdaBPLst = logPharserObj.extractDic(fdaBPStr, False, False)


        comBPTempLst = logPharserObj.extractDic(comBPStr)
        comBPLst = logPharserObj.extractDictofDict(comBPTempLst)
        print "RPM Dict", rpmBPLst
        print "COMP DICT", comBPLst
        print "FDA DICT", fdaBPLst

        # srvLst = logPharserObj.extractDictofDict(serlst)
        print "SERVER DICT", srvLst

        rpmBPValues = logPharserObj.checkformat(matchingFDABPTemplate, rpmBPLst, medicalDevices[0])
        fdaBPValues = logPharserObj.checkformat(matchingFDABPTemplate, fdaBPLst, medicalDevices[0])
        comBPValues = logPharserObj.checkformat(matchingComBPTemplate, comBPLst, medicalDevices[0])
        serverBPValues = logPharserObj.checkformat(matchingComBPTemplate, srvLst, medicalDevices[0])

        print "RPM VALUES", rpmBPValues
        print "FDA VALUES", fdaBPValues
        print "COM VALUES", comBPValues
        print "SERVER VALUES", serverBPValues


        rpmBPTmpVal = []
        fdaBPTmpVal = []
        comBPTmpVal = []
        serverBPTmpVal = []
        for i in range(len(rpmBPValues)):
            dict1 = dict(rpmBPValues[i])

            if dict1.has_key(medicalDevices[0]):
                rpmBPTmpVal.append(dict1.copy())
        for i in range(len(fdaBPValues)):
            dict1 = dict(fdaBPValues[i])

            if dict1.has_key(medicalDevices[0]):
                fdaBPTmpVal.append(dict1.copy())

        for i in range(len(comBPValues)):
            dict1 = dict(comBPValues[i])

            if dict1.has_key(medicalDevices[0]):
                comBPTmpVal.append(dict1.copy())

        for i in range(len(serverBPValues)):
            dict1 = dict(serverBPValues[i])

            if dict1.has_key(medicalDevices[0]):
                serverBPTmpVal.append(dict1.copy())


        rpmFinalBP = logPharserObj.removeDuplicate(rpmBPTmpVal)
        fdaFinalBP = logPharserObj.removeDuplicate(fdaBPTmpVal)
        comFinalBP = logPharserObj.removeDuplicate(comBPTmpVal)
        serverFinalBP = logPharserObj.removeDuplicate(serverBPTmpVal)

        print "RPM FINAL", rpmFinalBP
        print "FDA FINAL", fdaFinalBP
        print "COM FINAL", comFinalBP
        print "SERVER FINAL", serverFinalBP

        BPRPM, BPFDA = logPharserObj.matchListEqual(rpmFinalBP, fdaFinalBP, matchingFDABPTemplate,
                                                matchingComBPTemplate)

        print "MATCHED RPM", BPRPM
        print "MATCHED FDA", BPFDA

        BPFDACOM, BPCOM = logPharserObj.matchListEqual(BPFDA, comFinalBP, matchingFDABPTemplate,
                                                    matchingComBPTemplate)

        # BPFDACOM, BPCOM = logPharserObj.matchListEqual(rpmFinalBP, comFinalBP, matchingFDABPTemplate,
        #                                                matchingComBPTemplate)

        print "FDACOM", BPFDACOM
        print "BPCOM", BPCOM

        BPSERVERCOM, BPSERVER = logPharserObj.matchListEqual(BPCOM, serverFinalBP, matchingFDABPTemplate,
                                                     matchingComBPTemplate)

        # BPSERVERCOM, BPSERVER = logPharserObj.matchListEqual(rpmFinalBP, serverFinalBP, matchingFDABPTemplate,
        #                                                      matchingComBPTemplate)

        print "BPSERVERCOM", BPSERVERCOM
        print "BPSERVER", BPSERVER

        rpmBPMatched, rpmBPNonMatched = logPharserObj.matchValues(BPRPM, BPFDACOM, Config.rpmDate)

        print "rpmBPMatched", rpmBPMatched
        print "rpmBPNonMatched", rpmBPNonMatched

        fdaBPMatched, fdaBPNonMatched = logPharserObj.matchValues(BPFDACOM, BPRPM, Config.rpmDate)

        print "fdaBPMatched", fdaBPMatched
        print "fdaBPNonMatched", fdaBPNonMatched
        fdacomBPMatched, fdacomBPNonMatched = logPharserObj.matchValues(BPFDACOM, BPCOM, Config.rpmDate)

        comBPMatched, comBPNonMatched = logPharserObj.matchValues(BPCOM, BPFDACOM, Config.rpmDate)
        print "comBPMatched", comBPMatched
        print "comBPNonMatched", comBPNonMatched

        serverBPMatched, serverBPNonMatched = logPharserObj.matchValues(BPSERVER, BPRPM, Config.rpmDate)
        print "serverBPMatched", serverBPMatched
        print "serverBPNonMatched", serverBPNonMatched

        serverRPMBPMatched, serverRPMBPNonMatched = logPharserObj.matchValues(BPRPM,BPSERVER, Config.rpmDate)
        print "serverRPMBPMatched", serverRPMBPMatched
        print "serverRPMBPNonMatched", serverRPMBPNonMatched

        rpmBPPass = logPharserObj.extractPassData(medicalDevices, rpmBPMatched)
        print "rpmBPPass", rpmBPPass

        fdaBPPass = logPharserObj.extractPassData(medicalDevices, fdaBPMatched)
        print "fdaBPPass", fdaBPPass

        # fdaBPPass = logPharserObj.extractPassData(Config.BP, fdacomBPMatched)
        comBPPass = logPharserObj.extractPassData(medicalDevices, comBPMatched)
        print "comBPPass", comBPPass

        serverBPPass = logPharserObj.extractPassData(medicalDevices, serverBPMatched)
        rpmServerPass = logPharserObj.extractPassData(medicalDevices, serverRPMBPMatched)
        BPpasscount = logPharserObj.addData('Pass', fdaBPPass)
        BPfailcount = logPharserObj.addData('Fail', fdaBPNonMatched)
        Serverpasscount = logPharserObj.addData('Pass', rpmServerPass)
        Serverfailcount = logPharserObj.addData('Fail', serverBPNonMatched)
        dataType = logPharserObj.addData(devicesRunning, BPpasscount)
        dataType1 = logPharserObj.addData(devicesRunning, BPfailcount)

        fdaBPNonMatchedFinal = list(str(fdaBPNonMatched[i]) for i in range(len(fdaBPNonMatched)))


        comBPNonMatchedFinal = list(str(comBPNonMatched[i]) for i in range(len(comBPNonMatched)))

        print len(serverBPPass)
        print len(Serverfailcount)
        print len(BPpasscount)
        print len(BPfailcount)
        print len(comBPPass)
        print len(fdaBPPass)
        print len(rpmBPPass)
        print len(rpmServerPass)
        print devicesRunning
        rpmFinalValue = rpmBPPass + rpmBPNonMatched
        fdaFinalValue = fdaBPPass + fdaBPNonMatched
        comFinalValue = comBPPass + comBPNonMatched
        serverFinalValue = serverBPPass + serverBPNonMatched
        rpmServerFinalValue = rpmServerPass + serverRPMBPNonMatched
        finalResult = BPpasscount + BPfailcount
        serverResult = Serverpasscount + Serverfailcount
        dataTypeFinal = dataType + dataType1

        df = pd.DataFrame()
        # df1 = pd.DataFrame()
        # df2 = pd.DataFrame()
        # df3 = pd.DataFrame()

        df['Data Type'] = dataTypeFinal
        df['RPM'] = rpmFinalValue
        df['FDA'] = fdaFinalValue
        df['Com'] = comFinalValue
        df['Result'] = finalResult
        df['RPM-SERVER'] = rpmServerFinalValue
        df['Server'] = serverFinalValue

        df['Server Result'] = serverResult
        # df['Data Type'] = dataType
        # df['RPM'] = rpmBPPass
        # df['FDA'] = fdaBPPass
        # df['Com'] = comBPPass
        # df2['RPM-SERVER'] = rpmServerPass
        # df2['Server'] = serverBPPass
        # df['Result'] = BPpasscount
        # df2['Server Result'] = Serverpasscount
        #
        # df1['Data Type'] = dataType1
        # df1['RPM'] = rpmBPNonMatched
        # df1['FDA'] = fdaBPNonMatched
        # df1['Com'] = comBPNonMatched
        # df3['RPM-SERVER']=serverRPMBPNonMatched
        # df3['Server'] = serverBPNonMatched
        # df1['Result'] = BPfailcount
        # df3['Server Result'] = Serverfailcount

        # h = df.append(df1,ignore_index=True)
        # h2 = df2.append(df3, ignore_index=True)
        # print h2
        # print h
        # df4 = pd.concat([h, h2], axis=1)
        writer = pd.ExcelWriter(PATH_BASE+devicesRunning+'Result.xlsx',
                                engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Report', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Report']
        writer.save()
        writer.close()

        # v = validationPharser.validationPharser()
        # v.extractValResult(valStr, rpmValStr, Config.valmatch[count], Config.match2[count], Config.valiweight[count], Config.rpmval[count]
        #                    , Config.rpmDate, Config.valDate, devicesRunning, PATH_BASE)