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
ID = 13


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
        self.data = utils.load_all_patients()
        self.isFiltered = False

        self.patientDataTable.SetRowLabelSize(0)
        # self.patientDataTable.AutoSize()
        self.setTable(self.data)
        # self.Layout()
        # utils.create_database()
        # utils.init_database()


    def setTable(self, d):
        table = PatientTable(d)
        self.patientDataTable.SetTable(table)
        self.patientDataTable.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.patientDataTable.AutoSize()
        self.patientDataTable.Refresh()
        self.Layout()

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
            self.data[row][XRAYNUM] = xrayNum
            self.data[row][COBBSECTION] = cobbSection
            self.data[row][COBBDEGREE] = cobbDegree
            self.data[row][IS_CHECKED] = True
            utils.update_patient_data(self.data[row])
            self.patientDataTable.Refresh()
        else:
            print "canceled"
        checkpatientdialog.Destroy()


    def onShowUncheckedOnly(self, event):
        if self.cbxFilter.GetValue():
            self.isFiltered = True
            print "set filter to true"
            for each in self.data:
                if each[IS_CHECKED]:
                    print str(each[PATIENT_ID]) + " removed"
                    self.data.remove(each)
        else:
            self.isFiltered = False
            print "set filter to false"
            self.data = utils.load_all_patients()
        self.setTable(self.data)

    def onExportClick(self, event):
        print "export clicked"

    def onSearchClick(self, event):
        print "search clicked"


class CheckPatientDialog(ui.CheckPatientDialogBase):
    def set_values(self, patient):
        self.lblPatientIDValue.SetLabelText(unicode(patient[PATIENT_ID]))
        self.lblNameValue.SetLabelText(unicode(patient[NAME]))
        self.txtXRayNum.SetValue(patient[XRAYNUM])
        self.txtCobbSection.SetValue(patient[COBBSECTION])
        self.txtCobbDegree.SetValue(patient[COBBDEGREE])


class PatientTable(wx.grid.PyGridTableBase):
    def __init__(self, data):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        # print len(self.data)
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
