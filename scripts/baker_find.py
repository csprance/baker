# python
"""Return the result from the file dialog to the user value"""

import lx





def main():
	# lx.arg() contains a string of all the args sent through in this case the user.value we want to update
	arg = lx.arg()
	# set up our fileOpen Dialog
	lx.eval('dialog.setup fileOpen')
	# open the dialog
	lx.eval('dialog.open')
	# dialog.result ? holds the name of the file dialog 
	file_to_open = lx.eval('dialog.result ?')
	# set the user value to the file_to_open
	lx.eval("user.value %s { %s }" % (arg , file_to_open )  )



if __name__ == '__main__':
	main()