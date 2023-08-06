# runserver.py

import conda.cli

def run():
	conda.cli.main('bokeh', 'serve',  '--show', 'myapp.py')
	print("Got here...")