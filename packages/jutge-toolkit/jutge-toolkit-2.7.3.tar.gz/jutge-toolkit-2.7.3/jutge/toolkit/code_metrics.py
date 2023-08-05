#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import lizard
from shutil import which
from colorama import init, Fore, Style


program = sys.argv[1]
output = sys.argv[2] if len(sys.argv) == 3 else None


filename, extension = os.path.splitext(program)
bindir = os.path.dirname(os.path.realpath(__file__))

argon_installed = True

# ----------------------------------------------------------------------------
# Check for missing dependencies
# ----------------------------------------------------------------------------

def check_dependencies():
    check_list = ['cloc', 'argon']
    missing_list = []

    for program in check_list:
        if which(program) is None:
            missing_list.append(program)

    if 'argon' in missing_list:
        print(Fore.YELLOW + 'Warning: argon is not installed, you will not be able to generate code metrics for Haskell scripts!\n' + Style.RESET_ALL)
        global argon_installed
        argon_installed = False
        missing_list.remove('argon')

    if missing_list:
        print(Fore.RED + 'The following dependencies are missing, please install them and try again: ', end='')
        for missing_dep in missing_list:
            if missing_dep != missing_list[-1]:
                print(missing_dep, end=', ')
            else:
                print(missing_dep + Style.RESET_ALL)
        sys.exit(0)


# ----------------------------------------------------------------------------
# Generate code metrics
# ----------------------------------------------------------------------------

def main():
	check_dependencies()

	# count total number of lines
	lines = len(open(program, "r").readlines())

	# call lizard
	ana = lizard.analyze_file(program)

	# call cloc
	cloc = subprocess.getstatusoutput("cloc --csv %s 2> /dev/null | tail -1" % program)[1].split(",")

	# call commentedCodeDetector.py
	halstead = {}
	if extension in [".cc", ".c", ".java", ".py"]:
		out = subprocess.getstatusoutput("python3 %s/commented_code_detector.py -fm %s 2> /dev/null" % (bindir, program))[1]
		for line in out.split("\n"):
			key, val = map(str.strip, line.split())
			halstead[key] = float(val)

	# call argon
	argon = None
	if extension == ".hs":
		if not argon_installed:
			sys.exit(0)
		out = subprocess.getstatusoutput("argon --json %s 2> /dev/null" % program)[1]
		argon = json.loads(out)[0]['blocks']


	# build the output

	inf = {}
	ccn_max = 0.0
	inf = {}


	if argon is not None:
		for func in argon:
			f = {}
			f['name'] = func['name']
			f['long_name'] = str(func['name'])+":"+str(func['col'])
			f['ccn'] = func['complexity']
			inf[f['name']] = f
			ccn_max = max(f['ccn'], ccn_max)

	for func in ana.function_list:
		f = {}
		f['name'] = func.name
		f['long_name'] = func.long_name
		f['tokens'] = func.token_count
		f['nloc'] = func.nloc
		f['lines'] = func.length
		f['ccn'] = func.cyclomatic_complexity * 1.0
		f['parameters'] = func.parameters
		inf[func.name] = f
		ccn_max = max(func.cyclomatic_complexity, ccn_max)

	f = {}
	f['lines'] = lines
	f['nloc'] = ana.nloc
	f['tokens'] = ana.token_count
	f['name'] = program
	f['ccn'] = ccn_max
	f['comments'] = int(cloc[3])
	f['language'] = cloc[1]
	f['halstead'] = halstead
	inf["*"] = f


	# write output
	if output:
		json.dump(inf, open(output, "w"), indent=2)
	else:
		json.dump(inf, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
