# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class mainForm
###########################################################################

class mainForm(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"脊柱侧凸预防干预信息系统", pos=wx.DefaultPosition,
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.m_statusBar1 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.m_menubar1 = wx.MenuBar(0)
        self.fileMenu = wx.Menu()
        self.m_menubar1.Append(self.fileMenu, u"文件")

        self.SetMenuBar(self.m_menubar1)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.patientDataTable = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.RAISED_BORDER | wx.VSCROLL)

        # Grid
        self.patientDataTable.CreateGrid(5, 7)
        self.patientDataTable.EnableEditing(True)
        self.patientDataTable.EnableGridLines(True)
        self.patientDataTable.EnableDragGridSize(False)
        self.patientDataTable.SetMargins(0, 0)

        # Columns
        self.patientDataTable.EnableDragColMove(False)
        self.patientDataTable.EnableDragColSize(True)
        self.patientDataTable.SetColLabelSize(30)
        self.patientDataTable.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.patientDataTable.EnableDragRowSize(True)
        self.patientDataTable.SetRowLabelSize(80)
        self.patientDataTable.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.patientDataTable.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer1.Add(self.patientDataTable, 1, wx.ALL | wx.EXPAND, 0)

        self.operationPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.operationPanel.SetMaxSize(wx.Size(350, -1))

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.HORIZONTAL)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblSchool = wx.StaticText(self.operationPanel, wx.ID_ANY, u"学校：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblSchool.Wrap(-1)
        gbSizer1.Add(self.lblSchool, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtSchool = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     0)
        gbSizer1.Add(self.txtSchool, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.lblClass = wx.StaticText(self.operationPanel, wx.ID_ANY, u"班级：", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.lblClass.Wrap(-1)
        gbSizer1.Add(self.lblClass, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtClass = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                    0)
        gbSizer1.Add(self.txtClass, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.lblStuNum = wx.StaticText(self.operationPanel, wx.ID_ANY, u"学号：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblStuNum.Wrap(-1)
        gbSizer1.Add(self.lblStuNum, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtStuNum = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     0)
        gbSizer1.Add(self.txtStuNum, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.lblName = wx.StaticText(self.operationPanel, wx.ID_ANY, u"姓名：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblName.Wrap(-1)
        gbSizer1.Add(self.lblName, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtName = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                   0)
        gbSizer1.Add(self.txtName, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.lblContactInfo = wx.StaticText(self.operationPanel, wx.ID_ANY, u"联系方式：", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.lblContactInfo.Wrap(-1)
        gbSizer1.Add(self.lblContactInfo, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtContactInfo = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        gbSizer1.Add(self.txtContactInfo, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.lblMeasuredAngle = wx.StaticText(self.operationPanel, wx.ID_ANY, u"测量角度：", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.lblMeasuredAngle.Wrap(-1)
        gbSizer1.Add(self.lblMeasuredAngle, wx.GBPosition(6, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtMeasuredAngle = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        gbSizer1.Add(self.txtMeasuredAngle, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.lblDistrict = wx.StaticText(self.operationPanel, wx.ID_ANY, u"区域：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblDistrict.Wrap(-1)
        gbSizer1.Add(self.lblDistrict, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.txtDistrict = wx.TextCtrl(self.operationPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        gbSizer1.Add(self.txtDistrict, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.btnSearch = wx.Button(self.operationPanel, wx.ID_ANY, u"查找", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.btnSearch, wx.GBPosition(7, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cbxFilter = wx.CheckBox(self.operationPanel, wx.ID_ANY, u"只显示未检查病人", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.cbxFilter, wx.GBPosition(8, 0), wx.GBSpan(1, 2), wx.ALL, 5)

        self.btnExport = wx.Button(self.operationPanel, wx.ID_ANY, u"导出当前数据", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.btnExport, wx.GBPosition(9, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        gbSizer1.AddGrowableCol(1)

        self.operationPanel.SetSizer(gbSizer1)
        self.operationPanel.Layout()
        gbSizer1.Fit(self.operationPanel)
        bSizer1.Add(self.operationPanel, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
	

