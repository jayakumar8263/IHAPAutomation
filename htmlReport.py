'''

@author: Jayakumar M
'''

from json2html import *

import json

import xlrd
from collections import OrderedDict
import simplejson as json

from pandas import DataFrame, read_csv

import pandas as pd



class htmlReport(object):

    def __init__(self):
        pass

    def generateHTML(self, resultExcel, filePath):
        # Open the workbook and select the first worksheet

        df = pd.read_excel(resultExcel)
        j = df['Server Result']

        passfail = []
        for i in range(len(j)):
            passfail.append(j[i])

        print passfail

        totalCount = str(len(passfail))

        passCount = str(passfail.count("Pass"))
        failCount = str(passfail.count("Fail"))


        wb = xlrd.open_workbook(resultExcel)
        # wb1 = xlrd.open_workbook(validationExcel)
        # sh1 = wb1.sheet_by_index(0)
        sh = wb.sheet_by_index(0)

        # List to hold dictionaries
        fda = []
        com = []
        server = []
        allresult = []
        validation = []
        # for rownum in range(1, sh1.nrows):
        #     cars = OrderedDict()
        #     row_values1 = sh1.row_values(rownum)
        #     cars['Datatype'] = row_values1[0]
        #     cars['RPM Values'] = row_values1[1]
        #     # cars['Validation Values'] = row_values1[2]
        #     cars['Result'] = row_values1[2]
        #
        #     validation.append(cars)

        for rownum in range(1, sh.nrows):
            cars = OrderedDict()
            row_values = sh.row_values(rownum)
            cars['Datatype'] = row_values[0]
            cars['RPM Data'] = row_values[1]
            cars['FDA Data'] = row_values[2]
            cars['Result'] = row_values[4]

            fda.append(cars)
        for rownum in range(1, sh.nrows):
            cars = OrderedDict()
            row_values = sh.row_values(rownum)
            cars['Datatype'] = row_values[0]
            cars['RPM Data'] = row_values[1]
            cars['COM. Data'] = row_values[3]
            cars['Result'] = row_values[4]

            com.append(cars)
        for rownum in range(1, sh.nrows):
            cars = OrderedDict()
            row_values = sh.row_values(rownum)
            cars['Datatype'] = row_values[0]
            cars['Server Data'] = row_values[6]
            cars['Server-RPM Data'] = row_values[5]
            cars['Server Result'] = row_values[7]
            server.append(cars)

        for rownum in range(1, sh.nrows):
            cars = OrderedDict()
            row_values = sh.row_values(rownum)
            cars['Datatype'] = row_values[0]
            cars['RPM Data'] = row_values[1]
            cars['FDA Data'] = row_values[2]
            cars['COM. Data'] = row_values[3]
            cars['Result'] = row_values[4]
            cars['Server Data'] = row_values[6]
            cars['Server-RPM Data'] = row_values[5]
            cars['Server Result'] = row_values[7]
            allresult.append(cars)

        # Serialize the list of dicts to JSON
        fdajson = json.dumps(fda)
        comjson = json.dumps(com)
        serverjson = json.dumps(server)
        allresultjson = json.dumps(allresult)
        # validationjson = json.dumps(validation)

        with open(filePath+'fdadata.json', 'w') as f:
            f.write(fdajson)
        f.close()
        with open(filePath+'comdata.json', 'w') as f:
            f.write(comjson)
        f.close()
        with open(filePath+'serverdata.json', 'w') as f:
            f.write(serverjson)
        f.close()

        with open(filePath+'allresultdata.json', 'w') as f:
            f.write(allresultjson)
        f.close()

        # with open(filePath+'validation.json', 'w') as f:
        #     f.write(validationjson)
        # f.close()

        infoFromJson = open(filePath+'fdadata.json', 'r').read()
        # k = json2html.convert(json = infoFromJson)
        b = open(filePath+'comdata.json', 'r').read()

        e = open(filePath+'serverdata.json', 'r').read()

        q = open(filePath+'allresultdata.json', 'r').read()
        # m = open(filePath+'validation.json','r').read()
        # dictionary

        k = json2html.convert(json=infoFromJson)

        j = json2html.convert(json=b)

        l = json2html.convert(json=e)

        u = json2html.convert(json=q)

        # v = json2html.convert(json=m)

        k = k.replace('<table border="1">', '')
        j = j.replace('<table border="1">', '')
        l = l.replace('<table border="1">', '')
        u = u.replace('<table border="1">', '')
        # v = v.replace('<table border="1">', '')
        k = k.replace('</table>', '')
        j = j.replace('</table>', '')
        l = l.replace('</table>', '')
        u = u.replace('</table>', '')
        # v = v.replace('</table>', '')

        print k
        print "*********************************************************"

        print j
        print "*********************************************************"

        print l
        print "*********************************************************"

        print u

        htmlval = '''<!DOCTYPE html>
       <html>
        <head>
        <style>
        body {font-family: "Lato", sans-serif;}
        
        /* Style the tab */
        div.tab {
            overflow: hidden;
            border: 1px solid #000305;
            background-color: #ade7ff;
            padding: 0px 1px;
            width: 100%
        }
        
        /* Style the buttons inside the tab */
        div.tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 14px;
            transition: 0.3s;
            font-size: 14px;
            font-weight: bold;
        }
        
        /* Change background color of buttons on hover */
        div.tab button:hover {
            background-color: #0081ad;
        }
        
        /* Create an active/current tablink class */
        div.tab button.active {
            background-color: #2db4e2;
        }
        
        /* Style the tab content */
        .tabcontent {
            table-layout: fixed;
            border-collapse:collapse;
            display: none;
            padding: 1px 1px;
            border: 1px solid #000305;
            border-top: none;
            word-wrap: break-word;
            
        
            width: 100%;
        }
            #customers {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 1565px;
        
        }
        
        #customers td, #customers th {
            border: 1px solid #000305;
            padding: 18px 0px;
        
        
        }
        
        #customers tr:nth-child(even){background-color: #f2f2f2;white-space: -o-pre-wrap;
            word-wrap: break-word;
            }
        
        #customers tr:hover {background-color: #ddd; white-space: -o-pre-wrap;
            word-wrap: break-word;
            }
        
        #customers th {
            table-layout: fixed;
            padding: 8px 8px;
            text-align: center;
            background-color: #ff773f;
            color: black;
            width: 1565px;
            
        
        
        
        }
        </style>
        <h1><font color="#0083b3" face="sans-serif">Validation Test Report</font></h1>
        
        </head>
        <body>
        <p>Total : <font color="#0083b3" ><b>'''+totalCount+'''</b></font>
        | Pass  : <font color="#0f8d00"><b>'''+passCount+'''</b></font>
        | Fail  : <font color="#e00303"><b>'''+failCount+'''</b></font></p>
        <p>Click on the buttons for detailed result:</p>
        
        <div class="tab">
          <button class="tablinks" onclick="openCity(event, 'FDA')">FDA</button>
          <button class="tablinks" onclick="openCity(event, 'Communication')">Communication</button>
          <button class="tablinks" onclick="openCity(event, 'Server')">Server</button>
          <button class="tablinks" onclick="openCity(event, 'All Result')">All Result</button>
        </div>
        
        <div id="FDA" class="tabcontent">
          <h3>FDA Result</h3>
          <table id="customers"><tbody>''' + k + '''</tbody></table></div><div id="Communication" class="tabcontent">
          <h3>Communication</h3>
          <table id="customers"><tbody>''' + j + '''</tbody></table></div><div id="Server" class="tabcontent">
          <h3>Server</h3>
          <table id="customers"><tbody>''' + l + '''</tbody></table></div><div id="Validation" class="tabcontent">

        </div>
        <div id="All Result" class="tabcontent">
          <h3>All Result</h3>
           <table id="customers"><tbody>''' + u + '''</tbody></table></div><script>
        function openCity(evt, cityName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(cityName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        
        var allTableCells = document.getElementsByTagName("td");
        for(var i = 0, max = allTableCells.length; i < max; i++) {
            var node = allTableCells[i];
        
            //get the text from the first child node - which should be a text node
            var currentText = node.childNodes[0].nodeValue; 
        
            //check for 'one' and assign this table cell's background color accordingly 
            if (currentText === "Pass")
                node.style.backgroundColor = "#76e98e";
            if (currentText === "Fail")
                node.style.backgroundColor = "#e97676";
                node.style.font = "14px arial,serif";
                node.style.textAlign = "center"
        }
        
        ;(function($) {
           $.fn.fixMe = function() {
              return this.each(function() {
                 var $this = $(this),
                    $t_fixed;
                 function init() {
                    $this.wrap('<div class="container" />');
                    $t_fixed = $this.clone();
                    $t_fixed.find("tbody").remove().end().addClass("fixed").insertBefore($this);
                    resizeFixed();
                 }
                 function resizeFixed() {
                    $t_fixed.find("th").each(function(index) {
                       $(this).css("width",$this.find("th").eq(index).outerWidth()+"px");
                    });
                 }
                 function scrollFixed() {
                    var offset = $(this).scrollTop(),
                    tableOffsetTop = $this.offset().top,
                    tableOffsetBottom = tableOffsetTop + $this.height() - $this.find("thead").height();
                    if(offset < tableOffsetTop || offset > tableOffsetBottom)
                       $t_fixed.hide();
                    else if(offset >= tableOffsetTop && offset <= tableOffsetBottom && $t_fixed.is(":hidden"))
                       $t_fixed.show();
                 }
                 $(window).resize(resizeFixed);
                 $(window).scroll(scrollFixed);
                 init();
              });
           };
        })(jQuery);
        
        $(document).ready(function(){
           $("table").fixMe();
           $(".up").click(function() {
              $('html, body').animate({
              scrollTop: 0
           }, 2000);
         });
        });
        
        
        </script>
        
        </body>
        </html> '''

        htmlfile = open(filePath+'Report.html', 'w')

        htmlfile.write(htmlval.encode('utf-8'))

        htmlfile.close()

