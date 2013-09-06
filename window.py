__author__ = 'Danny Wynne'

from mlib.core import qt
from mlib.core.qt import QtGui, QtCore, uic

import maya.mel as mel
import os

from . import utils as explorer_utils
reload(explorer_utils)

baseclass = qt.loadUiFile("window")

class MayaQtExplorer(baseclass):
	def __init__(self, parent = None):
		super(MayaQtExplorer, self).__init__(parent)
		self.maya_window = parent
		
		self.setUnmanagedWidgets([self.gvars_list, self.info_te])

		self.gvars = explorer_utils.get_ui_gvars()
		self.gvars_list.clear()
		self.gvars_list.addItems(self.gvars)

		self.info_te.setText("")

		self.gvars_list.itemDoubleClicked.connect(self.gvar_double_clicked)
		self.parent_list.itemDoubleClicked.connect(self.ui_path_list_double_clicked)
		self.child_list.itemDoubleClicked.connect(self.ui_path_list_double_clicked)


		self._band = None

	def ui_path_list_double_clicked(self, *args):
		ui_path = args[0].text()
		try:
			widget = qt.toQtObject(ui_path)
			if type(widget) == type(None):
				raise TypeError
		except:
			return
		self.set_current_widget(widget)

	def gvar_double_clicked(self, *args):
		gvar = args[0].text()
		try:
			tmp = mel.eval('string $temp = %s;'%gvar)
			widget = qt.toQtObject(tmp)
		except:
			print "probably not a QObject"
			return
		self.set_current_widget(widget)

	def set_current_widget(self, widget):

		ui_path = qt.widgetToMayaName(widget)
		self.current_widget_path.setText(ui_path)

		children = widget.children()
		self.child_list.clear()
		for c in children:
			ui_path = qt.widgetToMayaName(c)
			self.child_list.addItem(ui_path)

		parent = widget.parent()
		self.parent_list.clear()
		self.parent_list.addItem(qt.widgetToMayaName(parent))

		self.rubber_band_widget(widget)

	def rubber_band_widget(self, widget):
		try:
			self.band.hide();
		except:
			pass

		self.band = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self.maya_window)
		rect = widget.geometry()
		pnt = widget.mapTo(self.maya_window, widget.geometry().topLeft())
		rect.moveTo(pnt)
		self.band.setGeometry(rect)

		self.band.show()