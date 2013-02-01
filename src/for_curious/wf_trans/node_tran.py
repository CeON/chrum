#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''
from imports import *


class WorkflowFileError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def node_substitution(text,props,path):
	currPath = os.getcwd()
	os.chdir(path)
#	print os.getcwd()
	
	for i in importAll('node_transformations'):
#		print i
		for f in dir(i):
			if f.startswith('NODETRANSFORMATION'):
				methodToCall = getattr(i, f)
				text = methodToCall(text)
				#text = i[f](text)
	os.chdir(currPath)
	return text
