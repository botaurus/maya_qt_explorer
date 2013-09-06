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
		
		self.setUnmanagedWidgets([self.gvars_list, self.info_te, self.current_widget_path])

		#hide unused widgets for now
		self.label_5.hide()
		self.info_te.hide()
		
		self.gvars = explorer_utils.get_ui_gvars()
		self.gvars = [" - ".join(x) for x in self.gvars]
		self.gvars_list.clear()
		self.gvars_list.addItems(self.gvars)

		self.info_te.setText("")

		self.gvars_list.itemDoubleClicked.connect(self.gvar_double_clicked)
		self.parent_list.itemDoubleClicked.connect(self.ui_path_list_double_clicked)
		self.child_list.itemDoubleClicked.connect(self.ui_path_list_double_clicked)
		self.search_gvars.textChanged.connect(self.search_changed)

		self.band = None

	def search_changed(self):
		search = str(self.search_gvars.text()).lower()
		if len(search) < 3:
			self.gvars_list.clear()
			self.gvars_list.addItems(self.gvars)
			return
		_tmp_gvars = []
		for g in self.gvars:
			if g.lower().find(search) > -1:
				_tmp_gvars.append(g)
		self.gvars_list.clear()
		self.gvars_list.addItems(_tmp_gvars)

	def ui_path_list_double_clicked(self, *args):
		ui_path = args[0].text()
		try:
			widget = qt.pathToWidget(ui_path.partition(" - ")[2])
			if widget is None:
				raise TypeError
		except:
			return
		self.set_current_widget(widget)

	def gvar_double_clicked(self, *args):
		gvar = args[0].text()
		try:
			tmp = mel.eval('string $temp = %s;'%gvar.partition(" - ")[0])
			widget = qt.pathToWidget(tmp)
		except:
			print "probably not a QObject"
			return
		self.set_current_widget(widget)

	def set_current_widget(self, widget):

		ui_path = qt.widgetToPath(widget)
		widget_type = type(widget).__name__
		self.current_widget_path.setText(widget_type + " - " + ui_path)

		children = widget.children()
		self.child_list.clear()
		for c in children:
			c_type = type(c).__name__
			ui_path = qt.widgetToPath(c)
			self.child_list.addItem(c_type + " - " + ui_path)

		parent = widget.parent()
		self.parent_list.clear()
		parent_type = type(parent).__name__
		self.parent_list.addItem(parent_type + " - " + qt.widgetToPath(parent))

		self.rubber_band_widget(widget)

	def rubber_band_widget(self, widget):
		try:
			self.band.hide();
		except:
			pass
		if self.band is None:
			self.band = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self.maya_window)
		try:
			rect = widget.geometry()
		except:
			return
		pnt = widget.mapTo(self.maya_window, widget.geometry().topLeft())
		rect.moveTo(pnt)
		self.band.setGeometry(rect)
		self.band.show()