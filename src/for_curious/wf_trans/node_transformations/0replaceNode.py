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


def NODETRANSFORMATIONreplaceTran(text):

	replaceDict = {}

	starts = [m.start() for m in re.finditer('# BEG:REPLACE',text)]
	ends = [m.start() for m in re.finditer('# END:REPLACE',text)]
	
	if len(starts) != len(ends):
		raise WorkflowFileError('The number of REPLACE opening statement is not equal with closing statements. Check your workflow prototype again')
	for idx,sta in enumerate(starts):
		sto = ends[idx]
		mid = text[sta:sto].index('\n')+sta
		slic = text[sta:mid]
		try:
			shr = re.search('(\@[^\@]*\@)',slic,re.IGNORECASE)
			if len(shr.groups())>1:
				raise WorkflowFileError('More then one alias for a block is not allowed for a REPLACE block')
			name = shr.group(1)
			if replaceDict.has_key(name):
				raise WorkflowFileError('Alias '+name+' has been used more then once. Please, use each alias only once.')
			content = text[mid:sto]
			for i in replaceDict:
				content = content.replace(i, replaceDict[i])
			replaceDict[name] = content;
		except WorkflowFileError as e:
			print e.value
			pass

	text = re.sub(r'\# BEG\:REPLACE[.\S\s]*?\# END\:REPLACE', '', text)

	for i in replaceDict:
			text = text.replace(i, replaceDict[i])
	return text
