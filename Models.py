# -*- coding: utf-8 -*-
# !/bin/env python
import unittest
import logging

from sqlalchemy import Column, Integer, Float, Boolean, MetaData, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

column_mapper = {u"编号"  : 0, u"区域": 1, u"学校": 2, u"年级": 3, u"班级": 4, u"姓名": 5, u"性别": 6, u"生日": 7, u"家长手机": 8, u"身高": 9,
                 u"体重"  : 10, u"测量角度": 11, u"脂肪判断": 12,
                 u"脂肪含量": 13, u"BMI指数": 14, u"肥胖类型": 15, u"基础代谢": 16, u"X光片号": 17, u"Cobb角节段": 18, u"Cobb角度数": 19,
                 u"已复查" : 20}

attribute_mapper = {0 : 'id', 1: 'district', 2: 'school', 3: 'grade', 4: 'class_name', 5: 'name', 6: 'gender',
                    7 : 'dob',
                    8 : 'contact_info',
                    9 : 'height',
                    10: 'weight', 11: 'measured_angle', 12: 'fat',
                    13: 'fat_percentage', 14: 'bmi', 15: 'fat_type', 16: 'basic_metabolism', 17: 'xraynum',
                    18: 'cobbsection',
                    19: 'cobbdegree',
                    20: 'is_checked'}

genders = [u'男', u'女', u'']

fatness = [u'低', u'标准', u'偏高', u'高', u'']

fat_type = [u'消瘦', u'标准', u'隐藏性肥胖', u'肥胖', u'肌肉性肥胖', u'']


class TestPatient(unittest.TestCase):
    def setUp(self):
        # self.engine = create_engine('sqlite:///./data-dev.db')
        import pyScoliosisUtils
        self.engine = pyScoliosisUtils.create_database(env='Dev')
        self.metadata = MetaData(self.engine)
        # self.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.p = Patient()
        self.p.name = "test"

    def testInsertPatient(self):
        self.session.add(self.p)
        self.session.commit()
        query = self.session.query(Patient)
        self.assertEqual(1, len(query.all()))

    def testLoadPatient(self):
        self.session.add(self.p)
        self.session.commit()
        r = self.session.query(Patient).filter_by(id=self.p.id).first()
        self.assertEqual(r.name, "test")

    def testGenderByCorrectNumber(self):
        l = [1] * 21
        self.p.load_from_list(l)
        self.assertEqual(self.p.gender, u'男')
        l = [2] * 21
        self.p.load_from_list(l)
        self.assertEqual(self.p.gender, u'女')

    def testGenderByWord(self):
        l = [1] * 21
        l[6] = u'男'
        # p = Patient()
        self.p.load_from_list(l)
        self.assertEqual(self.p.gender, u'男')
        l[6] = u'女'
        self.p.load_from_list(l)
        self.assertEqual(self.p.gender, u'女')

    def testWrongGender(self):
        l = [1] * 21
        l[6] = 6
        # p = Patient()
        try:
            self.p.load_from_list(l)
        except ValueError, e:
            # print e
            self.assertEqual(e[0][:12], 'Wrong Gender')

    # def test

    def tearDown(self):
        conn = self.engine.connect()
        conn.execute("delete From patients where 1=1")
        self.session.close()


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10), default='')
    district = Column(Unicode(10), default='')
    school = Column(Unicode(20), default='')
    grade = Column(Unicode(20), default='')
    class_name = Column(Unicode(10), default='')
    gender = Column(Unicode(5), default='')
    dob = Column(Unicode(20))
    contact_info = Column(Unicode(20), default='')
    height = Column(Float)
    weight = Column(Float)
    fat = Column(Unicode(10), default='')
    fat_percentage = Column(Float)
    bmi = Column(Float)
    fat_type = Column(Unicode(10), default='')
    basic_metabolism = Column(Integer)
    measured_angle = Column(Float)
    xraynum = Column(Unicode, default='')
    cobbsection = Column(Unicode(20), default='')
    cobbdegree = Column(Unicode(20), default=0)
    is_checked = Column(Boolean, nullable=False, default=False)

    def load_from_list(self, values):
        self.district = values[column_mapper[u"区域"]]
        self.school = values[column_mapper[u"学校"]]
        self.grade = int(values[column_mapper[u"年级"]])
        self.class_name = int(values[column_mapper[u"班级"]])
        self.name = values[column_mapper[u"姓名"]]

        v = values[column_mapper[u"性别"]]
        if v in [1, 2]:
            self.gender = genders[v - 1]
        elif v in genders:
            self.gender = v
        else:
            raise ValueError('Wrong Gender %s', v)

        self.dob = values[column_mapper[u"生日"]]
        self.contact_info = values[column_mapper[u"家长手机"]]
        try:
            self.height = float(values[column_mapper[u"身高"]])
        except ValueError:
            logging.error(unicode(self.height))
        try:
            self.weight = float(values[column_mapper[u"体重"]])
        except ValueError:
            logging.error(unicode(self.weight))

        v = values[column_mapper[u"脂肪判断"]]
        if v in range(1, 5):
            self.fat = fatness[v - 1]
        elif v in fatness:
            self.fat = v
        else:
            raise ValueError("Wrong Fat: %s", v)

        try:
            self.fat_percentage = float(values[column_mapper[u"脂肪含量"]])
        except ValueError:
            logging.error(unicode(self.fat_percentage))

        try:
            self.bmi = float(values[column_mapper[u"BMI指数"]])
        except ValueError:
            logging.error(unicode(self.bmi))

        v = values[column_mapper[u"肥胖类型"]]
        if v in range(1, 6):
            self.fat_type = fat_type[v - 1]
        elif v in fat_type:
            self.fat_type = v
        else:
            raise ValueError('Wrong Fat Type: %s', v)

        try:
            self.basic_metabolism = int(values[column_mapper[u"基础代谢"]])
        except ValueError:
            logging.error(unicode(self.name))
        try:
            self.measured_angle = float(values[column_mapper[u"测量角度"]])
        except ValueError:
            logging.error(unicode(self.measured_angle))
        self.xraynum = values[column_mapper[u"X光片号"]]
        self.cobbsection = values[column_mapper[u"Cobb角节段"]]
        self.cobbdegree = values[column_mapper[u"Cobb角度数"]]
        v = values[column_mapper[u"已复查"]]
        if v == '' or v is False or v == 0:
            self.is_checked = False
        else:
            self.is_checked = True

    def to_list(self):
        return [self.id, self.district, self.school, self.grade, self.class_name, self.name, self.gender, self.dob,
                self.contact_info, self.height, self.weight, self.measured_angle, self.fat, self.fat_percentage,
                self.bmi, self.fat_type, self.basic_metabolism, self.xraynum, self.cobbsection, self.cobbdegree,
                self.is_checked]

    def __repr__(self):
        return '[Patient: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (
            self.id, self.district, self.school, self.class_name, self.name, self.gender, self.dob,
            self.contact_info, self.height, self.weight, self.measured_angle, self.fat, self.fat_percentage, self.bmi,
            self.fat_type, self.basic_metabolism, self.xraynum, self.cobbsection, self.cobbdegree, self.is_checked)


def check(self, x_ray_num='', cobb_section='', cobb_degree=''):
    if x_ray_num is None:
        x_ray_num = ''
    self.x_ray_num = x_ray_num
    if cobb_section is None:
        cobb_section = ''
    if cobb_degree is None:
        cobb_degree = 0
    self.cobb_section = cobb_section
    self.cobb_degree = cobb_degree
    self.is_checked = True


if __name__ == '__main__':
    unittest.main()
