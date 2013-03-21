#!/usr/bin/python

import sys
import os 
from src.for_curious import wf_transformations

def writeFile(path,txt):
    f = open(path,'w')
    f.write(txt)
    f.close()

def main(args):
    execPath = ''
    if args[0].rindex('/') != -1:
        execPath = args[0][:args[0].rindex('/')] 
    else:
        execPath = os.getcwd()

    wftxt = wf_transformations.main(execPath,args[1],args[2])
    
    if len(args)==4:
        try:
            with open(args[3]):
                print 'File already exist in a given localization.'
        except IOError:
            writeFile(args[3],wftxt)
    elif len(args)==5:
        writeFile(args[3],wftxt)
    else:
        print wftxt
    

if len(sys.argv) < 3 or len(sys.argv) > 5:
    print "Usage:\n\tpython full_chrum_action.py <oozie-workflow-properties> <chrum-workflow-xml> [<output-xml-destination> [!]]"
    print "where\n\
    <oozie-workflow-properties> is a path to a Oozie workflow file accompanied with Chrum syntax\n\
    <output-xml-destination> is a path to a generated workflow file e.g. /tmp/output.workflow.xml\n\
    ! - as a 5th parameter - force writing to <output-xml-destination> even if a file already exists in a given localization"
else:
    main(sys.argv)