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


def NODETRANSFORMATIONactionTran(text):

	actDict = {}
	replaceDict = {}
	out_script = []
	starts = [m.start() for m in re.finditer('# BEG:ACTION',text)]
	ends = [m.start() for m in re.finditer('# END:ACTION',text)]
	
	if len(starts) != len(ends):
		raise WorkflowFileError('The number of ACTION opening statement is not equal with closing statements. Check your workflow prototype again')
	for idx,sta in enumerate(starts):
		sto = ends[idx]
		mid = text[sta:sto].index('\n')+sta
		slic = text[sta:mid]
		regscript = text[mid:sto]
		try:
			wyn = re.search('([\w]+=[\w]+)[\W]+([\w]+=[\w]+)[\W]+([\w]+=[\w]+)[\W]*',slic,re.IGNORECASE).groups()
			for i in wyn:
				i2 = i.split('=')
				actDict[i2[0]]=i2[1]
			
			if not actDict.has_key('name') or not actDict.has_key('ok') or  not actDict.has_key('error'):
				raise WorkflowFileError('ACTION block requires 3 parameters: name, ok, error, describing respectively a current node name, a next node in case of success or failure')

			out_script.append("	<action name='"+actDict['name']+"'>\n");
			out_script.append(regscript)
			out_script.append("		<ok to='"+actDict['ok']+"'/>\n");
			out_script.append("		<error to='"+actDict['error']+"'/>\n");
			out_script.append("	</action>\n");
			out_script.append("\n\n");			
			
			name = slic
			if replaceDict.has_key(name):
				raise WorkflowFileError('Alias '+name+' has been used more then once. Please, use each alias only once.')
			content = ''.join(out_script)
			replaceDict[name] = content;
		except WorkflowFileError as e:
			print e.value
			pass

	for i in replaceDict:
		text = re.sub(r''+i+'[.\S\s]*?\# END\:ACTION', replaceDict[i], text)

	return text
