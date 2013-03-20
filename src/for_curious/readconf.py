#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''
import string;
import sys;
import re;

def readConfiguration(text,props):
	for line in text.split('\n'):
		line=line.strip()
		if line.startswith('#'):
			continue
		if re.search('=',line,re.IGNORECASE):
			while line.find('${')!=-1:
				srh = re.search('\$\{([^\}]+)\}',line,re.IGNORECASE);
				txt = srh.group(1)
				if not props.has_key(txt):
					print 'The property '+txt+' has beed used before it has been defined'
					break
				else:
					line = line.replace(str('${'+txt+'}'),str(props[txt]))
					break
			props[line.split('=')[0].strip()] = line.split('=')[1].strip()
	return props
