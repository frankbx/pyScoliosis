# -*- coding: utf-8 -*-
# !/bin/env python
import sqlite3

from xlwt import Workbook
from xlrd import *
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from Models import Patient

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
                 u"脂肪含量", u"BMI指数", u"肥胖类型", u"基础代谢", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查"]

attribute_mapper = {u"编号"     : "id", u"区域": "district", u"学校": 'school', u"年级": 'grade', u"班级": 'class_name',
                    u"姓名"     : 'name', u"性别": 'gender', u"生日": 'dob', u"家长手机": 'contact_info', u"身高": 'height',
                    u"体重"     : 'weight', u"测量角度": 'measured_angle', u"脂肪判断": 'fat',
                    u"脂肪含量"   : 'fat_percentage',
                    u"BMI指数"  : 'bmi',
                    u"肥胖类型"   : 'fat_type', u"基础代谢": 'basic_metabolism', u"X光片号": 'x_ray_num',
                    u"Cobb角节段": 'cobb_section',
                    u"Cobb角度数": 'cobb_degree', u"已复查": 'is_checked'}

column_nums = [1, 0, 10, 11, 12, 2, 7, 9, 3, 82, 83, 6, 80, 81]

INSERT_INTO_PATIENT = """INSERT INTO [patients] (patient_id, district, school,grade,class_name,  [name], gender,dob, contact_info,height,weight,measured_angle, fat,fat_percentage, bmi, fat_type,basic_metabolism)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

INSERT_INTO_PATIENTS = """ INSERT INTO [patients] (patient_id, district, school,grade,class_name,  [name], gender,dob, contact_info,height,weight,measured_angle, fat,fat_percentage, bmi, fat_type,basic_metabolism)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

SELECT_ALL_PATIENT = """SELECT patient_id, district, school,grade, class_name,[name],gender,dob, contact_info, height, weight,measured_angle, fat,fat_percentage, bmi, fat_type,basic_metabolism, x_ray_num, cobb_section, cobb_degree, is_checked, id FROM patients """

CHECK_PATIENT = """ UPDATE patients SET xraynum = ?, cobbsection =? , cobbdegree =?, is_checked = 1 WHERE id = ?"""
DB_NAME = "data.db"


def connect_database():
    engine = create_engine('sqlite:///./data.db')
    metadata = MetaData(engine)
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_database():
    engine = create_engine('sqlite:///./data.db')
    metadata = MetaData(engine)

    patients = Table('patients', metadata,
                     sa.Column('id', sa.Integer(), nullable=False),
                     sa.Column('name', sa.Unicode(length=10), nullable=True),
                     sa.Column('district', sa.Unicode(length=10), nullable=True),
                     sa.Column('school', sa.Unicode(length=20), nullable=True),
                     sa.Column('grade', sa.Unicode(length=20), nullable=True),
                     sa.Column('class_name', sa.Unicode(length=10), nullable=True),
                     sa.Column('gender', sa.Unicode(length=5), nullable=True),
                     sa.Column('dob', sa.Date(), nullable=True),
                     sa.Column('contact_info', sa.Unicode(length=20), nullable=True),
                     sa.Column('height', sa.Float(), nullable=True),
                     sa.Column('weight', sa.Float(), nullable=True),
                     sa.Column('fat', sa.Unicode(length=10), nullable=True),
                     sa.Column('fat_percentage', sa.Float(), nullable=True),
                     sa.Column('bmi', sa.Float(), nullable=True),
                     sa.Column('fat_type', sa.Unicode(length=10), nullable=True),
                     sa.Column('basic_metabolism', sa.Integer(), nullable=True),
                     sa.Column('measured_angle', sa.Float(), nullable=True),
                     sa.Column('x_ray_num', sa.Unicode(), nullable=True),
                     sa.Column('cobb_section', sa.Unicode(length=20), nullable=True),
                     sa.Column('cobb_degree', sa.Float(), nullable=True),
                     sa.Column('is_checked', sa.Boolean(), nullable=True),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('district', 'school', 'grade', 'class_name', 'name', 'gender', 'dob'))
    metadata.create_all()


def load_all_patients():
    session = connect_database()
    data = session.query(Patient).all()
    return data


def update_patient_data(patient):
    session = connect_database()
    session.add(patient)
    session.commit()


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
    gender = [u'男', u'女', u' ']
    if i <= 1:
        return gender[int(i) - 1]
    else:
        return gender[2]


def get_fat(i):
    fatness = [u'低', u'标准', u'偏高', u'高', u'无']
    if i <= 3:
        return fatness[int(i) - 1]
    else:
        return fatness[4]


def get_fat_type(i):
    fat_type = [u'消瘦', u'标准', u'隐藏性肥胖', u'肥胖', u'肌肉性肥胖', u'无']
    if i <= 4:
        return fat_type[int(i) - 1]
    else:
        return fat_type[5]


def read_value(sheet, row):
    l = [''] * 17
    l[PATIENT_ID] = row
    l[DISTRICT] = unicode(sheet.cell(row, 0).value)
    l[SCHOOL] = unicode(sheet.cell(row, 1).value)
    l[CLASS] = sheet.cell(row, 2).value
    l[GRADE] = sheet.cell(row, 3).value
    l[NAME] = unicode(sheet.cell(row, 4).value)
    l[GENDER] = get_gender(sheet.cell(row, 5).value)
    l[DOB] = sheet.cell(row, 6).value
    l[CONTACT_INFO] = sheet.cell(row, 7).value
    l[HEIGHT] = sheet.cell(row, 8).value
    l[WEIGHT] = sheet.cell(row, 9).value
    l[MEASURED_ANGLE] = get_measured_angle(sheet.cell(row, 10).value)
    l[FAT] = get_fat(sheet.cell(row, 11).value)
    l[FAT_PERCENTAGE] = sheet.cell(row, 12).value
    l[BMI] = float(sheet.cell(row, 13).value)
    l[FAT_TYPE] = get_fat_type(sheet.cell(row, 14).value)
    l[BASIC_METABOLISM] = sheet.cell(row, 15).value

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
