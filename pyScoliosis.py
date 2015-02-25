# -*- coding: utf-8 -*-
# !/bin/env python
import wx

import pyScoliosisUI as ui


if "2.8" in wx.version():
    import wx.lib.pubsub.setupkwargs
    from wx.lib.pubsub import pub
else:
    from wx.lib.pubsub import pub

column_labels = [u"编号", u"区域", u"学校", u"班级", u"学号", u"姓名", u"联系方式", u"测量角度", u"已复查", u"分组"]
PATIENT_ID = 0
DISTRICT = 1
SCHOOL = 2
CLASS = 3
STUDENT_NUM = 4
NAME = 5
CONTACT_INFO = 6
MEASURED_ANGLE = 7
IS_CHECKED = 8
GROUP = 9


class LoginDialog():
    def __init__(self, parent):
        ui.LoginDialogBase.__init__(self, parent)

    def login(self, event):
        stupid_password = "password"
        user_password = self.txt_password.GetValue()
        if user_password == stupid_password:
            print "You are now logged in!"
            pub.sendMessage("frameListener", message="show")
            self.Destroy()
        else:
            print "Username or password is incorrect!"
            self.Destroy()

    def cancel(self, event):
        self.Destroy()


class Patient(list):
    def __init__(self, patient_id=None, district=None, name=None, contact_info=None, school=None, class_num=None,
                 group=None,
                 measured_angle=None, is_checked=None, student_num=None):
        self.patient_id = patient_id
        self.district = district
        self.name = name
        self.contact_info = contact_info
        self.school = school
        self.class_num = class_num
        self.group = group
        self.measured_angle = measured_angle
        self.is_checked = is_checked
        self.student_num = student_num


class MainForm(ui.MainFormBase):
    def __init__(self):
        ui.MainFormBase.__init__(self, None)
        self.data = self.loaddata()
        table = PatientTable(self.data)
        self.setTable(table)
        self.Layout()


    def setTable(self, table):
        self.table = table
        self.patientDataTable.SetTable(table)
        self.patientDataTable.AutoSize()

    def loaddata(self):
        data = []
        for i in range(0, 6):
            p = [i + 1, "district", "school", "class", "student number", "name",
                 "contact information *********************", "measured angle", False,
                 "A"]
            print p
            data.append(p)

        return data


class PatientTable(wx.grid.PyGridTableBase):
    def __init__(self, data):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        print len(self.data)
        self.colLabels = [u"编号", u"区域", u"学校", u"班级", u"学号", u"姓名", u"联系方式", u"测量角度"]
        # print self.colLabels

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return 8

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.data[row][col]
        # pass

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return row + 1

    def getdata(self):
        return self.data


if __name__ == '__main__':
    app = wx.App()
    frame = MainForm()
    # print dir(frame)
    frame.Layout()
    frame.Show(True)
    app.MainLoop()
