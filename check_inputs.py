#!/usr/bin/env python3

"""
Cross-check where all the input files in config.yaml are used.
"""

from glob import glob
import re
import yaml
import os

notfound = []  # list of files referred to only in config.yaml

configfname = 'config.yaml'
fnames = [ f for f in glob('*') if os.path.isfile(f) ]
fnames.sort()

with open(configfname, 'r') as configf:
    configyaml = yaml.load(configf, Loader=yaml.FullLoader)
    input = configyaml.get('input')
    for inpath in input:
        if os.path.isdir(inpath):
            inpaths = glob(os.path.join(inpath, '*'))
            inpaths.sort()
        else:
            inpaths = [ inpath ]
        for infile in [ os.path.basename(inp) for inp in inpaths ]:
            print('\n'+infile)
            if os.path.isdir(inpath):
                print(configfname, ':', inpath)
            found = False
            for fname in fnames:
                with open(fname, 'r') as f:
                    for line in f:
                        if re.search(infile, line):
                            print(fname, ':', line, end='')
                            if fname != configfname:
                                found = True
            if not found:
                print('*** not found except in', configfname, '***')
                notfound.append(infile)

print()
print(len(notfound), configfname, 'input file(s) not referred to anywhere else')
for f in notfound:
    print('  ', f)
