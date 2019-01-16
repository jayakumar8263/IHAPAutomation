import pandas as pd
import numpy as np


class mergeExcel(object):

    def __int__(self):
        pass

    def mergeResultExcel(self, resultPath, *filename):


        rpmXls = pd.read_excel(
            filename[0],
            keep_default_na=True, na_values=[" "])


        fdaXls = pd.read_excel(
            filename[1],
            keep_default_na=True, na_values=[" "])

        comXls = pd.read_excel(
            filename[2],
            keep_default_na=True, na_values=[" "])

        resultXls = pd.concat([rpmXls, fdaXls, comXls], axis=1)
        writer = pd.ExcelWriter(resultPath+'Result.xlsx', engine='xlsxwriter')
        resultXls.to_excel(writer, sheet_name='Sheet1', index=False)

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
        worksheet.set_column('J:J', 11, format1)
        worksheet.set_column('K:K', 21, format1)
        worksheet.set_column('L:L', 12, format1)
        worksheet.set_column('M:M', 11, format1)
        worksheet.set_column('N:N', 17, format1)
        worksheet.set_column('O:O', 15, format1)
        worksheet.set_column('P:P', 12, format1)
        worksheet.set_column('Q:Q', 14, format1)
        worksheet.set_column('R:R', 17, format1)
        worksheet.set_column('S:S', 11, format1)
        worksheet.set_column('T:T', 21, format1)
        worksheet.set_column('U:U', 12, format1)
        worksheet.set_column('V:V', 11, format1)
        worksheet.set_column('W:W', 17, format1)
        worksheet.set_column('X:X', 15, format1)
        worksheet.set_column('Y:Y', 12, format1)
        worksheet.set_column('Z:Z', 14, format1)
        worksheet.set_column('AA:AA', 17, format1)

        writer.save()
        writer.close()