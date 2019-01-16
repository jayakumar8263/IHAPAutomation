import logPharser
import Search
import Config
import pandas as pd
import serverOperation
class runPO(object):
    def __init__(self):
        pass

    def executePO(self,  rawLogs, serverData, run=False):
        logPharserObj = logPharser.logPharser()
        searchObj = Search.logSearch()

        poDefFile = open(Config.PODEFINITIONFILE, 'r').read()
        serlst = []
        for i in range(len(serverData)):
            l = dict(serverData[i])
            if l.has_key('data'):
                serlst.append(l['data'])


        fdaPODefinition = logPharserObj.extractDic(poDefFile, extractCommunicationTemplate=False,
                                                   extractFDATemplate=True)
        comPODefinition = logPharserObj.extractDic(poDefFile, extractCommunicationTemplate=True,
                                                   extractFDATemplate=False)

        matchingFDAPOTemplate, matchingComPOTemplate = logPharserObj.matchDictTemplate(fdaPODefinition, comPODefinition)


        rpmPOList = searchObj.keywordSearch(rawLogs, *Config.RPMKEYS)
        fdaPOList = searchObj.keywordSearch(rawLogs, *Config.FDAKEYS)
        comPOList = searchObj.keywordSearch(rawLogs, *Config.COMMUNICATIONKEYS)
        rpmPOStr = '\n'.join(rpmPOList)
        fdaPOStr = '\n'.join(fdaPOList)
        comPOStr = '\n'.join(comPOList)

        rpmPOLst = logPharserObj.extractDic(rpmPOStr)

        fdaPOLst = logPharserObj.extractDic(fdaPOStr)

        comPOTempLst = logPharserObj.extractDic(comPOStr)
        comPOLst = logPharserObj.extractDictofDict(comPOTempLst)
        # serverPOLst = logPharserObj.extractDic(serlst)

        rpmPOValues = logPharserObj.checkformat(matchingFDAPOTemplate, rpmPOLst, Config.PO[0])
        fdaPOValues = logPharserObj.checkformat(matchingFDAPOTemplate, fdaPOLst, Config.PO[0])
        comPOValues = logPharserObj.checkformat(matchingComPOTemplate, comPOLst, Config.PO[0])
        serverPOValues = logPharserObj.checkformat(matchingComPOTemplate, serlst, Config.PO[0])

        rpmPOTmpVal = []
        fdaPOTmpVal = []
        comPOTmpVal = []
        serverPOTmpVal = []
        for i in range(len(rpmPOValues)):
            dict1 = dict(rpmPOValues[i])

            if dict1.has_key(Config.PO[0]):
                rpmPOTmpVal.append(dict1.copy())
        for i in range(len(fdaPOValues)):
            dict1 = dict(fdaPOValues[i])

            if dict1.has_key(Config.PO[0]):
                fdaPOTmpVal.append(dict1)

        for i in range(len(comPOValues)):
            dict1 = dict(comPOValues[i])

            if dict1.has_key(Config.PO[0]):
                comPOTmpVal.append(dict1)

        for i in range(len(serverPOValues)):
            dict1 = dict(serverPOValues[i])

            if dict1.has_key(Config.PO[0]):
                serverPOTmpVal.append(dict1)

        rpmFinalPO = logPharserObj.removeDuplicate(rpmPOTmpVal)
        fdaFinalPO = logPharserObj.removeDuplicate(fdaPOTmpVal)
        comFinalPO = logPharserObj.removeDuplicate(comPOTmpVal)
        serverFinalPO = logPharserObj.removeDuplicate(serverPOTmpVal)

        print matchingFDAPOTemplate
        print matchingComPOTemplate
        print comFinalPO
        PORPM, POFDA = logPharserObj.matchListEqual(rpmFinalPO, fdaFinalPO, matchingFDAPOTemplate,
                                                matchingComPOTemplate)

        POFDACOM, POCOM = logPharserObj.matchListEqual(POFDA, comFinalPO, matchingFDAPOTemplate,
                                                    matchingComPOTemplate)

        POSERVERCOM, POSERVER = logPharserObj.matchListEqual(POCOM, serverFinalPO, matchingFDAPOTemplate,
                                                       matchingComPOTemplate)
        print len(POSERVER)
        print len(POCOM)

        rpmPOMatched, rpmPONonMatched = logPharserObj.matchValues(PORPM, POFDACOM, 'date')

        fdaPOMatched, fdaPONonMatched = logPharserObj.matchValues(POFDACOM, PORPM, 'date')
        fdacomBPMatched, fdacomBPNonMatched = logPharserObj.matchValues(POFDACOM, POCOM, 'date')
        comPOMatched, comPONonMatched = logPharserObj.matchValues(POCOM, fdaPOMatched, 'date')
        serverPOMatched, serverPONonMatched = logPharserObj.matchValues(POSERVERCOM, PORPM, 'date')


        print rpmPOMatched
        rpmPOPass = logPharserObj.extractPassData(Config.PO, rpmPOMatched)

        fdaPOPass = logPharserObj.extractPassData(Config.PO, fdaPOMatched)

        # fdaBPPass = logPharserObj.extractPassData(Config.BP, fdacomBPMatched)
        comPOPass = logPharserObj.extractPassData(Config.PO, comPOMatched)

        serverPOPass = logPharserObj.extractPassData(Config.PO, serverPOMatched)



        POpasscount = logPharserObj.addData('Pass', fdaPOPass)
        POfailcount = logPharserObj.addData('Fail', fdaPONonMatched)
        dataType = logPharserObj.addData('PO', POpasscount)
        dataType1 = logPharserObj.addData('PO', POfailcount)
        # print POCOM
        # print len(comPOPass)
        # print len(rpmPOPass)
        # print len(fdaPOPass)

        fdaPONonMatchedFinal = list(str(fdaPONonMatched[i]) for i in range(len(fdaPONonMatched)))


        comPONonMatchedFinal = list(str(comPONonMatched[i]) for i in range(len(comPONonMatched)))

        df = pd.DataFrame()
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        df['Data Type'] = dataType
        df['RPM'] = rpmPOPass
        df['FDA'] = fdaPOPass
        df['Com'] = comPOPass
        df2['Server'] = serverPOPass
        df['Result'] = POpasscount

        df1['Data Type'] = dataType1
        df1['RPM'] = rpmPONonMatched
        df1['FDA'] = fdaPONonMatched
        df1['Com'] = comPONonMatched
        df3['Server'] = serverPONonMatched
        df1['Result'] = POfailcount

        h = df.append(df1, ignore_index=True)
        h2 = df2.append(df3, ignore_index=True)
        df4 = pd.concat([h, h2], axis=1)
        writer = pd.ExcelWriter('POResult.xlsx',
                                engine='xlsxwriter')
        df4.to_excel(writer, sheet_name='Report', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Report']
        writer.save()
        writer.close()

