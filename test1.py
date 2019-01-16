import Search
import re

def validationPhrase():

    logSearch = Search.logSearch()
    weightVal = [120.0, 85.0, 130.0, 108.0, 81.0, 163.0, 94.0]
    fileOpen = str(open("-adbLogs.log",'r').read())

    keyword = ["Validation_automation", 'Max']

    k = logSearch.keywordSearch(fileOpen,*keyword)

    valValues = []

    print k
    valResult = ' '.join(k)
    valResult = re.sub('[^a-zA-Z0-9 \n\.]', ' ', valResult)
    validationLst = valResult.split()
    valWeightIndex = [i for i, x in enumerate(validationLst) if x == 'WeightRecord']

    weightMinVal = []
    weightMaxVal = []

    for i in valWeightIndex:
        weightMaxVal.append(validationLst[i + 2])
        weightMinVal.append(validationLst[i + 4])

    print weightMaxVal
    print weightMinVal

    valWeightResult = []
    for i in range(len(weightVal)):

        if weightVal[i] >= int(weightMinVal[i]) and weightVal[i] <= int(weightMaxVal[i]):
            valWeightResult.append("Pass")
            valValues.append(weightMinVal[i] + '-' + weightMaxVal[i])
        else:
            valWeightResult.append("Fail")
            valValues.append(weightMinVal[i] + '-' + weightMaxVal[i])

    valPOIndex = [i for i, x in enumerate(validationLst) if x == 'PORecord']

    minspoVal = []
    maxspoVal = []
    minbpmVal = []
    maxbpmVal = []
    POBPM = [54.0, 57.0, 50.0, 60.0, 59.0, 60.0, 60.0]
    POSPO = [66.0, 66.0, 70.0, 68.0, 69.0, 65.0, 167.0]
    for i in valPOIndex:
        minspoVal.append(validationLst[i+4])
        maxspoVal.append(validationLst[i+2])
        minbpmVal.append(validationLst[i+8])
        maxbpmVal.append(validationLst[i+6])
    print minspoVal
    print minbpmVal
    valPOResult = []
    for i in range(len(POSPO)):

        if (POSPO[i] >= int(minspoVal[i]) and POSPO[i] <= int(maxspoVal[i]) and POBPM[i] >= int(minbpmVal[i])
                and POBPM[i] <= int(maxbpmVal[i])):
            valPOResult.append("Pass")
            valValues.append(minspoVal[i] + '-' + maxspoVal[i] + '|' + minbpmVal[i] + '-' + maxbpmVal[i])
        else:
            valPOResult.append("Fail")
            valValues.append(minspoVal[i] + '-' + maxspoVal[i] + '|' + minbpmVal[i] + '-' + maxbpmVal[i])



    valBPIndex = [i for i, x in enumerate(validationLst) if x == 'BPRecord']

    minSysVal = []
    maxSysVal = []
    minDiaVal = []
    maxDiaVal = []
    minPulseVal = []
    maxPulseVal = []

    for i in valBPIndex:
        minSysVal.append(validationLst[i+4])
        maxSysVal.append(validationLst[i+2])
        minDiaVal.append(validationLst[i+8])
        maxDiaVal.append(validationLst[i+6])
        minPulseVal.append(validationLst[i+12])
        maxPulseVal.append(validationLst[i+10])

    print minSysVal
    print maxSysVal
    print minDiaVal
    print maxDiaVal
    print minPulseVal
    print maxPulseVal

    valBPResult = []
    BPSYSValue = [88.0, 90.0, 82.0, 83.0, 30.0, 66.0, 45.0]
    BPPulseValue = [69.0, 69.0, 66.0, 67.0, 78.00, 80.0, 90.0]
    BPDiaValue = [48.0, 46.0, 45.0, 41.0, 100.0, 120.0, 200.0]

    for i in range(len(BPSYSValue)):

        if (BPSYSValue[i] >= int(minSysVal[i]) and BPSYSValue[i] <= int(maxSysVal[i])
            and BPPulseValue[i] >= int(minDiaVal[i]) and BPPulseValue[i] <= int(maxDiaVal[i])
            and BPDiaValue[i] >= int(minPulseVal[i]) and BPDiaValue[i] <= int(maxPulseVal[i])):

            valBPResult.append("Pass")
            valValues.append(minSysVal[i] + '-' + maxSysVal[i] + '|' + minPulseVal[i] + '-' + maxPulseVal[
                i] + '|' + minDiaVal[i] + '-' + maxDiaVal[i])
        else:
            valBPResult.append("Fail")
            valValues.append(minSysVal[i] + '-' + maxSysVal[i] + '|' + minPulseVal[i] + '-' + maxPulseVal[
                i] + '|' + minDiaVal[i] + '-' + maxDiaVal[i])

    po = []
    bp = []
    for i in range(len(POBPM)):
        po.append(str(POSPO[i])+'-'+str(POBPM[i]))

    for i in range(len(BPSYSValue)):
        bp.append(str(BPSYSValue[i])+'-'+str(BPPulseValue[i])+'-'+str(BPDiaValue[i]))
    print valValues
    print valWeightResult + valPOResult + valBPResult
    print weightVal+po+bp


validationPhrase()


xmlVal = '''<?xml version="1.0" encoding="utf-8" ?>
<validation version="8.0">
	<device-config isRequired="TRUE" parseTime="60000">
		<device type="BP" isRequired="true" repeatTime="60000">
			<value>
				<max>90</max>
				<min>80</min>
			</value>
			<value>
				<max>70</max>
				<min>60</min>
			</value>
			<value>
				<max>50</max>
				<min>40</min>
			</value>
		</device>
		<device type="PO" isRequired="true" repeatTime="20000">
			<value>
				<max>70</max>
				<min>65</min>
			</value>
			<value>
				<max>60</max>
				<min>50</min>
			</value>
		</device>
		<device type="WEIGHT" isRequired="true" repeatTime="30000">
			<value>
				<max>150</max>
				<min>80</min>
			</value>
		</device>
	</device-config>
</validation>'''