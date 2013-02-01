#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''

import shutil
import time
import re
import os
import sys
###############################################
######## DEFINITION BLOCK #####################
###############################################
def copyFilesNeeded(propsDir,directory,compilation_time, copylist):
	shutil.copy(sys.argv[1], directory)
	proj_props = ''
	idx = sys.argv[2].rfind('/')
	if idx !=-1:
		proj_props = sys.argv[2][idx+1:]
	else:
		 proj_props = sys.argv[2]
	
	fr = open(sys.argv[2],'r')
	fw = open(directory+'/'+proj_props,'w')
	fw.write('COMPILATION_TIME='+compilation_time+'\n'+fr.read())
	fw.close();fr.close()
	os.makedirs(directory+'/results')
	shutil.copy(sys.argv[3], directory)
	currDir = os.getcwd()
	os.chdir(sys.argv[2][:idx])
	for di,fils in copylist.items():
		fulldi = directory+di+'/'
		for fi in fils: 
			a = os.path.realpath(fi);b = fulldi
			if os.path.isdir(a):
				shutil.copytree(a, b)
			else:
				os.makedirs(fulldi)
				shutil.copy(a,b)
	os.chdir(currDir)

def readFileToString(path):
	file_ = open(sys.argv[1],'r')
	text_ = file_.read()
	file_.close()
	return text_

def removeComments(text):
	text = re.sub('#[^\n]*','',text)		
	text = re.sub(re.compile('\'\'\'.*?\'\'\'',re.DOTALL),'',text)
	return text

def getCommandLineProps(allParams):
	chrumprops = {}
	for par in allParams[4:]:
		if par.startswith('-D') and par.find('=') != -1 and par.find('=') != 2:
			chrumprops[par[2:].split('=')[0]]=par[2:].split('=')[1]
	return chrumprops

def readChrumProps(chrumPropsText,otherPropsDict):
	copylist = {}
	keywords = {}
	for line in chrumPropsText.split('\n'):
		line = line.strip()
		if line.find('=') != -1:
			for match in re.finditer('\$\{([^\}]+)\}',line,re.IGNORECASE):
				if otherPropsDict.has_key(match.group(1)):
					line = line.replace('${'+match.group(1)+'}',otherPropsDict[match.group(1)])
				else:
					raise Exception('Undefined parameter \''+match.group(1)+'\' in chrum-properties-file. \
					\nFirst provide parameter value, then use it.')
			if any((line.split('=')[0] == 'HDFS',
				line.split('=')[0]=='LOCAL',
				line.split('=')[0]=='PROJECT',
				line.split('=')[0]=='OOZIE_SERVER',
				line.split('=')[0]=='OOZIE_PORT')):
				keywords[line.split('=')[0]]=line.split('=')[1]
			else:
				otherPropsDict[line.split('=')[0]]=line.split('=')[1]
		elif line.find('<-') != -1:
			to = line.split('<-')[0].strip()
			which = line.split('<-')[1].split(',')
			which = map(str.strip,which)
			copylist[to]=which

	return otherPropsDict, copylist, keywords

def main(args):
		otherprops = {}
		if len(args) > 4:
			otherprops = getCommandLineProps(args)
	
		chrumpropstext = removeComments(readFileToString(args[1]))
		chrumprops, copylist, keywords = readChrumProps(chrumpropstext,otherprops)
		
		propsDir = os.path.dirname(os.path.realpath(args[1]))
		propsDir = propsDir[:propsDir.rindex('/')]
	
		compilation_time = str(time.time())
		root_dir = '/tmp/chrum/'+compilation_time+'/'+keywords['PROJECT']+'/'+compilation_time+'/'
		directory = root_dir+'/default/'
		os.makedirs(directory)
	
		copyFilesNeeded(propsDir,directory,compilation_time,copylist)
		
		return compilation_time, keywords, chrumprops, root_dir

