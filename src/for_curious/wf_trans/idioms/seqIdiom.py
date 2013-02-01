import re
###
# the fuction for substituting seq() idiom
###
class ConfigurationFileError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def isnumeric(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def isvariable(x):
	pattern = re.compile('\$\{[^\}]*\}')
	return pattern.match(x)

def seq(word,props):
        #print "used"
	seqsplit = re.search('seq\(([^,]+),([^,]+),([^\)]*)\)', word, re.IGNORECASE)
	params = ['blank','blank','blank']
	for i, _ in enumerate(params):
            val = seqsplit.group(i+1)
            if isnumeric(val):
		params[i] = val
            elif isvariable(val):
		try:
                    tmp = props[val[2:-1]]
                    if isnumeric(tmp):
			params[i] = tmp
                    else:
			raise ConfigurationFileError('In the given properties \
			file the property '+val+' has the value '+tmp+' \
			which is not numeric BUT is used in IDIOM \'sep\'.\n\
			Please, change a property used in IDIOM \
			or change parameter value to numeric.')
                except KeyError:
                    raise ConfigurationFileError('In the given properties file the property '+val+' could not be find.\n Please, provide this variable')
        output = ''
        iter = int(params[0])
        softborder = int(params[1])
        step = int(params[2])
        #print 'inside'
        while iter<softborder: 
            #print 'in-inside'
            output = output +str(iter)+ " "
            iter=iter+step
        return output.strip()

#############################################################################
#############################################################################
#############################################################################
