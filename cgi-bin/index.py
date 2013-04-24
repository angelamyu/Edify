#!/usr/bin/env python


from insert_select_data import select
import cgi

form = cgi.FieldStorage()
if 'criterion' in form:
    table_name = form['criterion'].value
else:
    pass
year = ""
if table_name == "ACT":
    year = form['ACTgroup'].value
elif table_name == "SAT":
    year = form['SATgroup'].value
elif table_name == "SCHOOL_ENROLLMENT":
    year = form['enrollyear'].value
elif table_name == "SCHOOL_ETHNICITY_LOW_INCOME":
    year = form['incomeyear'].value
elif table_name == "SCHOOL_SERIOUS_INCIDENTS":
    year = form['incidentyear'].value
elif table_name == "SCHOOL_SUSPENSIONS":
    year = form['suspensionyear'].value

print "Content-Type: text/html\r\n\r\n"
print """\
<html>
  <head>
    <title>Edify</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <link href="../../Edify/edify.css" rel="stylesheet" type="text/css" />
    <script type="text/javascript">
function initialize() {
  var mapOptions = {
    zoom: 10,
    center: new google.maps.LatLng(39.9522, -75.1642),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

  if(typeof initializeSub != "undefined"){// call back
    initializeSub();
  }
}
function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyCsjSv8WvxzS2BrJiEvU4hg6jKNqAuHoNk&sensor=false&callback=initialize";
  document.body.appendChild(script);
}
function createMarker(lat, lng, myHtml) { if(!map) return;
  var latlng=new google.maps.LatLng(0.0000000000000001+lat,0.0000000000000001+lng),
        marker = new google.maps.Marker({position:latlng, map:map}),
        infowindow = new google.maps.InfoWindow({content:myHtml + lat +', '+ lng});
  google.maps.event.addListener(marker,"click", function() { infowindow.open(marker.get('map'), marker); });
}
if(window.attachEvent){//MS
    window.attachEvent('onload',loadScript);
}else if(window.addEventListener){
    window.addEventListener('load',loadScript,false);
}else{
    window.onload=loadScript;
}

var sections = {
    'ACT': 'ACT',
    'SAT': 'SAT',
    'SCHOOL_ENROLLMENT': 'SCHOOL_ENROLLMENT',
    'SCHOOL_ETHNICITY_LOW_INCOME': 'SCHOOL_ETHNICITY_LOW_INCOME',
    'SCHOOL_SERIOUS_INCIDENTS': 'SCHOOL_SERIOUS_INCIDENTS',
    'SCHOOL_SUSPENSIONS': 'SCHOOL_SUSPENSIONS'
};


var selection = function(select) {
    for(i in sections)
        document.getElementById(sections[i]).style.display = "none";

    document.getElementById(sections[select.value]).style.display = "block";
}
</script>
"""
print """\
  </head>
  <body>
     <div id = "content">
        <div id = "header">
            <div id = "logo"><img src="../../Edify/images/edify.png" width="164" height="91" alt="Edify" /></div>
        </div>


     <div id = "stuff">
        <div id = "searchform">
            <form action="../../cgi-bin/index.py"  name="SearchForm">	<div id="dropdown">
        <label for="search">Locate Schools:</label><br/>
        <select id="criterion" name = "criterion"  onchange="selection(this);">
            <option value="None">None</option>
            <option value="ACT">ACT Scores</option>
            <option value="SAT">SAT Scores</option>
            <option value="SCHOOL_ENROLLMENT">Enrollment</option>
            <option value="SCHOOL_ETHNICITY_LOW_INCOME">Income</option>
            <option value="SCHOOL_INFORMATION">Information</option>
            <option value="SCHOOL_SERIOUS_INCIDENTS">Incidents</option>
            <option value="SCHOOL_SUSPENSIONS">Suspensions</option>
        </select>
    </div>

    <div id="ACT" class = "hidden" style="display:none;">
        Select a year:<br>
        <label for="2010">2010</label><input type="radio" value = "2010"  name = "ACTgroup">
        <label for="2011">2011</label><input type="radio" value = "2011"  name = "ACTgroup">
    </div>


    <div id="SAT" class = "hidden" style="display:none;">
     Select a year:<br>
       <div><label for="2009">2009</label><input type="radio" value = "2009"  name = "SATgroup"></div>
       <div><label for="2010">2010</label><input type="radio" value = "2010"  name = "SATgroup"></div>
       <div><label for="2011">2011</label><input type="radio" value = "2011"  name = "SATgroup"></div>
       <div><label for="2012">2012</label><input type="radio" value = "2012"  name = "SATgroup"></div>
    </div>


    <div id="SCHOOL_ENROLLMENT" class = "hidden" style="display:none;">
    Pick Enrollment Year:<br/>
         <select id="enrollyear" name = "enrollyear">
            <option value="2008-2009">2008 - 2009</option>
            <option value="2009-2010">2009 - 2010</option>
            <option value="2010-2011">2010 - 2011</option>
            <option value="2011-2012">2011 - 2012</option>
            <option value="2012-2013">2012 - 2013</option>
        </select>
    </div>

    <div id="SCHOOL_ETHNICITY_LOW_INCOME" class = "hidden" style="display:none;">
         Pick Income Year:<br/>
         <select id="incomeyear" name = "incomeyear">
            <option value="2008-2009">2008 - 2009</option>
            <option value="2009-2010">2009 - 2010</option>
            <option value="2010-2011">2010 - 2011</option>
            <option value="2011-2012">2011 - 2012</option>
            <option value="2012-2013">2012 - 2013</option>
        </select>
    </div>
    <div id="SCHOOL_SERIOUS_INCIDENTS" class = "hidden" style="display:none;">
         Pick a Year:<br/>
         <select id="incidentyear" name = "incidentyear">
            <option value="2008-2009">2008 - 2009</option>
            <option value="2009-2010">2009 - 2010</option>
            <option value="2010-2011">2010 - 2011</option>
            <option value="2011-2012">2011 - 2012</option>
        </select>
    </div>
    <div id="SCHOOL_SUSPENSIONS" class = "hidden" style="display:none;">
             Pick a Year:<br/>
         <select id="suspensionyear" name="suspensionyear">
            <option value="2008-2009">2008 - 2009</option>
            <option value="2009-2010">2009 - 2010</option>
            <option value="2010-2011">2010 - 2011</option>
            <option value="2011-2012">2011 - 2012</option>
        </select>
    </div>
<input type="submit" id = "submitbutton" value = "Submit Query">
  <br>
</form>

        </div>

        <div id = "map-canvas">
        </div>

     </div>
    </div>
"""
print """\
<script type="text/javascript">
      function initializeSub(){
"""
select(table_name, year)
print """\
}
</script>
  </body>
</html>
"""
