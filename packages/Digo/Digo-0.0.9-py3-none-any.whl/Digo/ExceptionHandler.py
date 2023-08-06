import sys, traceback
import atexit
from Digo import DigoCore

isCrash = False

def check_crash(exc_type, exc_value, exc_traceback):
	global isCrash
	isCrash = True
	traceback.print_exception(exc_type, exc_value, exc_traceback)

def exit_process(stateUpdate):
	if isCrash is True:
		stateUpdate(2)
		print("Digo Exit(1)")
	else:
		stateUpdate(1)
		print("Digo Exit(0)")



sys.excepthook = check_crash
