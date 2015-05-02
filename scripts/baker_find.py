#python
"""Return the result from the file dialog to the user value"""



import lx

arg = lx.arg()

lx.eval('dialog.setup fileOpen')
lx.eval('dialog.open')
file_to_open = lx.eval('dialog.result ?')
lx.out(file_to_open)
lx.eval("user.value " + arg + " {" + file_to_open + '}' )