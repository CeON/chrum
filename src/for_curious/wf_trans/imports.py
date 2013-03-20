#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''
import re
import imp
import os
import glob

def importAll(package):
	py_mods = []
	pre = './'+package
	for file_ in glob.glob(pre+'/*.py'):
		ret = re.search('^([a-aA-Z0-9][^\.]+)',file_[len(pre)+1:],re.IGNORECASE)
		if ret:
			py_mods.append(load_from_file(file_))
	return py_mods

def load_from_file(filepath):
	mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
	if file_ext.lower() == '.py':
		py_mod = imp.load_source(mod_name, filepath)
	elif file_ext.lower()=='.pyc':
		py_mod = imp.load_compiled(mod_name, filepath)
	return py_mod
