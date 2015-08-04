var xmlHttp = createXmlHttpRequestObject();
var serverFilePaths = [];
var serverFileNames = [];
var serverFileDates = [];

// create object
function createXmlHttpRequestObject() {
  var xmlHttp;

  if (window.XMLHttpRequest) {
    xmlHttp = new XMLHttpRequest();
  } else {
    xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  return xmlHttp;
}


//create processfunction, called on load
function process() {
  if (xmlHttp) {
    try {
      xmlHttp.open("GET","skynetcontent.xml",true);
      xmlHttp.onreadystatechange = handleStateChange;
      xmlHttp.send(null);
    } catch (e) {
      alert(e.toString());
    }
  }
}

// when state changes
function handleStateChange() {
  if (xmlHttp.readyState==4) {
    if (xmlHttp.status==200) {
      try {
        handleResponse();
      } catch (e) {
        alert(e.toString());
      }
    } else {
      alert(xmlHttp.statusText);
    }
  }
}

// handle the response from the server
function handleResponse() {
  var xmlResponse = xmlHttp.responseXML;
  root = xmlResponse.documentElement;

  panelNames = root.getElementsByTagName("panelfilename");
  sidebarList = document.getElementById("sidebarList");
  sidebarList.innerHTML = createSidepanelList(panelNames);

  fileNames = root.getElementsByTagName("serverfilename");
  filePaths = root.getElementsByTagName("serverfilepath");
  fileDates = root.getElementsByTagName("serverfiledate");
  tableList = document.getElementById("tableList");

  for (var i = 0; i < fileNames.length; i++) {
  // add to global variable to quicker process later
    serverFilePaths.push(filePaths.item(i).firstChild.data);
    serverFileNames.push(fileNames.item(i).firstChild.data);
    serverFileDates.push(fileDates.item(i).firstChild.data);
  }

  var tablecontent = createTableListFromArray(serverFileNames,serverFilePaths,serverFileDates);
  tableList.innerHTML = tablecontent;
}

function createTableListFromArray(fileNames,filePaths,fileDates) {

  var tableListOutput = "";

  for (var i = 0; i < fileNames.length; i++) {

    var nowdate = new Date();
    var filedate = new Date(fileDates[i]);

    var diff = differenceInDays(filedate,nowdate);
    var expiration = 40 - diff;
    var expirationPercentage = (expiration/40)*100;

    if (diff == '0'){tableListOutput += "<tr class='alert-success-edit'>";}
    else {tableListOutput += "<tr>";}

    tableListOutput += "<td> <a href=" + filePaths[i] + ">"  + fileNames[i] + "</a></td>";
    tableListOutput += "<td>" + formatDate(filedate)  + "</td>";
    tableListOutput += "<td>" + diff + " days </td>";
    tableListOutput += "<td>";
    tableListOutput += "<div class='progress progress-slim'>";
    tableListOutput += "<div class='progress-bar' role='progressbar' aria-valuemin='0' aria-valuemax='40' style='width: "+expirationPercentage+"%; float: right;'>";
    tableListOutput += "<span class='sr-only'>90% Complete</span>";
    tableListOutput += "</div>";
    tableListOutput += "</div>";
    tableListOutput += "</td>";
    tableListOutput += "</tr>";
  }
  return tableListOutput;
}


function createSidepanelList(nameArray) {
  // build the static overhead
  var listOutput = '<li onclick="listAll() "class="active"> <a href="#">Overview <span class="sr-only">(current)</span></a></li>';

  for (var i = 0; i < nameArray.length; i++) {
    var buttonlink = '"' + nameArray.item(i).firstChild.data.toString() + '"';
    listOutput += "<li onclick='filterByName("+buttonlink+")'><a href='#'>" + nameArray.item(i).firstChild.data + "</a></li>";
  }
  return listOutput;
}

function formatDate(datein) {
    var dd = datein.getDate();
    var mm = datein.getMonth()+1; //January is 0!

    var yyyy = datein.getFullYear();
    if(dd<10){
        dd='0'+dd
    }
    if(mm<10){
        mm='0'+mm
    }
    var today = dd+'.'+mm+'.'+yyyy;
    //document.getElementById("DATE").value = today;
    return today;
}

function differenceInDays(date1,date2) {
  var days = Math.floor((date2 - date1) / (1000*60*60*24))
  return days;
}

function filterByName(inputname) {

  var substrings = inputname.toLowerCase().split(" ");
  nArray = [];
  pArray = [];
  dArray = [];

  for (var i = 0; i < serverFileNames.length; i++) {

    var checkName = serverFileNames[i].toLowerCase();
    var matches = 0;
    length = substrings.length;
    while(length--) {
      if (checkName.indexOf(substrings[length])!=-1) {
        matches++;
      }
    }
    if (matches == substrings.length){
      nArray.push(serverFileNames[i]);
      pArray.push(serverFilePaths[i]);
      dArray.push(serverFileDates[i]);
    }

  }

  var filteredlist = createTableListFromArray(nArray,pArray,dArray);
  tableList = document.getElementById("tableList");
  tableList.innerHTML = filteredlist;

  tableHeader = document.getElementById("serieSubHeader");
  tableHeader.innerHTML = inputname;
}

function listAll() {
  var filteredlist = createTableListFromArray(serverFileNames,serverFilePaths,serverFileDates);
  tableList = document.getElementById("tableList");
  tableList.innerHTML = filteredlist;

  tableHeader = document.getElementById("serieSubHeader");
  tableHeader.innerHTML = "All";
}
