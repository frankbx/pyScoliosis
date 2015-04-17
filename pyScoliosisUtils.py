# -*- coding: utf-8 -*-
# !/bin/env python
import sqlite3

from xlwt import Workbook
from xlrd import *

PATIENT_ID = 0
DISTRICT = 1
SCHOOL = 2
CLASS = 3
GRADE = 4
NAME = 5
GENDER = 6
DOB = 7
CONTACT_INFO = 8
HEIGHT = 9
WEIGHT = 10
MEASURED_ANGLE = 11
FAT = 12
FAT_PERCENTAGE = 13
BMI = 14
FAT_TYPE = 15
BASIC_METABOLISM = 16
XRAYNUM = 17
COBBSECTION = 18
COBBDEGREE = 19
IS_CHECKED = 20
ID = 21

column_labels = [u"编号", u"区域", u"学校", u"年级", u"班级", u"姓名", u"性别", u"生日", u"家长手机", u"身高", u"体重", u"测量角度", u"脂肪判断",
                 u"脂肪含量",
                 u"BMI指数",
                 u"肥胖类型", u"基础代谢", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查"]

column_nums = [1, 0, 10, 11, 12, 2, 7, 9, 3, 82, 83, 6, 80, 81]

CREATE_PATIENT_TABLE = """CREATE TABLE IF NOT EXISTS [patients] (
                          [patient_id] INTEGER,
                          [district] NVARCHAR(10)  NULL,
                          [school] NVARCHAR(20)  NULL,
                          [grade] INTEGER  NULL,
                          [class_name] INTEGER  NULL,
                          [name] NVARCHAR(10)  NOT NULL,
                          [gender] NVARCHAR(1) NULL ,
                          [dob] INTEGER NULL ,
                          [contact_info] INTEGER  NULL,
                          [height] FLOAT NULL ,
                          [weight] FLOAT NULL,
                          [fat] NVARCHAR(10) NULL,
                          [fat_percentage] FLOAT NULL,
                          [bmi] FLOAT NULL ,
                          [fat_type] NVARCHAR(10) NULL,
                          [basic_metabolism] INTEGER NULL,
                          [measured_angle] NVARCHAR(10)  NULL,
                          [xraynum] INTEGER  NULL,
                          [cobbsection] NVARCHAR(10)  NULL,
                          [cobbdegree] INTEGER  NULL,
                          [is_checked] BOOLEAN  NULL,
                          [id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT)"""

INSERT_INTO_PATIENT = """INSERT INTO [patients] (patient_id, district, school,grade,class_name,  [name], gender,dob, contact_info,height,weight,measured_angle, fat,fat_percentage, bmi, fat_type,basic_metabolism)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

INSERT_INTO_PATIENTS = """ INSERT INTO [patients] (patient_id, district, school,grade,class_name,  [name], gender,dob, contact_info,height,weight,measured_angle, fat,fat_percentage, bmi, fat_type,basic_metabolism)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

SELECT_ALL_PATIENT = """SELECT patient_id, district, school,grade, class_name,[name],gender,dob, contact_info, height, weight,measured_angle, fat,fat_percentage, bmi, fat_type,basic_metabolism, xraynum, cobbsection, cobbdegree, is_checked, id FROM patients """

CHECK_PATIENT = """ UPDATE patients SET xraynum = ?, cobbsection =? , cobbdegree =?, is_checked = 1 WHERE id = ?"""
DB_NAME = "data.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_PATIENT_TABLE)
    conn.commit()
    conn.close()


def load_all_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(SELECT_ALL_PATIENT)
    data = cursor.fetchall()
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
    # for each in conditions.keys():
    where = unicode(where + " name " + ' LIKE "%' + conditions["[name]"] + '%"')
    # print where[:-3]
    sql = unicode(sql + where)
    # print sql
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return [list(i) for i in data]


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
    # print filename
    book = open_workbook(filename)
    sheet = book.sheet_by_index(0)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # print sheet.nrows
    for i in range(1, sheet.nrows):
        cursor.execute(INSERT_INTO_PATIENT, read_value(sheet, i))
    conn.commit()
    conn.close()
    read_value(sheet, 1)


def get_gender(i):
    gender = [u'男', u'女']
    return gender[i - 1]


def get_fat(i):
    fatness = [u'低', u'标准', u'偏高', u'高']
    return fatness[i - 1]


def get_fat_type(i):
    fat_type = [u'消瘦', u'标准', u'隐藏性肥胖', u'肥胖', u'肌肉性肥胖']
    return fat_type[i - 1]


def read_value(sheet, row):
    l = [''] * 17
    l[PATIENT_ID] = row
    l[DISTRICT] = unicode(sheet.cell(row, 0).value)
    l[SCHOOL] = unicode(sheet.cell(row, 1).value)
    l[CLASS] = sheet.cell(row, 2).value
    l[GRADE] = sheet.cell(row, 3).value
    l[NAME] = unicode(sheet.cell(row, 4).value)
    l[GENDER] = get_gender(int(sheet.cell(row, 5).value))
    l[DOB] = sheet.cell(row, 6).value
    l[CONTACT_INFO] = sheet.cell(row, 7).value
    l[HEIGHT] = sheet.cell(row, 8).value
    l[WEIGHT] = sheet.cell(row, 9).value
    l[MEASURED_ANGLE] = get_measured_angle(sheet.cell(row, 10).value)
    l[FAT] = get_fat(int(sheet.cell(row, 11).value))
    l[FAT_PERCENTAGE] = float(sheet.cell(row, 12).value)
    l[BMI] = float(sheet.cell(row, 13).value)
    l[FAT_TYPE] = get_fat_type(int(sheet.cell(row, 14).value))
    l[BASIC_METABOLISM] = int(sheet.cell(row, 15).value)

    return tuple(l)


def get_measured_angle(s):
    # print s
    v = str(s)
    if v.isdigit():
        return int(v)
    if '.' in v:
        return max([int(x) for x in v.split('.')])
    if ',' in v:
        return max([int(x) for x in v.split(',')])
    return 0