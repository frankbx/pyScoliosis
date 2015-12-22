# -*- coding: utf-8 -*-
# !/bin/env python
import os
import sys

import wx

import pyScoliosisUI as ui
import pyScoliosisUtils
from Models import attribute_mapper


# if "2.8" in wx.version():
#     import wx.lib.pubsub.setupkwargs
#     from wx.lib.pubsub import pub
# else:
#     from wx.lib.pubsub import pub
#
#
# class LoginDialog():
#     def __init__(self, parent):
#         ui.LoginDialogBase.__init__(self, parent)
#
#     def login(self, event):
#         stupid_password = "password"
#         user_password = self.txt_password.GetValue()
#         if user_password == stupid_password:
#             print "You are now logged in!"
#             pub.sendMessage("frameListener", message="show")
#             self.Destroy()
#         else:
#             print "Username or password is incorrect!"
#             self.Destroy()
#
#     def cancel(self, event):
#         self.Destroy()


class MainForm(ui.MainFormBase):
    def __init__(self):
        ui.MainFormBase.__init__(self, None)
        self.util = pyScoliosisUtils.ScoliosisUtils()
        self.data = self.util.load_all_patients()
        self.patientDataTable.SetRowLabelSize(0)
        self.setTable(self.data)
        districts = self.util.get_distinct_districts()
        # print type(districts[0])
        # print dir(districts[0])
        # print districts[0].district
        self.district_choice.Append(u"全部区")
        self.school_choice.Append(u'全部学校')
        self.grade_choice.Append(u'全部年级')
        self.class_choice.Append(u'全部班级')
        for each in districts:
            self.district_choice.Append(each)
        schools = self.util.get_distinct_schools()
        for each in schools:
            self.school_choice.Append(each)

    def setTable(self, d):
        table = PatientTable(d)
        self.patientDataTable.SetTable(table)
        self.patientDataTable.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.patientDataTable.AutoSize()
        self.patientDataTable.Refresh()
        self.Layout()
        self.stbStatus.SetStatusText(u"当前显示记录数：" + str(len(self.data)), 0)

    def onRowSelect(self, event):
        row = event.GetRow()
        col = event.GetCol()
        checkpatientdialog = CheckPatientDialog(None)
        checkpatientdialog.set_values(self.data[row])
        if checkpatientdialog.ShowModal() == wx.ID_OK:
            xrayNum = checkpatientdialog.txtXRayNum.GetValue()
            cobbSection = checkpatientdialog.txtCobbSection.GetValue()
            cobbDegree = checkpatientdialog.txtCobbDegree.GetValue()
            self.data[row].xraynum = xrayNum
            self.data[row].cobbsection = cobbSection
            self.data[row].cobbdegree = cobbDegree
            self.data[row].is_checked = True
            self.util.save_patient(self.data[row])
            self.data = self.util.load_all_patients()
            self.setTable(self.data)
            # self.patientDataTable.SetValue(row, column_mapper['xraynum'], xrayNum)
            # self.patientDataTable.SetValue(row, column_mapper['cobbsection'], cobbSection)
            # self.patientDataTable.SetValue(row, column_mapper['cobbdegree'], cobbDegree)
            # self.patientDataTable.SetValue(row, column_mapper['is_checked'], True)
            # self.patientDataTable.Refresh()
        else:
            print "canceled"
        checkpatientdialog.Destroy()

    def onShowUncheckedOnly(self, event):
        self.data = self.util.load_all_checked_patients(False)
        if self.cbxUnchecked.GetValue():
            self.cbxChecked.SetValue(False)
            # for each in self.util.load_all_patients():
            #     if each.is_checked:
            #         self.data.remove(each)
        self.setTable(self.data)
        # pass

    def onShowCheckedOnly(self, event):
        self.data = self.util.load_all_checked_patients(True)
        if self.cbxChecked.GetValue():
            self.cbxUnchecked.SetValue(False)
            # for each in self.util.load_all_patients():
            #     if not each.is_checked:
            #         self.data.remove(each)
        self.setTable(self.data)
        # pass

    def onShowAll(self, event):
        self.data = self.util.load_all_patients()
        self.setTable(self.data)
        self.cbxUnchecked.SetValue(False)
        self.cbxChecked.SetValue(False)
        # pass

    def filter_table(self, filter_str):
        # self.data = execute_query(filter_str)
        # self.setTable(self.data)
        pass

    def onExportClick(self, event):
        wildcard = u"Excel 文件 (*.xls)|*.xls|所有文件 (*.*)|*.*"
        filename = None
        dlg = wx.FileDialog(self, u"导出到...",
                            os.getcwd(),
                            style=wx.SAVE | wx.OVERWRITE_PROMPT,
                            wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename += '.xls'
        if filename:
            self.util.export_to_excel(filename, self.data)

    def onSearchClick(self, event):
        # formdata = {}
        # if self.txtDistrict.GetValue().strip():
        #     formdata["[district]"] = self.txtDistrict.GetValue()
        # if self.txtSchool.GetValue().strip():
        #     formdata["[school]"] = self.txtSchool.GetValue().strip()
        # if self.txtClass.GetValue().strip():
        #     formdata["[class]"] = self.txtClass.GetValue().strip()
        # if self.txtName.GetValue().strip():
        #     formdata["[name]"] = self.txtName.GetValue().strip()
        # if not len(formdata) == 0:
        #     self.filter_table(formdata)
        pass

    def import_data(self, event):
        wildcard = u"Excel 文件 (*.xls)|*.xls|所有文件 (*.*)|*.*"
        dlg = wx.FileDialog(self, u"从文件导入数据",
                            os.getcwd(),
                            style=wx.OPEN,
                            wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            r = self.util.import_from_excel(filename)
            msg_duplicate = ''
            msg_errors = ''
            if r[1] > 0:
                # print "check  duplicated file"
                msg_duplicate = u"发现重复数据并已忽略。请检查 重复数据.xls 查看重复数据。"
            if r[0] > 0:
                # print "check errors file"
                msg_errors = u"发现数据有错。错误数据已输出到 错误数据.xls。请更改数据后重新导入。"
            msg = wx.MessageDialog(None, u'数据导入完成！' + msg_errors + msg_duplicate, u'警告', wx.OK | wx.ICON_WARNING)
            if msg.ShowModal() == wx.OK:
                msg_duplicate = ''
                msg_errors = ''
                msg.Destroy()
            else:
                msg_duplicate = ''
                msg_errors = ''
                msg.Destroy()
        self.data = self.util.load_all_patients()
        self.setTable(self.data)


class CheckPatientDialog(ui.CheckPatientDialogBase):
    def set_values(self, patient):
        self.txtPatientID.SetValue(unicode(patient.id))
        self.txtName.SetValue(unicode(patient.name))
        self.txtXRayNum.SetValue(unicode(patient.xraynum))
        self.txtCobbSection.SetValue(unicode(patient.cobbsection))
        self.txtCobbDegree.SetValue(unicode(patient.cobbdegree))


class PatientTable(wx.grid.PyGridTableBase):
    def __init__(self, data):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.colLabels = pyScoliosisUtils.column_labels

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        v = self.data[row].__dict__[attribute_mapper[col]]
        if v is None:
            return ''
        else:
            return v

    def SetValue(self, row, col, value):
        self.data[row].__dict__[attribute_mapper[col]] = value

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return row + 1

    def getdata(self):
        return self.data


if __name__ == '__main__':
    app = wx.App()
    if os.path.exists(pyScoliosisUtils.DB_NAME):
        print "DB file found!"
    else:
        dlg = wx.MessageDialog(None, u'数据库文件不存在，要创建空白数据库文件吗？点击“否”将退出程序。', u'警告', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            pyScoliosisUtils.create_database()
        else:
            sys.exit(-1)
        dlg.Destroy()
    frame = MainForm()
    frame.Show(True)
    app.MainLoop()
