# -*- coding: utf-8 -*-
# !/bin/env python

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from xlwt import Workbook
from xlrd import *

from Models import Patient

column_labels = [u"编号", u"区域", u"学校", u"年级", u"班级", u"姓名", u"性别", u"生日", u"家长手机", u"身高", u"体重", u"测量角度", u"脂肪判断",
                 u"脂肪含量", u"BMI指数", u"肥胖类型", u"基础代谢", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查"]


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

    def export_to_excel(self, filename, data):
        book = Workbook()
        sheet = book.add_sheet(u"病人信息")
        for i in range(0, len(column_labels)):
            sheet.row(0).write(i, column_labels[i])

        for x in range(0, len(data)):
            for y in range(0, len(column_labels)):
                sheet.row(x + 1).write(y, data[x][y])

        book.save(filename)
