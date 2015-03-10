# -*- coding: utf-8 -*-
# !/bin/env python
import sqlite3

from xlwt import Workbook

PATIENT_ID = 0
DISTRICT = 1
SCHOOL = 2
CLASS = 3
GENDER = 5
NAME = 4
CONTACT_INFO = 6
MEASURED_ANGLE = 7
XRAYNUM = 8
COBBSECTION = 9
COBBDEGREE = 10
IS_CHECKED = 11
ID = 12

column_labels = [u"编号", u"区域", u"学校", u"班级", u"性别", u"姓名", u"联系方式", u"测量角度", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查"]

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
                          [gender] NVARCHAR(1) NULL,
                          [id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT)"""

INSERT_INTO_PATIENT = """ INSERT INTO patients (patient_id, district, school,class, gender, [name], contact_info,measured_angle,xraynum, cobbsection, cobbdegree, is_checked)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?) """

SELECT_ALL_PATIENT = """SELECT patient_id, district, school,class, gender, [name], contact_info,measured_angle,xraynum, cobbsection, cobbdegree, is_checked, id FROM patients """

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
            i[PATIENT_ID], i[DISTRICT], i[SCHOOL], i[CLASS], i[GENDER], i[NAME], i[CONTACT_INFO],
            i[MEASURED_ANGLE],
            i[XRAYNUM], i[COBBSECTION], i[COBBDEGREE], i[IS_CHECKED]))
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


def execute_query(conditions):
    sql = SELECT_ALL_PATIENT
    where = " WHERE "
    for each in conditions.keys():
        where = unicode(where + " " + each + " = " + '"' + conditions[each] + '" AND')
    print where[:-3]
    sql = unicode(sql + where[:-3])
    print sql
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return [list(i) for i in data]


def dummy_data():
    data = []
    for i in range(0, 600):
        it = str(i + 1)
        p = [i + 1, "district " + it, "school " + it, "class " + it, u"姓名 " + it, u"男",
             "contact information ********************* " + it, "measured angle " + it, "", "", "", False]
        # print p
        data.append(p)
    return data


def export_to_excel(filename, data):
    print filename
    print len(data)
    book = Workbook()
    sheet = book.add_sheet(u"病人信息")
    for i in range(0, len(column_labels)):
        sheet.row(0).write(i, column_labels[i])

    for x in range(0, len(data)):
        for y in range(0, len(column_labels)):
            sheet.row(x + 1).write(y, data[x][y])

    book.save(filename)