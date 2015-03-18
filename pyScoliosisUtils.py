# -*- coding: utf-8 -*-
# !/bin/env python
import sqlite3

from xlwt import Workbook
from xlrd import open_workbook

PATIENT_ID = 0
DISTRICT = 1
SCHOOL = 2
CLASS = 3
NAME = 4
GENDER = 5
DOB = 6
CONTACT_INFO = 7
HEIGHT = 8
WEIGHT = 9
FAT = 10
FAT_PERCENTAGE = 11
BMI = 12
FAT_TYPE = 13
BASIC_METABOLISM = 14
MEASURED_ANGLE = 15
XRAYNUM = 16
COBBSECTION = 17
COBBDEGREE = 18
IS_CHECKED = 19
ID = 20

column_labels = [u"编号", u"区域", u"学校", u"年级", u"班级", u"姓名", u"性别", u"生日", u"联系方式", u"身高", u"体重", u"脂肪判断", u"脂肪含量",
                 u"BMI指数",
                 u"肥胖类型", u"基础代谢", u"测量角度", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查"]

column_nums = [1, 0, 10, 11, 12, 2, 7, 9, 3, 82, 83, 80, 81]

CREATE_PATIENT_TABLE = """CREATE TABLE IF NOT EXISTS [patients] (
                          [patient_id] NVARCHAR(20)  UNIQUE NOT NULL,
                          [district] NVARCHAR(10)  NULL,
                          [school] NVARCHAR(20)  NULL,
                          [grade] NVARCHAR(10)  NULL,
                          [class_name] NVARCHAR(10)  NULL,
                          [name] NVARCHAR(10)  NOT NULL,
                          [gender] NVARCHAR(1) NULL ,
                          [dob] DATE NULL ,
                          [contact_info] TEXT  NULL,
                          [height] INTEGER NULL ,
                          [weight] FLOAT NULL,
                          [fat] NVARCHAR(10) NULL,
                          [fat_percentage] FLOAT NULL,
                          [bmi] FLOAT NULL ,
                          [fat_type] NVARCHAR(10) NULL,
                          [basic_metabolism] FLOAT NULL,
                          [measured_angle] NVARCHAR(10)  NULL,
                          [xraynum] NVARCHAR(10)  NULL,
                          [cobbsection] NVARCHAR(10)  NULL,
                          [cobbdegree] NVARCHAR(10)  NULL,
                          [is_checked] BOOLEAN  NULL,
                          [id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT)"""

INSERT_INTO_PATIENT = """ INSERT INTO [patients] (patient_id, district, school, grade, class_name, [name], gender, dob, contact_info, height, weight, cobbsection, cobbdegree)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) """

INSERT_INTO_PATIENTS = """ INSERT INTO [patients] (patient_id, district, school,grade,class_name,  [name], gender,dob, contact_info,height,weight,cobbsection, cobbdegree)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

SELECT_ALL_PATIENT = """SELECT patient_id, district, school,grade, class_name,[name],gender,dob, contact_info, height, weight, fat,fat_percentage, bmi, fat_type,basic_metabolism, measured_angle,xraynum, cobbsection, cobbdegree, is_checked, id FROM patients """

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
            i[PATIENT_ID], i[DISTRICT], i[SCHOOL], i[CLASS], i[NAME], i[GENDER], i[CONTACT_INFO],
            i[MEASURED_ANGLE],
            i[XRAYNUM], i[COBBSECTION], i[COBBDEGREE], i[IS_CHECKED]))
    conn.commit()
    conn.close()


def load_all_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(SELECT_ALL_PATIENT)
    data = []
    # cursor.row_factory = sqlite3.Row
    # for row in cursor:
    # for key in Patient.__dict__:
    # pass
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
    # print where[:-3]
    sql = unicode(sql + where[:-3])
    # print sql
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
    # print filename
    # print len(data)
    book = Workbook()
    sheet = book.add_sheet(u"病人信息")
    for i in range(0, len(column_labels)):
        sheet.row(0).write(i, column_labels[i])

    for x in range(0, len(data)):
        for y in range(0, len(column_labels)):
            sheet.row(x + 1).write(y, data[x][y])

    book.save(filename)


def import_from_excel(filename):
    book = open_workbook(filename)
    sheet = book.sheet_by_index(0)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # for i in range(5:sheet.nrows):
    # cursor.execute(INSERT_INTO_PATIENT, get_value_tuple(sheet, i))
    sql = INSERT_INTO_PATIENTS % get_value_tuple(sheet, 3)
    print sql
    cursor.execute(sql)
    # cursor.execute(INSERT_INTO_PATIENT, (
    # s(sheet, 5, 0), s(sheet, 5, 1), s(sheet, 5, 2), s(sheet, 5, 3), s(sheet, 5, 4), s(sheet, 5, 5), s(sheet, 5, 6),
    #     s(sheet, 5, 7), s(sheet, 5, 8), s(sheet, 5, 9), s(sheet, 5, 10), s(sheet, 5, 11), s(sheet, 5, 12)))
    conn.commit()
    conn.close()
    # for i in range(sheet.nrows):
    # print INSERT_INTO_PATIENTS % get_value_tuple(sheet, i)


def get_gender(i):
    gender = [u'男', u'女']
    return gender[i - 1]


def s(sheet, row, i):
    return sheet.cell(row, column_nums[i]).value


def get_value_tuple(sheet, row):
    l = []
    for x in column_nums:
        l.append(sheet.cell(row, x).value)
    return tuple(l)