import maya.mel as mel
import maya.cmds as cmds

from mlib.core import qt
from mlib.core.qt import QtGui, QtCore

def get_ui_gvars():
	#only get gvars that are qt related
	gvars = []
	for g in [x for x in sorted(mel.eval('env')) if x.find("$g")>-1]:
		try:
			var_type = mel.eval('whatIs "%s"'%g)
			if not var_type == "string variable":
				raise TypeError
				
			tmp = mel.eval('string $temp = %s;'%g)

			if not type(tmp) == type(u''):
				raise TypeError

			target_widget = qt.toQtObject(tmp)
			if type(target_widget) == type(None):
				raise ValueError
		except:
			continue
		gvars.append(g)
	return gvars
