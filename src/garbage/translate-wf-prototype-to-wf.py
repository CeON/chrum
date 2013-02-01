#!/usr/bin/python
'''
 (C) 2010-2012 ICM UW. All rights reserved.
'''
import string;
import sys;
import re;
import collections;
import pickle
from wf_transformations import transformations
# create an output file from a prototype file.
# at first remove comments

in_path = sys.argv[1];
out_path = re.sub(r''+name_from+'',name_to+'',sys.argv[1])


in_file = open(in_path,'r')
whole_thing = in_file.read()
in_file.close()

def a(): 
	print "this is a" 

def b(): 
	print "this is b" 

lst = [a(), b()] 

lst 

#create a list of transformations

whole_thing = whole_thing.replace("A", "Orange");
text_file.write(whole_thing);
text_file.close();


for line in in_file:
	re.sub(r'<!--[\S\s.]+?-->',r'',s)
	new=string.replace(line,param,val)
	out_file.write(new)

out_file = open(out_path,'rw')
out_file.close()


with open(out_path, "wt") as out:
    for line in open("Stud.txt"):
        out.write(line.replace('A', 'Orange'))

print './'+out_path
