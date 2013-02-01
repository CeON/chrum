import sys
import os
import for_curious.copy_oozie
import for_curious.params_combination
import for_curious.prepaire_tmp_mirror

if len(sys.argv) < 4:
	raise Exception("Usage:\n\
	\t./copy_oozie.py <chrum-properties-file> <workflow-properties> <chrum-workflow-xml>")
else:
#	print sys.argv[1]
#	print sys.argv[2]
#	print sys.argv[3]
	compilation_time, keywords, chrumprops, root_dir = for_curious.copy_oozie.main(sys.argv)
	keys, combs, names = for_curious.params_combination.main(sys.argv[2])
	for_curious.prepaire_tmp_mirror.main(compilation_time, keywords, chrumprops, keys, combs, names, root_dir)
