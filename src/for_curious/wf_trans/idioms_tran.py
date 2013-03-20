#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''
from idioms.seqIdiom import *

def appendSpace(x):
	return x+' '

def appendNewLine(x):
	return x.strip()+'\n'

def idioms_replacement(text,props,path):
	'''	
	The dictionary of idioms. 
	To add a new idiom add its prefix as a key AND a function which will interpret it
	You add your function into the directory ./idioms/ 
	'''
	idioms = {'seq(':seq}
	out_text = []
	#print text
	for line in text.split('\n'):
		#print 'in : ' + line
		#words=line.split(' ')
		out_line = []
		for word in line.split(' '):
			idiomDetected = False
			for idiom in idioms.keys():
				#print idiom
				if(word.startswith(idiom)):
					tmp = idioms[idiom](word,props)
					#print 'out: '+outline
					out_line.append(tmp)
					idiomDetected = True
					break;
			if not idiomDetected:
				#print 'out: '+word
				out_line.append(word)
		out_text.append(''.join(map(appendSpace,out_line)))
	return ''.join(map(appendNewLine,out_text))

