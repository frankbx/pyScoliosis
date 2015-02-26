# -*- coding: utf-8 -*-
# !/bin/env python
import wx

import pyScoliosisUI as ui
import pyScoliosisUtils as utils


if "2.8" in wx.version():
    import wx.lib.pubsub.setupkwargs
    from wx.lib.pubsub import pub
else:
    from wx.lib.pubsub import pub

column_labels = [u"编号", u"区域", u"学校", u"班级", u"学号", u"姓名", u"联系方式", u"测量角度", u"X光片号", u"Cobb角节段", u"Cobb角度数", u"已复查",
                 u"分组"]
PATIENT_ID = 0
DISTRICT = 1
SCHOOL = 2
CLASS = 3
STUDENT_NUM = 4
NAME = 5
CONTACT_INFO = 6
MEASURED_ANGLE = 7
XRAYNUM = 8
COBBSECTION = 9
COBBDEGREE = 10
IS_CHECKED = 11
GROUP = 12


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


class MainForm(ui.MainFormBase):
    def __init__(self):
        ui.MainFormBase.__init__(self, None)
        # utils.save_data(utils.dummy_data())
        self.data = utils.load_data()
        table = PatientTable(self.data)
        self.setTable(table)
        self.Layout()


    def setTable(self, table):
        self.table = table
        self.patientDataTable.SetTable(table)
        self.patientDataTable.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.patientDataTable.AutoSize()

    def onRowSelect(self, event):
        row = event.GetRow()
        col = event.GetCol()
        checkpatientdialog = CheckPatientDialog(None)
        checkpatientdialog.set_values(self.data[row])
        print self.data[row][col]
        if checkpatientdialog.ShowModal() == wx.ID_OK:
            xrayNum = checkpatientdialog.txtXRayNum.GetValue()
            cobbSection = checkpatientdialog.txtCobbSection.GetValue()
            cobbDegree = checkpatientdialog.txtCobbDegree.GetValue()
            # print xrayNum, cobbSection, cobbDegree
            self.data[row][XRAYNUM] = xrayNum
            self.data[row][COBBSECTION] = cobbSection
            self.data[row][COBBDEGREE] = cobbDegree
            self.data[row][IS_CHECKED] = True
            # self.patientDataTable.Refresh()
            self.patientDataTable.AutoSize()
            utils.save_data(self.data)
        else:
            print "canceled"
        checkpatientdialog.Destroy()


class CheckPatientDialog(ui.CheckPatientDialogBase):
    def set_values(self, patient):
        self.lblPatientIDValue.SetLabelText(unicode(patient[PATIENT_ID]))
        self.lblNameValue.SetLabelText(unicode(patient[NAME]))


class PatientTable(wx.grid.PyGridTableBase):
    def __init__(self, data):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        print len(self.data)
        self.colLabels = column_labels

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.colLabels)

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
    frame.Show(True)
    app.MainLoop()
