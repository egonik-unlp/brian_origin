from pandas_to_np import main as array
import originpro as op
import numpy as np
import sys
import matplotlib.pyplot as plt
import os



# Very useful, especially during development, when you are
# liable to have a few uncaught exceptions.
# Ensures that the Origin instance gets shut down properly.
# Note: only applicable to external Python.

#Lifted straight from origin documentation website!


def origin_shutdown_exception_hook(exctype, value, traceback):
    '''Ensures Origin gets shut down if an uncaught exception'''
    op.exit()
    sys.__excepthook__(exctype, value, traceback)

def process_file(filename:str) -> dict:
	'''
	Receives filenames, returns dictionary with sheet names as keys and (xx,yy,zz) tuples as values
	can be used for plotting EEMs using sth like:
	```python
	worksheets=process_file(file)
	for ws_name, ws in worksheets.items():
		plt.contourf(**ws)
		plt.title(ws_name)
		plt.show()
	
	```
	
	'''

	worksheets={}
	file_as_path=os.path.join(os.getcwd(), filename)
	op.open(file=file_as_path)
	for wd in op.pages('w'):
		worksheets[wd.lname]=array(wd[6].to_df()) # El 6to nodo del WBook son los datos en formato xyz 
	return worksheets


def main(path: str) -> None:
	#Boilerplate for origin.
	if op and op.oext:
	    sys.excepthook = origin_shutdown_exception_hook


	# Set Origin instance visibility.
	# Important for only external Python.
	# Should not be used with embedded Python. 
	if op.oext:
	    op.set_show(False)
	
	#My own code
	os.chdir(path) # Passes through path from function call
	for file in os.listdir():
		if file[-4:]=='.opj':
			worksheets=process_file(file)
			np.savez('{}_arrays'.format(file[:-4]), **worksheets) # Sheet name acts as key, 3:n:m matrices are values. n is the number of exc lammdas, m is emission.


	op.exit()



if __name__ =='__main__':
	if len(sys.argv)==1:
		main('files')		# Assuming files are in "files" folder
	elif len(sys.argv)==2:
		try:
			main(sys.argv[1])
		except FileNotFoundError:
			print('Error: Path nonexistant')
