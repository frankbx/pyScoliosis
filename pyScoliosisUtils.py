# -*- coding: utf-8 -*-
# !/bin/env python

import unittest

from sqlalchemy import create_engine, MetaData, Table, distinct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from xlwt import Workbook
from xlrd import *
import sqlalchemy as sa

from Models import Patient

column_labels = [u"编号", u"区域", u"学校", u"年级", u"班级", u"姓名", u"性别", u"生日", u"家长手机", u"身高", u"体重", u"测量角度", u"脂肪判断",
                 u"脂肪含量", u"BMI指数", u"肥胖类型", u"基础代谢", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查"]

DB_NAME = 'data.db'


# TODO improve Search functionality
# TODO add pagenate functionality to the table view

def create_database(env=None):
    if env is None:
        engine = create_engine('sqlite:///./data.db')
    else:
        engine = create_engine('sqlite:///./data-dev.db')
    metadata = MetaData(engine)

    patients = Table('patients', metadata,
                     sa.Column('id', sa.Integer(), nullable=False),
                     sa.Column('name', sa.Unicode(length=10), nullable=True),
                     sa.Column('district', sa.Unicode(length=10), nullable=True),
                     sa.Column('school', sa.Unicode(length=20), nullable=True),
                     sa.Column('grade', sa.Unicode(length=20), nullable=True),
                     sa.Column('class_name', sa.Unicode(length=10), nullable=True),
                     sa.Column('gender', sa.Unicode(length=5), nullable=True),
                     sa.Column('dob', sa.Unicode(20), nullable=True),
                     sa.Column('contact_info', sa.Unicode(length=20), nullable=True),
                     sa.Column('height', sa.Float(), nullable=True),
                     sa.Column('weight', sa.Float(), nullable=True),
                     sa.Column('fat', sa.Unicode(length=10), nullable=True),
                     sa.Column('fat_percentage', sa.Float(), nullable=True),
                     sa.Column('bmi', sa.Float(), nullable=True),
                     sa.Column('fat_type', sa.Unicode(length=10), nullable=True),
                     sa.Column('basic_metabolism', sa.Integer(), nullable=True),
                     sa.Column('measured_angle', sa.Float(), nullable=True),
                     sa.Column('xraynum', sa.Unicode(), nullable=True),
                     sa.Column('cobbsection', sa.Unicode(length=20), nullable=True),
                     sa.Column('cobbdegree', sa.Float(), nullable=True),
                     sa.Column('is_checked', sa.Boolean(), nullable=True),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('district', 'school', 'grade', 'class_name', 'name', 'gender', 'dob'))
    metadata.create_all()
    return engine


class ScoliosisUtils:
    def __init__(self):
        self.session = None
        self.data_errors = []
        self.duplicated_lines = []

    def get_session(self):
        if self.session is None:
            engine = create_engine('sqlite:///./data.db')
            metadata = MetaData(engine)
            metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            self.session = Session()

        return self.session

    def import_from_excel(self, filename):
        '''
        :param filename: 输入的Excel文件
        数据唯一性检查通过捕获SqlAlchemy插入时触发的异常来进行。
        '''

        book = open_workbook(filename)
        sheet = book.sheet_by_index(0)
        for i in range(1, sheet.nrows):
            p = Patient()
            row = sheet.row_values(i)
            try:
                p.load_from_list(row)
                self.get_session().add(p)
                # 数据重复性检查，若插入数据时不符合唯一性则抛出异常。
                try:
                    self.session.flush()
                    self.session.commit()
                except SQLAlchemyError, e:
                    self.duplicated_lines.append(row)
                    # Rollback to start new transaction with this session
                    self.session.rollback()
            except ValueError, e:
                self.append_to_errors(row)
        if len(self.data_errors) > 0:
            self.export_to_excel(u'错误数据.xls', self.data_errors)
        if len(self.duplicated_lines) > 0:
            self.export_to_excel(u'重复数据.xls', self.duplicated_lines)
        self.session.close()
        return len(self.data_errors), len(self.duplicated_lines)

    def append_to_errors(self, l):
        self.data_errors.append(l)

    def load_patients_by_condition(self, district=None, school=None, grade=None, class_name=None, name=None,
                                   is_checked=None):
        session = self.get_session()
        query = session.query(Patient)
        if district is not None:
            query = query.filter(Patient.district == district)
        if school is not None:
            query = query.filter(Patient.school == school)
        if grade is not None:
            query = query.filter(Patient.grade == grade)
        if class_name is not None:
            query = query.filter(Patient.class_name == class_name)
        if name is not None:
            query = query.filter(Patient.name == name)
        if is_checked is not None:
            query = query.filter(Patient.is_checked == is_checked)
        data = query.all()
        # print "length", len(data)
        return data

    def export_to_excel(self, filename, data):
        book = Workbook()
        sheet = book.add_sheet(u"病人信息")
        for i in range(0, len(column_labels)):
            sheet.row(0).write(i, column_labels[i])

        for x in range(0, len(data)):
            for y in range(0, len(column_labels)):
                sheet.row(x + 1).write(y, data[x][y])

        book.save(filename)

    def save_patient(self, patient):
        self.get_session().add(patient)
        self.session.flush()
        self.session.commit()

    def get_distinct_districts(self):
        districts = self.get_session().query(distinct(Patient.district)).all()
        return [each[0] for each in districts]

    def get_distinct_schools(self, district=None):
        q = self.get_session().query(distinct(Patient.school))
        if district is not None:
            q = q.filter(Patient.district == district)
        schools = q.all()
        return [each[0] for each in schools]

    def get_distinct_grade(self, school=None):
        q = self.get_session().query(distinct(Patient.grade))
        if school is not None:
            q = q.filter(Patient.school == school)
        grades = q.all()
        return [each[0] for each in grades]

    def get_distinct_classes(self, school=None, grade=None):
        if school is None or grade is None:
            return []
        else:
            classes = self.get_session().query(distinct(Patient.class_name)).filter(Patient.school == school).filter(
                Patient.grade == grade).all()
            return [each[0] for each in classes]


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.utils = ScoliosisUtils()

    def test_get_distinct_districts(self):
        districts = self.utils.get_distinct_districts()
        # districts = r.fetchall()
        # print districts
        self.districts = districts
        self.assertGreaterEqual(len(districts), 0)

    def test_get_distinct_schools(self):
        schools = self.utils.get_distinct_schools()
        # schools = r.fetchall()
        # print schools
        # print len(schools)
        self.schools = schools
        self.assertGreater(len(schools), 0)

    def test_get_distinct_schools_by_district(self):
        district = list(self.utils.get_distinct_districts()[1])[0]
        print unicode(district)
        schools = self.utils.get_distinct_schools(district=unicode(district))
        # print schools
        # print len(schools)
        self.assertGreaterEqual(len(schools), 0)

    def test_get_distinct_grade(self):
        pass

    def test_get_distinct_classes(self):
        pass
