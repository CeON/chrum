#!/usr/bin/python
'''
 (C) 2010-2013 ICM UW. All rights reserved.
'''

import shutil
import time
import re

###############################################
######## DEFINITION BLOCK #####################
###############################################
def main(propsPath):

		f = open(propsPath,'r')
		text = f.read()
		f.close()

		var_val = {}

		for line in text.split('\n'):
			line = line.strip()
			for i in re.finditer('^@([^@\W]+?)@([^\n]+)',line):
				var_val[i.group(1)] = list(re.search('([^\W]+)',i.group(2)).groups())
		combs = calculateParamCombinations(var_val)
		coolNames = createCoolName(combs,var_val.keys())
		return var_val.keys(), combs, coolNames

def createCoolName(combs,keys):
	retval = []
	for comb in combs:
		final = []
		for idx,tup in enumerate(comb):
			final.append(str(keys[idx])+'__'+str(tup)+'__')
		retval.append(','.join(final))
	return retval
		
def calculateParamCombinations(var_val):
		retval = []
		for tup in addmine(var_val.values(),[],0):
			retval.append(tup[::-1])
		return retval

def addmine(vals,upper,lev):
	if lev+1==len(vals):
		retval = []
		for val in vals[lev]:
			retval.append((val,))
		return retval
	retval = []
	for i in vals[lev]:
		rets = addmine(vals,upper,lev+1)
		for ret in rets:
			tup = ret+(i,)
			retval.append(tup)
	return retval

