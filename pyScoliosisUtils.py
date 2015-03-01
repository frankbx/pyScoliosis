# -*- coding: utf-8 -*-
# !/bin/env python
import pickle

import sqlite3

PATIENT_ID = 0
DISTRICT = 1
SCHOOL = 2
CLASS = 3
STUDENT_NUM = 4
NAME = 5
CONTACT_INFO = 6
MEASURED_ANGLE = 7
XRAYNUM = 8
COBBSECTION = 9
COBBDEGREE = 10
IS_CHECKED = 11
GROUP = 12
ID = 13

CREATE_PATIENT_TABLE = """CREATE TABLE IF NOT EXISTS [patients] (
                          [patient_id] nvARCHAR(20)  UNIQUE NOT NULL,
                          [district] nvARCHAR(10)  NULL,
                          [school] nvARCHAR(20)  NULL,
                          [class] nvARCHAR(10)  NULL,
                          [student_num] nvARCHAR(10)  NULL,
                          [name] NVARCHAR(10)  NOT NULL,
                          [contact_info] TEXT  NULL,
                          [measured_angle] NVARCHAR(10)  NULL,
                          [xraynum] NVARCHAR(10)  NULL,
                          [cobbsection] NVARCHAR(10)  NULL,
                          [cobbdegree] NVARCHAR(10)  NULL,
                          [is_checked] BOOLEAN  NULL,
                          [group] nvARCHAR(10)  NULL,
                          [id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT)"""

INSERT_INTO_PATIENT = """ INSERT INTO patients (patient_id, district, school,class, student_num, [name], contact_info,measured_angle,xraynum, cobbsection, cobbdegree, is_checked,[group])
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) """

SELECT_ALL_PATIENT = """SELECT patient_id, district, school,class, student_num, [name], contact_info,measured_angle,xraynum, cobbsection, cobbdegree, is_checked,[group], id FROM patients"""

CHECK_PATIENT = """ UPDATE patients SET xraynum = ?, cobbsection =? , cobbdegree =?, is_checked = 1 WHERE id = ?"""
DB_NAME = "data.dat"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_PATIENT_TABLE)
    conn.commit()
    conn.close()


def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    dummy = dummy_data()
    for i in dummy:
        cursor.execute(INSERT_INTO_PATIENT, (
            i[PATIENT_ID], i[DISTRICT], i[SCHOOL], i[CLASS], i[STUDENT_NUM], i[NAME], i[CONTACT_INFO],
            i[MEASURED_ANGLE],
            i[XRAYNUM], i[COBBSECTION], i[COBBDEGREE], i[IS_CHECKED], i[GROUP]))
        conn.commit()
    conn.close()


def load_all_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(SELECT_ALL_PATIENT)
    data = cursor.fetchall()
    # print type(data)
    # print type((data)[0])
    conn.close()
    return [list(i) for i in data]


def update_patient_data(patient):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CHECK_PATIENT, (patient[XRAYNUM], patient[COBBSECTION], patient[COBBDEGREE], patient[ID]))
    # print (patient[XRAYNUM], patient[COBBSECTION], patient[COBBDEGREE], patient[ID])
    conn.commit()
    conn.close()


def save_data(data, filename="data.pickle"):
    try:
        with open(filename, 'wb') as savedata:
            pickle.dump(data, savedata)
        print "data saved!"
    except IOError as ierr:
        print("File Error: " + str(ierr))
    except pickle.PickleError as perr:
        print("Pickle Error: " + str(perr))


def dummy_data():
    data = []
    for i in range(0, 600):
        it = str(i + 1)
        p = [i + 1, "district " + it, "school " + it, "class " + it, "student number " + it, u"姓名 " + it,
             "contact information ********************* " + it, "measured angle " + it, "", "", "", False,
             "A"]
        # print p
        data.append(p)
    return data
