#!/usr/bin/python

import MySQLdb


def create_tables():
    """ Creates the tables in the database. We do this explicitly because a lot
    of the columns in the original dataset do not necessarily match those found
    other files. This is to try to keep similar naming between table.
    (Ex. SCHOOL_CODE)
    """
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "", "CIS192")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS ACT")
    cursor.execute("DROP TABLE IF EXISTS SAT")
    cursor.execute("DROP TABLE IF EXISTS SCHOOL_ENROLLMENT")
    cursor.execute("DROP TABLE IF EXISTS SCHOOL_ETHNICITY_LOW_INCOME")
    cursor.execute("DROP TABLE IF EXISTS SCHOOL_INFORMATION")
    cursor.execute("DROP TABLE IF EXISTS SCHOOL_SERIOUS_INCIDENTS")
    cursor.execute("DROP TABLE IF EXISTS SCHOOL_SUSPENSIONS")
    cursor.execute("DROP TABLE IF EXISTS SCHOOL_LOCATIONS")

    # Create table as per requirement
    sql = """CREATE TABLE ACT (
        AUN INT,
        DISTRICT  VARCHAR(50),
        SCHOOL_CODE INT NOT NULL,
        SCHOOL VARCHAR(50) NOT NULL,
        ENGLISH_NUMBER_TESTED INT,
        ENGLISH_AVERAGE_SCORE FLOAT,
        MATH_NUMBER_TESTED INT,
        MATH_AVERAGE_SCORE FLOAT,
        SCIENCE_NUMBER_TESTED INT,
        SCIENCE_AVERAGE_SCORE FLOAT,
        READING_NUMBER_TESTED INT,
        READING_AVERAGE_SCORE FLOAT,
        COMPOSITE_NUMBER_TESTED INT,
        COMPOSITE_AVERAGE_SCORE FLOAT,
        ENGLISH_WRITING_NUMBER_TESTED INT,
        ENGLISH_WRITING_AVERAGE_SCORE FLOAT,
        WRITING_SUBSCORE_NUMBER_TESTED INT,
        WRITING_SUBSCORE_AVERAGE_SCORE FLOAT,
        YEAR INT NOT NULL,
        primary key(SCHOOL_CODE, YEAR, SCHOOL)
        )"""
        # primary key includes SCHOOL because SCHOOL_CODE and YEAR is not
        # unique for this data set

    cursor.execute(sql)

    # Create table as per requirement
    sql = """CREATE TABLE SAT (
       AUN INT,
       SCHOOL_DISTRICT VARCHAR(55),
       SCHOOL_CODE INT NOT NULL,
       SCHOOL VARCHAR(55) NOT NULL,
       NUMBER_OF_STUDENTS_TESTED INT,
       VERBAL FLOAT,
       MATHEMATICS FLOAT,
       WRITING FLOAT,
       YEAR INT NOT NULL,
       primary key(SCHOOL_CODE, YEAR, SCHOOL)
       )"""
       # primary key includes SCHOOL because SCHOOL_CODE and YEAR is not unique
       # for this data set

    cursor.execute(sql)

    sql = """CREATE TABLE SCHOOL_ENROLLMENT (
       SCHOOL_CODE INT NOT NULL,
       SCHOOL_YEAR CHAR(9) NOT NULL,
       SCH_ATTENDANCE FLOAT,
       SCH_ENROLLMENT INT,
       SCH_STUDENT_ENTERED INT,
       SCH_STUDENT_WITHDREW INT,
       primary key(SCHOOL_CODE, SCHOOL_YEAR)
       )"""

    cursor.execute(sql)

    sql = """CREATE TABLE SCHOOL_ETHNICITY_LOW_INCOME (
       SCHOOL_CODE INT NOT NULL,
       SCHOOL_YEAR CHAR(9) NOT NULL,
       AFRICAN_AMERICAN FLOAT,
       WHITE FLOAT,
       ASIAN FLOAT,
       LATINO FLOAT,
       OTHER FLOAT,
       PACIFIC_ISLANDER FLOAT,
       AMERICAN_INDIAN FLOAT,
       SCH_LOW_INCOME_FAMILY FLOAT,
       primary key(SCHOOL_CODE, SCHOOL_YEAR)
       )"""

    cursor.execute(sql)

    sql = """CREATE TABLE SCHOOL_INFORMATION (
       SCHOOL_CODE INT,
       SCHOOL_NAME_1 VARCHAR(30),
       SCHOOL_NAME_2 VARCHAR(30),
       ADDRESS VARCHAR(30),
       SCHOOL_ZIP INT,
       ZIP_PLUS_4 VARCHAR(10),
       CITY VARCHAR(30),
       STATE_CD CHAR(2),
       PHONE_NUMBER VARCHAR(12),
       SCH_START_GRADE INT,
       SCH_TERM_GRADE INT,
       HPADDR VARCHAR(55),
       SCHOOL_LEVEL_NAME VARCHAR(30),
       primary key(SCHOOL_CODE)
       )"""

    cursor.execute(sql)

    sql = """CREATE TABLE SCHOOL_SERIOUS_INCIDENTS (
       SCHOOL_CODE INT,
       SCHOOL_YEAR CHAR(9),
       ASSAULT INT,
       DRUG INT,
       MORALS INT,
       WEAPONS INT,
       THEFT INT,
       primary key(SCHOOL_CODE, SCHOOL_YEAR)
       )"""

    cursor.execute(sql)

    sql = """CREATE TABLE SCHOOL_SUSPENSIONS (
       SCHOOL_CODE INT,
       SCHOOL_YEAR CHAR(9),
       TOTAL_SUSPENSIONS INT,
       SCH_ONE_TIME_SUSP INT,
       SCH_TWO_TIME_SUSP INT,
       SCH_THREE_TIME_SUSP INT,
       SCH_MORE_THAN_THREE_SUSP INT,
       primary key(SCHOOL_CODE, SCHOOL_YEAR)
       )"""

    cursor.execute(sql)

    sql = """CREATE TABLE SCHOOL_LOCATIONS (
       SCHOOL_CODE INT,
       LATITUDE FLOAT,
       LONGITUDE FLOAT,
       SCHOOL_NAME VARCHAR(55),
       primary key(SCHOOL_CODE)
       )"""

    cursor.execute(sql)

    # disconnect from server
    db.close()
