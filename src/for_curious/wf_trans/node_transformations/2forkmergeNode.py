#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''
import re;

class WorkflowFileError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def NODETRANSFORMATIONforkMergeTran(text):

	starts = [m.start() for m in re.finditer('# BEG:FORK_MERGE',text)]
	ends = [m.end() for m in re.finditer('# END:FORK_MERGE',text)]

	if len(starts) != len(ends):
		raise WorkflowFileError('The number of FORK_MERGE opening statement is not equal with closing statements. Check your workflow prototype again')
	
	scripts = []
	
	for idx, sta in enumerate(starts):
		sto = ends[idx]
		scripts.append(particularForkMerge(text[sta:sto]))
	
	shift = 0
	for idx, sta in enumerate(starts):
		sto = ends[idx]		
		text = text[:sta+shift] + scripts[idx] + text[sto+shift:]
		shift = shift + len(scripts[idx]) - sto + sta
	
	return text

def particularForkMerge(defin):

	while True:
		tmp = defin
		defin = defin.replace('\n\n', '\n');
		if len(tmp)==len(defin):
			break
#	print defin
		
	firstNewLine = defin.index('\n')
	head = defin[len('# BEG:FORK_MERGE'):firstNewLine].strip()
	params = {}
	for part in head.split(' '):
		if part.find('=') != -1:
			params[part.split('=')[0]]= part.split('=')[1]
	if not all((params.has_key("name"),params.has_key("node_after_join"),params.has_key("error"))):
		raise Exception('FORK_MERGE block must have defined parameters name,node_after_join, error.\n\
		Provided values are: '+str(params.keys())+'. Please provide their values')
	else:
		withoutHead = defin[firstNewLine+1:len(defin)-len('# END:FORK_MERGE')]
		whlines = withoutHead.split('\n')
		var_val,surogate,all_var = getDefinitionAndSurogate(whlines)
		retval = calculateParamCombinations(var_val)
		bsurogates = createAfterForkNodesBetterSugorates(retval,var_val,surogate)
		
		finalScript = []
		finalScript.append(createForkNode(params,all_var))
		finalScript.append(createAfterForkNode(params,bsurogates))
		return ''.join(finalScript)

def createAfterForkNode(params,bsurogates):
	script = []
	for idx,bsurogate in enumerate(bsurogates):
		script.append("    <action name='"+params["name"]+"_forked_node_"+str(idx)+"'>\n");
		script.append(bsurogate)
		script.append("        <ok to='"+params["name"]+"_join'/>\n");
		script.append("        <error to='"+params["error"]+"'/>\n");
		script.append("    </action>\n");
		script.append("\n\n");
		
	script.append("\n\n\n");
	script.append("    <join name='"+params["name"]+"_join' to='"+params["node_after_join"]+"'/>\n");
	script.append("\n\n\n");
	
	return ''.join(script)

def createForkNode(params,all_var):
		script = []
		script.append("\n\n\n\n")
		script.append("    <fork name='"+params["name"]+"'>\n");
		for i in xrange(0,all_var):
			script.append("        <path start='"+params["name"]+"_forked_node_"+str(i)+"'/>\n");
		script.append("    </fork>\n");
		script.append("\n\n");
		return ''.join(script)

def createAfterForkNodesBetterSugorates(retval,var_val,surogate):
		surogates = []
		for tup in retval:
			surogate_ = surogate
			for idx,ks in enumerate(var_val.keys()):
				tmp = tup[idx]
				surogate_ = surogate_.replace(ks,tmp)
			surogates.append(surogate_)
		return surogates

def calculateParamCombinations(var_val):
		retval = []
		for tup in addmine(var_val.values(),[],0):
			retval.append(tup[::-1])
		return retval
			
def getDefinitionAndSurogate(whlines):
		var_val = {}
		surogate_ = []
		surogate = ''
		all_var = 1
		for idx,line in enumerate(whlines):
			name,values,still = getDefinition(line)
			if not still:
				break
			var_val[name]=values
			all_var*=len(values.split(' '))
	
		for line in whlines[idx:]:
			surogate_.append(line+"\n")		
		surogate = ''.join(surogate_)
		return var_val,surogate,all_var	

def getDefinition(withoutHead):
	srh = re.search('^(\@[^\@]+\@)([^\n]*)',withoutHead,re.IGNORECASE)
	if srh:
		name = srh.group(1)
		values = srh.group(2).strip()
		still = True 
	else:
		name = None
		values = None			
		still = False
	return name,values,still

def addmine(vals,upper,lev):
	if lev+1==len(vals):
		retval = []
		for val in vals[lev].split(' '):
			retval.append((val,))
		return retval
	retval = []
	for i in vals[lev].split(' '):
		rets = addmine(vals,upper,lev+1)
		for ret in rets:
			tup = ret+(i,)
			retval.append(tup)
	return retval

	