#!/usr/bin/python

import nose
import MySQLdb
from createTable import create_tables
from insert_select_data import parse_load_csv, get_SAT_trend
from get_lat_long import get_location, get_addresses
from nose.tools import eq_


# Parse the CSV's for populating the tables

def test_create_tables():
    """Placing most tests here to try to avoid Google's request limit
    by making sure get_locations() is only called once and that all
    other tables are filled before calling get_locations().
    """

    create_tables()
    mydb = MySQLdb.connect(host='localhost', user='root', passwd='',
                           db='CIS192')
    cursor = mydb.cursor()
    sql = "SHOW TABLES;"
    cursor.execute(sql)
    tables = cursor.fetchall()
    eq_(len(tables), 8)
    assert ('ACT',) in tables, "ACT should be a table"
    assert ('SAT',) in tables, "SAT should be a table"
    assert ('SCHOOL_ENROLLMENT',) in tables, \
        "SCHOOL_ENROLLMENT should be a table"
    assert ('SCHOOL_ETHNICITY_LOW_INCOME',) in tables, \
        "SCHOOL_ETHNICITY_LOW_INCOME should be a table"
    assert ('SCHOOL_INFORMATION',) in tables, \
        "SCHOOL_INFORMATION should be a table"
    assert ('SCHOOL_LOCATIONS',) in tables, \
        "SCHOOL_LOCATIONS should be a table"
    assert ('SCHOOL_SERIOUS_INCIDENTS',) in tables, \
        "SCHOOL_SERIOUS_INCIDENTS should be a table"
    assert ('SCHOOL_SUSPENSIONS',) in tables, \
        "SCHOOL_SUSPENSIONS should be a table"
    cursor.close()
    # disconnect from server
    mydb.close()


def test_insert_tables():
    """ To test parse_load_csv which inserts into the db"""
    mydb = MySQLdb.connect(host='localhost', user='root', passwd='',
                           db='CIS192')
    cursor = mydb.cursor()
    parse_load_csv("./CSV_Input/SCHOOL_INFORMATION.csv", "SCHOOL_INFORMATION")
    sql = "SELECT COUNT(1) FROM SCHOOL_INFORMATION;"
    cursor.execute(sql)
    tables = cursor.fetchall()
    eq_((tables)[0][0], 240)

    parse_load_csv("./CSV_Input/SCHOOL_ENROLLMENT.csv", "SCHOOL_ENROLLMENT")
    parse_load_csv("./CSV_Input/SCHOOL_ETHNICITY_LOW_INCOME.csv",
                   "SCHOOL_ETHNICITY_LOW_INCOME")
    parse_load_csv("./CSV_Input/SCHOOL_SERIOUS_INCIDENTS.csv",
                   "SCHOOL_SERIOUS_INCIDENTS")
    parse_load_csv("./CSV_Input/SCHOOL_SUSPENSIONS.csv", "SCHOOL_SUSPENSIONS")
    parse_load_csv("./CSV_Input/ACT_Scores_2010.csv", "ACT", "2010")
    parse_load_csv("./CSV_Input/ACT_Scores_2011.csv", "ACT", "2011")
    parse_load_csv("./CSV_Input/2012_SAT_Scores_Public_Schools_2009.csv",
                   "SAT", "2009")
    parse_load_csv("./CSV_Input/2012_SAT_Scores_Public_Schools_2010.csv",
                   "SAT", "2010")
    parse_load_csv("./CSV_Input/2012_SAT_Scores_Public_Schools_2011.csv",
                   "SAT", "2011")
    parse_load_csv("./CSV_Input/2012_SAT_Scores_Public_Schools_2012.csv",
                   "SAT", "2012")
    cursor.close()
    # disconnect from server
    mydb.close()


def test_get():
    """ tests for get functions """
    mydb = MySQLdb.connect(host='localhost', user='root', passwd='',
                           db='CIS192')
    cursor = mydb.cursor()
    # test get_addresses
    eq_(len(get_addresses()), 240)
    eq_(len(get_addresses()[0]), 3)

    # tests get_location and load_locations_db
    get_location()
    sql = "SELECT COUNT(1) FROM SCHOOL_LOCATIONS;"
    cursor.execute(sql)
    tables = cursor.fetchall()
    eq_((tables)[0][0], 240)

    sql = "SELECT LATITUDE, LONGITUDE  FROM SCHOOL_LOCATIONS \
    WHERE SCHOOL_CODE = 1020;"
    cursor.execute(sql)
    tables = cursor.fetchall()
    assert abs((tables)[0][0] - 39.9523350) < 0.001
    assert abs((tables)[0][1] - -75.16378900000001) < 0.001

    # test get_SAT_trend
    eq_(get_SAT_trend("1100"), "6.5")

    cursor.close()
    # disconnect from server
    mydb.close()


def main():
    """ Our main function """
    print "\n\nRunning unit tests...\n"
    if nose.run(argv=["--with-coverage", "tests.py"]):
        print "\nPassed all unit tests"


if __name__ == "__main__":
    # calls main() if we have run this with 'python load_db.py'
    main()
    print "Finished"
