
#######################################LOCAL PATH WHERE THE ALL APKs PRESENT############################################
APKPATH = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\Apks"

######################################MENTION THE PATH WHERE VALIDATION APK PRESENT WITH FILE NAME######################
VALIDATIONAPK = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ValidationApk\Validation_6.111.6_signed.apk"


#####################################LOCAL PATH WHERE THE VALIDATION CONFIG PRESENT#####################################
VALIDATIONCONFIG = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\Validation"


#####################################LOCAL PATH WHERE THE MANAGEMENT CONFIG PRESENT#####################################
MANGAMENTCONFIG = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Management"


#####################################LOCAL PATH WHERE THE COMMUNICATION CONFIG PRESENT##################################
COMMUNICATIONCONFIG = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication"


####################################Mention the correct UserProfile ID get details from portal using Firebug############
SERVERUSERPROFILEID = "aus1y"


###################################Mention the correct DATA Server IP###################################################
DATASERVERIP = "54.68.227.234"

###################################BP VALUE#############################################################################
BP =['Diastolic', 'Systolic', 'Pulse', 'date']
PO = ['spo2', 'BPM', 'date']
WEIGHT = ['Weight', 'date']
MEDICALDEVICES = {'BP': ['Diastolic', 'Systolic', 'Pulse', 'measurementTime'],
                 'PO': ['spo2', 'BPM', 'measurementTime'],
                 'Weight': ['Weight', 'measurementTime']}

DEFINITIONFILES = ["C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication\BP.txt",
                   "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication\PO.txt",
                   "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication\WEIGHT.txt"]

RPMKEYS = ['DatabaseAccessor_automation', 'deviceDataList']
FDAKEYS = ['FDADB_RpmService_automation', 'insertMedicalDataFromRpm']
COMMUNICATIONKEYS = ['Communication_HttpsConnectionCommunication_automation', 'uploadServerData']
VALIDATIONKEYS = [['Validation_automation', 'getBpRecord'], ['Validation_automation', 'getOxyRecord'],
                  ['Validation_automation', 'getScaleRecord']]
RPMVALIDATIONKEYS = [['DatabaseAccessor_automation', 'insertBPDeviceData'],
                     ['DatabaseAccessor_automation', 'insertPODeviceData'],
                     ['DatabaseAccessor_automation', 'insertWeightDeviceData']]

BPDEFINITIONFILE = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication\BP.txt"
WEIGHTDEFINITIONFILE = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication\WEIGHT.txt"
PODEFINITIONFILE = "C:\Users\jmunis1x\PycharmProjects\Austonio_Automation_CESL\ConfigFile\Communication\PO.txt"
DEVICES = ['BP', 'PO', 'Weight']

match2 = ['{"Diastolic":"0","Systolic":"0","Pulse":"0","unit":"NA","measurementTime":"0","receiptTime":"NA","date":"NA","model":"NA","manufacturer":"NA","serialnumber":"NA"}',
        '{"spo2":"0","BPM":"0","unit":"%","measurementTime":"0","receiptTime":"0","date":"NA","model":"NA","manufacturer":"NA","serialnumber":"NA"}',
          '{"Weight":0,"unit":"NA","measurementTime":"0","receiptTime":"NA","date":"NA","model":"NA","manufacturer":"NA","serialnumber":"NA"}'
          ]

valmatch = ['{"sysMax":0, "sysMin":0, "diaMax":0, "diaMin":0, "pulseMax":0, "pulseMin":0, "date":"0"}'
            , '{"spo2Max":0, "spo2Min":0, "bpmMax":0, "bpmMin":0, "date":"0"}', '{"weightMax":0, "weightMin":0, "date":"0"}'
            ]

rpmval = [['Diastolic', 'Systolic', 'Pulse'], ['spo2', 'BPM'], ['Weight']]
valiweight = [[('diaMax', 'diaMin'), ('sysMax', 'sysMin'), ('pulseMax', 'pulseMin')],
              [('spo2Max', 'spo2Min'), ('bpmMax', 'bpmMin')],
              [('weightMax', 'weightMin')]]
valDate = "date"
rpmDate = "measurementTime"
