from json2html import *

import json

import xlrd
from collections import OrderedDict
import simplejson as json

from pandas import DataFrame, read_csv

import pandas as pd


df = pd.read_excel('FinalResult.xlsx')
j = df['Result']

passfail = []
for i in range(len(j)):
	passfail.append(j[i])

print passfail

totalCount =  str(len(passfail))

passCount = str(passfail.count("Pass"))
failCount =  str(passfail.count("Fail"))


wb = xlrd.open_workbook('FinalResult.xlsx')

sh = wb.sheet_by_index(0)

# List to hold dictionaries
fda = []
com = []
server = []
allresult = []
validation = []

for rownum in range(1, sh.nrows):
	cars = OrderedDict()
	row_values = sh.row_values(rownum)
	cars['Data Type'] = row_values[0]
	cars['FDA Values'] = row_values[1]
	cars['Com Values'] = row_values[2]
	cars['Result'] = row_values[3]

	fda.append(cars)


# Serialize the list of dicts to JSON
fdajson = json.dumps(fda)

with open('fdadata.json', 'w') as f:
	f.write(fdajson)
f.close()


infoFromJson = open('fdadata.json', 'r').read()



k = json2html.convert(json=infoFromJson)


k = k.replace('<table border="1">', '')


print k
print "*********************************************************"


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
	padding: 0px 24px;
	width: 100%
}

/* Style the buttons inside the tab */
div.tab button {
	background-color: inherit;
	float: left;
	border: none;
	outline: none;
	cursor: pointer;
	padding: 14px 16px;
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
	table-layout: auto;
	border-collapse:collapse;
	display: none;
	padding: 1px 24px;
	border: 1px solid #000305;
	border-top: none;

	word-wrap: break-word;

	width: 100%
}
	#customers {
	font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
	border-collapse: collapse;
	width: 100%;

}

#customers td, #customers th {
	border: 1px solid #000305;
	padding: 8px;


}

#customers tr:nth-child(even){background-color: #f2f2f2;white-space: -o-pre-wrap; 
	word-wrap: break-word;
	}

#customers tr:hover {background-color: #ddd;white-space: -o-pre-wrap; 
	word-wrap: break-word;
	}

#customers th {
	table-layout: auto;
	padding-top: 12px;
	padding-bottom: 12px;
	text-align: center;
	background-color: #ff773f;
	color: black;
	white-space: -o-pre-wrap; 
	word-wrap: break-word;



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
  <button class="tablinks" onclick="openCity(event, 'Validation')">Validation</button>
  <button class="tablinks" onclick="openCity(event, 'All Result')">All Result</button>
</div>

<div id="FDA" class="tabcontent">
  <h3>FDA Result</h3>
  <table id="customers"><tbody>''' + k + '''</tbody></table></div><div id="Communication" class="tabcontent">
  <h3>Communication</h3>
  <table id="customers"><tbody>hj</tbody></table></div><div id="Server" class="tabcontent">
  <h3>Server</h3>
  <table id="customers"><tbody>kk</tbody></table></div><div id="Validation" class="tabcontent">
  <h3>Validation</h3>
  <table id="customers"><tbody>xx</tbody></table></div><div id="Validation" class="tabcontent">
</div>
<div id="All Result" class="tabcontent">
  <h3>All Result</h3>
   <table id="customers"><tbody>xxxx</tbody></table></div><script>
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

htmlfile = open('Report.html', 'w')

htmlfile.write(htmlval)

htmlfile.close()
print htmlval
