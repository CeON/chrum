import sys
#import os
import for_curious.copy_oozie
import for_curious.params_combination
import for_curious.prepaire_tmp_mirror

if len(sys.argv) < 4:
	print "Usage:\n\
	\tpython full_chrum_action.py <chrum-properties-file> <workflow-properties> <chrum-workflow-xml>"
else:
	print "CEM generation have started"
	print "It may take about one minute..."
	#create a copy of given resources in HDFS and locally 
	compilation_time, keywords, chrumprops, root_dir = for_curious.copy_oozie.main(sys.argv)
	#get info about combinations of parameters 
	keys, combs, names = for_curious.params_combination.main(sys.argv[2])
	#for each combination create local ignition scripts 
	for_curious.prepaire_tmp_mirror.main(compilation_time, keywords, chrumprops, keys, combs, names, root_dir)
	print "CEM generation successfully finished!"