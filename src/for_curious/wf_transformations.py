#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''
import sys
import xml.dom.minidom
from wf_trans.idioms_tran import *
from wf_trans.rem_comments_tran import *
from wf_trans.rem_many_newlines import *
from wf_trans.node_tran import *
from wf_trans.conf_insert import *
from readconf import *

#############################################
########### FUNCTION DEFINITIONS ############
#############################################
def main(WFPath, PropsPath, ChrumPath):
	ChrumPath = ChrumPath + '/'
	f = open(WFPath,'r')
	wf = f.read()
	f.close()
	
	f = open(PropsPath,'r')
	con = f.read()
	f.close()
	condic = readConfiguration(con,{})
	after = allTran(wf,condic,ChrumPath)
	#print after
	xml_val = str(xml.dom.minidom.parseString(after).toprettyxml())
	
	while True:
		tmp = xml_val
		xml_val = re.sub('[\s]*\n[\s]*\n','\n',xml_val)
		if len(tmp) == len(xml_val):
			break
	
	return xml_val

transformations = [remove_one_line_comments,insert_conf,idioms_replacement,node_substitution,remove_many_newlines]
def allTran(text,props,path):
	for i in transformations:
#		print i
		text = i(text,props,path+"for_curious/wf_trans/")
	return text

#############################################
############# EXECUTION BLOCK ###############
#############################################
'''
TEST = False
if TEST:
	print main('/home/pdendek/icm_kod/CoAnSys/document-classification/src/main/oozie/dc-train-model/workflow/workflow.xml.part1',
		'/home/pdendek/icm_kod/CoAnSys/document-classification/src/main/oozie/dc-train-model/cluster.properties'
		,'/home/pdendek/workspace-CoAnSys/Chrum/src')
elif not TEST: 
	if len(sys.argv)==4:
		print main(sys.argv[1],sys.argv[2],sys.argv[3])
	elif len(sys.argv)==3:
		print main(sys.argv[1],sys.argv[2],os.getcwd())
	else:
		print "Usage:\n\
\t./wf_translations.py <path-to-workflow-xml> <path-to-properties-file> [<path-to-chrum-src-directory>]\n \
<path-to-chrum-src-directory> should be passed if a working directory of \
execution is different from chrum-src-directory"

'''
