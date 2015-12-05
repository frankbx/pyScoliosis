# -*- coding: utf-8 -*-
# !/bin/env python
import unittest

from sqlalchemy import Column, String, Integer, Date, Float, Boolean, create_engine, MetaData, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


class TestPatient(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///./data-dev.db', echo=True)
        self.metadata = MetaData(self.engine)
        self.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine) #创建了一个自定义了的 Session类
        # Session.configure()  #将创建的数据库连接关联到这个session
        self.session = Session()

    def testInsertPatient(self):
        p = Patient()
        p.name = 'test'
        self.session.add(p)
        self.session.commit()
        query = self.session.query(Patient)
        self.assertEqual(1, len(query.all()))

    def testLoadPatient(self):
        p = Patient(name="test")
        self.session.add(p)
        self.session.commit()
        r = self.session.query(Patient).filter_by(name="test").first()
        self.assertEqual(r.name, "test")



    def tearDown(self):
        conn= self.engine.connect()
        conn.execute("delete From patients where 1=1")
        self.session.close()


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10))
    district = Column(Unicode(10))
    school = Column(Unicode(20))
    class_name = Column(Unicode(10))
    gender = Column(Unicode(5))
    dob = Column(Date)
    contact_info = Column(Unicode(20))
    height = Column(Float)
    weight = Column(Float)
    fat = Column(Unicode(10))
    fat_percentage = Column(Float)
    bmi = Column(Float)
    fat_type = Column(Unicode(10))
    basic_metabolism = Column(Integer)
    measured_angle = Column(Float)
    x_ray_num = Column(Unicode)
    cobb_section = Column(Unicode(20))
    cobb_degree = Column(Float)
    is_checked = Column(Boolean)

    def __repr__(self):
        return '[Patient: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (
            self.patient_id, self.district, self.school, self.class_name, self.name, self.gender, self.dob,
            self.contact_info, self.height, self.weight, self.fat, self.fat_percentage, self.bmi, self.fat_type,
            self.basic_metabolism,
            self.measured_angle, self.x_ray_num, self.cobb_section, self.cobb_degree, self.is_checked)

    def check(self, x_ray_num, cobb_section, cobb_degree):
        self.x_ray_num = x_ray_num
        self.cobb_section = cobb_section
        self.cobb_degree = cobb_degree
        self.is_checked = True


if __name__ == '__main__':
    # p = Patient(1, "district ", "school ", "class ", u"姓名 ", u"男", "2008/11/18", 120, 20, 'fat',
    #             0.2, 20, 'fat_type', 'basic_metabolism',
    #             "contact information ********************* ", "measured angle ", "", "", "", False)
    # for key in p.__dict__:
    #     print key, '=>', getattr(p, key)
    #
    # print unicode(p)
    unittest.main()
