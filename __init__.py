__author__ = 'Danny Wynne'

from mlib.core import qt
from mlib.core.qt import QtGui, QtCore
from . import window
reload(window)
def show():
	win = qt.getMayaWindow()
	global exp_win
	try:
		exp_win.close()
	except:
		pass
	exp_win = window.MayaQtExplorer(win)
	exp_win.show()
