#!/usr/bin/python
'''
 (C) 2010-2012 ICM UW. All rights reserved.
'''
import re;

def insert_conf(text,props,path):
	ret_text = []
	idioms = ['seq\([^,]*,[^,]*,[^\)]*\)']
	for line in text.split('\n'):
		line=line.strip()
		proceed = False
		for idiom in idioms:
			if re.search(idiom,line):
				proceed = True
				break
		if proceed:
			while line.find('${')!=-1:
				srh = re.search('\$\{([^\}]+)\}',line,re.IGNORECASE);
				txt = srh.group(1)
				if props.has_key(txt): #TODO zrob cos zeby obslugiwac braki w wywolaniu
					line = line.replace(str('${'+txt+'}'),str(props[txt]))
				else:
					break
		ret_text.append(line)
			
	return '\n'.join(ret_text)
