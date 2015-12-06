# -*- coding: utf-8 -*-
# !/bin/env python
import sqlite3

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









