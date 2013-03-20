#!/usr/bin/python
'''
 (C) 2010-2012 ICM UW. All rights reserved.
'''

def remove_many_newlines(text,props,path):
	while True:
		old = len(text)
		text = text.replace('\n\n','\n')
		new = len(text)	
		if old==new:
			break
	return text

