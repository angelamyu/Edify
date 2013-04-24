#!/usr/bin/python

import MySQLdb
import requests
import urllib
import time

""" Parse the CSV's for populating the tables """


def get_addresses():
    """ Gets all addresses from the SCHOOL_INFORMATION table """
    db = MySQLdb.connect("localhost", "root", "", "CIS192")

    # prepare a cursor object
    cursor = db.cursor()

    # Prepare SQL query to select all schools in school info
    sql = " SELECT SCHOOL_CODE, ADDRESS , CITY, STATE_CD, SCHOOL_ZIP,\
    SCHOOL_NAME_1 FROM SCHOOL_INFORMATION;"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        addresses = [(row[0], ",".join(row[1:4]), row[5]) for row in results]
        return addresses
    except:
        print "Error: unable to fetch data"

    cursor.close()
    # disconnect from server
    db.close()


def get_location():
    """ Gets location by requesting it from Google's API. Waits a second
    every 4 requests because Google will shut us out if we request too quickly.
    """
    addresses = get_addresses()
    f = open('/var/www/html/hackamaroo/Edify/addresses.txt', 'w')
    for item in addresses:
        f.write("%d\t%s\n" % (item[0], item[1]))
    for i in range(len(addresses)):
        # get lat and long
        latlong = parse_for_lat_long(addresses[i][1])
        schoolcodes = addresses[i][0]
        # add into table
        load_locations_db(schoolcodes, latlong, addresses[i][2])
        if(i % 4 == 0):
            time.sleep(1)


def parse_for_lat_long(addr):
    """ Requests a JSON from Google API and parses it to get latitude and
    longitude.
    """
    param = {'address': addr}
    base_url = "http://maps.googleapis.com/maps/api/geocode/json?address="
    r = requests.get(base_url + urllib.urlencode(param) + '&sensor=false')
    if r.json():
        if 'OK' not in r.json()['status']:
            print base_url + urllib.urlencode(param) + '&sensor=false'
            raise Exception(r.json()['status'])
        location = r.json()['results'][0]['geometry']['location']
        return (location['lat'], location['lng'])


def load_locations_db(schoolcode, latlong, sname):
    """ Loads a location into the SCHOOL_LOCATIONS table. """
    # Open database connection
    mydb = MySQLdb.connect("localhost", "root", "", "CIS192")

    # prepare a cursor object
    cursor = mydb.cursor()

    placeholders = ','.join('%s' for i in range(4))
    uncompress = [schoolcode, latlong[0], latlong[1], sname]
    # generate placeholders for our data
    query_string = """INSERT INTO %s VALUES (%s);""" \
                   % ("SCHOOL_LOCATIONS", placeholders)
    cursor.execute(query_string, uncompress)  # execute query
    try:
        mydb.commit()
    except:
        mydb.rollback()
    cursor.close()

    # disconnect from server
    mydb.close()
