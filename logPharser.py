import re
import ast
import json
import time
import Config


class logPharser(object):
    def __init__(self):
        pass

    def extractDic(self, configFileName, extractCommunicationTemplate=False, extractFDATemplate=False):
        number_of_parthesis = 0
        start_index = -1
        in_quotes = False
        listOfDict = []
        for i, c in enumerate(configFileName):
            if c in ["\'", "\""]:
                if in_quotes:
                    in_quotes = False
                else:
                    in_quotes = True
            if in_quotes:
                continue
            if c == "{":
                number_of_parthesis += 1
                if start_index == -1:
                    start_index = i
            if c == "}":
                number_of_parthesis -= 1
                if number_of_parthesis == 0:
                    val = (configFileName[start_index:i + 1]).replace('\n', '')
                    val = re.sub("\s\s+", " ", val)
                    listOfDict.append(val)
                    start_index = -1
        if extractCommunicationTemplate:
            newListOfDict = []
            j = re.sub(r'\{[^)]*\{', '', listOfDict[1])
            j = '{' + j
            j = j[:-1]

            result = re.search('{(.*)}', j)

            p = '{' + result.group(1) + '}'
            newListOfDict.append(p)
            return newListOfDict
        elif extractFDATemplate:
            fdaList = []
            fdaList.append(listOfDict[0])
            return fdaList
        else:
            return listOfDict


    def extractDictofDict(self,dictOfDict):
        # Converting the format according to the fda template
        newListOfDict = []
        for i in range(len(dictOfDict)):
            j = re.sub(r'\{[^)]*\{', '', dictOfDict[i])
            j = '{' + j
            j = j[:-1]

            result = re.search('{(.*)}', j)

            p = '{' + result.group(1) + '}'
            newListOfDict.append(p)
        return newListOfDict

    def extractDictofServerDict(self,dictOfDict):
        # Converting the format according to the fda template
        newListOfDict = []
        for i in range(len(dictOfDict)):
            j = re.sub(r'\{[^)]*\{', '', str(dictOfDict[i]))
            j = '{' + j
            j = j[:-1]

            result = re.search('{(.*)}', j)

            p = '{' + result.group(1) + '}'
            newListOfDict.append(p)
        return newListOfDict


    # fdaDefinition = extractDic(d, extractCommunicationTemplate=False, extractFDATemplate=True)
    # comTemplate = extractDic(d, extractCommunicationTemplate=True, extractFDATemplate=False)


    def matchDictTemplate(self, fdaDefinition, comTemplate):
        matchingFDATemplate = {}
        matchingComTemplate = {}
        val1w = []
        for i in range(len(comTemplate)):
            dict1 = dict((k, str(v)) for k, v in ast.literal_eval(fdaDefinition[i]).iteritems())

            dict2 = dict((k, str(v)) for k, v in ast.literal_eval(comTemplate[i]).iteritems())
            for key in dict1.values():
                if key in dict2.values():
                    # if dict1[values] == dict2[values]:
                    # matching_dict_values[key]=dict1[key]
                    a = dict2.keys()[dict2.values().index(key)]
                    b = dict2[dict2.keys()[dict2.values().index(key)]]
                    val1 = tuple([a])

                    val2 = tuple([b])
                    val = dict(zip(val1, val2))

                    matchingComTemplate.update(val)
            for key1 in dict2.values():
                if key1 in dict1.values():
                    a = dict1.keys()[dict1.values().index(key1)]
                    b = dict1[dict1.keys()[dict1.values().index(key1)]]
                    val1 = tuple([a])

                    val2 = tuple([b])
                    val = dict(zip(val1, val2))

                    matchingFDATemplate.update(val)
        return matchingFDATemplate, matchingComTemplate


    # matchingFDATemplate, matchingComTemplate = matchDictTemplate(fdaDefinition, comTemplate)


    # y = open('fda.txt', 'r').read()


    def checkformat(self, defauldict, dictlist, hasKey):
        # Checking the values are in correct template
        value = []
        val = ''
        comTimestamp = ''
        fda = {}
        print "server dict", dictlist
        for j in range(len(dictlist)):
            dict1 = dict((k, str(v)) for k, v in ast.literal_eval(dictlist[j]).iteritems())

            for i in defauldict.keys():
                if dict1.has_key(hasKey):
                    if dict1.has_key(i) and i != Config.rpmDate:

                        val1 = tuple([dict1[i]])

                        val2 = tuple([i])
                        vfval = dict(zip(val2, val1))
                        fda.update(vfval)

                    elif dict1.has_key(Config.rpmDate) and i == Config.rpmDate and dict1.has_key(hasKey):
                        comTimestamp = dict1[i]
                        val1 = tuple([comTimestamp])
                        val2 = tuple([i])
                        vfval = dict(zip(val2, val1))
                        fda.update(vfval)

            value.append(fda.copy())
        return value

    def removeDuplicate(self, listDict):
        return [i for n, i in enumerate(listDict) if i not in listDict[n + 1:]]



    def matchListEqual(self,listOne, listTwo, matchingFDATemplate, matchingComTemplate):
        maxLength = max(len(listOne), len(listTwo))

        if len(listOne) == len(listTwo):
            pass
        else:
            if len(listOne) != maxLength:
                diff1 = maxLength - len(listOne)
                for i in range(diff1):
                    listOne.append(matchingFDATemplate.copy())
            if len(listTwo) != maxLength:
                diff2 = maxLength - len(listTwo)
                for i in range(diff2):
                    listTwo.append(matchingComTemplate.copy())
        return listOne, listTwo



    def matchValues(self, listDict1, listDict2, sortBy):
        matchedVal = [x for x in listDict1 if x in listDict2]
        print matchedVal
        matchedVal = sorted(matchedVal, key=lambda k: k[sortBy])
        nonMatchedVal = [x for x in listDict1 if x not in listDict2]
        nonMatchedVal = sorted(nonMatchedVal, key=lambda k: k[sortBy])
        print nonMatchedVal
        return matchedVal, nonMatchedVal


    def extractPassData(self, dataList, listData):
        passv = []
        for i in range(len(listData)):
            f = listData[i]
            for j in dataList:
                if f.has_key(j):
                    passv.append(str(f[j]))
        size = len(dataList)
        print passv
        bp = [passv[i:i + size] for i in range(0, len(passv), size)]
        passData = [u"\u0020\u2726\u0020".join(x) for x in bp]
        # passData = ["-".join(x) for x in bp]

        return passData

    def extractValPassData(self, dataList, listData):
        passv = []
        passv1 = []
        for i in range(len(listData)):
            f = listData[i]
            for j in dataList:
                if f.has_key(j):
                    passv.append(str(f[j]))
        size = len(dataList)

        bp = [passv[i:i + size] for i in range(0, len(passv), size)]
        for l in bp:
            bp2 = [l[i:i + 2] for i in range(0, len(l), 2)]


            passData1 = ["-".join(x) for x in bp2]

            passData2 = ["".join(x) for x in passData1]
            passv1.append(u"\u0020\u2726\u0020".join(passData2))
        return passv1

    def addData(self, textVal, listData):
        return list(textVal for i in range(len(listData)))






