#!/usr/bin/python

from createTable import create_tables
from insert_select_data import parse_load_csv
from get_lat_long import get_location

""" Parse the CSV's for populating the tables """


def main():
    """ Controls the loading of the database and its tables """

    create_tables()  # create database tables
    # loads csvs into table
    parse_load_csv("./CSV_Input/SCHOOL_INFORMATION.csv", "SCHOOL_INFORMATION")
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
    get_location()  # gets lat long for each school for markers

if __name__ == "__main__":
    # calls main() if we have run this with 'python load_db.py'
    main()
    print "Loaded"
