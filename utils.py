import maya.mel as mel
import maya.cmds as cmds

from mlib.core import qt
from mlib.core.qt import QtGui, QtCore

def get_ui_gvars():
	#only get gvars that are qt related
	gvars = []
	for g in [x for x in sorted(mel.eval('env')) if x.find("$g")>-1]:
		widget_type = None
		try:
			var_type = mel.eval('whatIs "%s"'%g)
			if not var_type == "string variable":
				raise TypeError

			tmp = mel.eval('string $temp = %s;'%g)

			if tmp is None:
				raise TypeError

			target_widget = qt.pathToWidget(tmp)
			if type(target_widget) == type(None):
				raise ValueError
			widget_type = type(target_widget)
		except:
			continue
		gvars.append([g, widget_type.__name__])
	return gvars
