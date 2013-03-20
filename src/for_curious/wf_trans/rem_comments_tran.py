#!/usr/bin/python
'''
 (C) 2010-2012 ICM UW. All rights reserved.
'''
import re;

def remove_one_line_comments(text,props,path):
	out_text = []
	text = re.sub(r'<!--[\S\s.]+?-->',r'',text)
	return ''.join(text)

