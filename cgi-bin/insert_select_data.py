#!/usr/bin/python

import csv
import MySQLdb
from numpy import array, ones, linalg

""" Parse the CSV's for populating the tables """


def parse_load_csv(fname, table_name, year=None):
    """ Loads the data CSV into a table in the database.
    Warnings will be thrown when there is missing data from the data sets when
    the column types are not satisfied with ''. (ex. null into FLOAT column)
    """
    mydb = MySQLdb.connect(host='localhost', user='root', passwd='', db='CIS192')
    cursor = mydb.cursor()
    with open(fname) as file_object:
        reader = csv.reader(file_object, delimiter=",")
        # only use non-empty fields ex. x,y,,, => x,y
        valid_fields = slice(0, len(filter(bool, reader.next())))
        for line in reader:
            # remove '*' placeholders for missing data
            cleaned_data = [data.strip().replace('*', '') for data in line][valid_fields]
            if(year is not None):
                cleaned_data.append(year)  # add year for SAT and ACT
            placeholders = ','.join('%s' for data in cleaned_data)
            # generate placeholders for our data
            query_string = """INSERT INTO %s VALUES (%s);""" \
                           % (table_name, placeholders)
            cursor.execute(query_string, cleaned_data)  # execute query
    try:
        mydb.commit()
    except:
        mydb.rollback()
    cursor.close()

    # disconnect from server
    mydb.close()


def select(table_name, year=None):
    """ Selects data from tables by year. If year is not specified, it will
    make it a certain year. """
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "", "CIS192")

    # prepare a cursor object
    cursor = db.cursor()

    # in case year is not specified use the last guaranteed year we have
    if year is None and table_name == "SAT":
        year = "2012"
    elif year is None and table_name == "ACT":
        year = "2011"
    elif year is None and table_name != "SCHOOL_INFORMATION":
        year = "2011-2012"
    # Prepare SQL query to SELECT based on table and year
    if table_name == "SAT":  # calculate total because was not in csv
        sql = "SELECT A.*, SUM(VERBAL + MATHEMATICS + WRITING) as Total, \
        B.LATITUDE, B.LONGITUDE \
        FROM SAT as A, SCHOOL_LOCATIONS as B\
        WHERE LOWER(A.SCHOOL) = LOWER(B.SCHOOL_NAME) and A.YEAR = %s\
        GROUP BY SCHOOL_CODE" \
        % (year)
    elif table_name == "ACT":  # calculate total because was not in csv
        sql = "SELECT A.*, B.LATITUDE, B.LONGITUDE \
        FROM ACT as A, SCHOOL_LOCATIONS as B\
        WHERE LOWER(A.SCHOOL) = LOWER(B.SCHOOL_NAME) and A.YEAR = %s\
        GROUP BY SCHOOL_CODE" \
        % (year)
    elif table_name != "SCHOOL_INFORMATION":
        # all other tables besides SCHOOL_INFORMATION has year
        sql = "SELECT A.*, B.LATITUDE, B.LONGITUDE\
        FROM %s as A, SCHOOL_LOCATIONS as B\
        WHERE LOWER(A.SCHOOL_CODE) = LOWER(B.SCHOOL_CODE) and A.SCHOOL_YEAR = \
        '%s'" % (table_name, year)
    else:  # for SCHOOL_INFORMATION (no year)
        sql = "SELECT A.*, B.LATITUDE, B.LONGITUDE\
        FROM %s as A, SCHOOL_LOCATIONS as B\
        WHERE LOWER(A.SCHOOL_CODE) = LOWER(B.SCHOOL_CODE)" % (table_name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        field_names = [i[0] for i in cursor.description]
        for row in results:
            # make strings like field_name: value
            named = [": ".join([str(n), str(r)+r"<br>"]) for n, r in
                     zip(field_names, row)[0:-2]]
            # calculate total trend for SAT
            if(table_name == "SAT"):  # calculate trend information for SAT
                if get_SAT_trend(row[2]) is not None:
                    named.append("Trend in total score per year: "
                                 + get_SAT_trend(row[2])+r"<br>")
            # turn all information into a string to put in the createMarker
            info = "".join(named)
            p_string = "createMarker(%f,%f,'%s');" % (row[-2], row[-1], info)
            if row is not None:
                print p_string
                # print out to webpage to call javascript function with python
                # generated info
    except:
        print "Error: unable to fetch data"
    cursor.close()
    # disconnect from server
    db.close()


def get_SAT_trend(schoolcode):
    """ Calculate SAT total score trend (aka slope) across the years we
    have data for"""
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "", "CIS192")

    # prepare a cursor object
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT SCHOOL_CODE, (VERBAL + MATHEMATICS + WRITING) \
        AS TOTAL_SCORE, YEAR \
        FROM SAT \
        WHERE SCHOOL_CODE = %s \
        ORDER BY YEAR" % (schoolcode)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        x = [int(result[2]) for result in results]
        A = array([x, ones(len(results))])
        y = [result[1] for result in results]
        w = linalg.lstsq(A.T, y)[0]
        return str(w[0])  # the slope
    except:
        print "Error: unable to fetch data"

    cursor.close()
    # disconnect from server
    db.close()
