from assets import loadMelodic, select_files, corpora_parser, match_lengths, csv_export, csv_import
from music21 import *
import argparse
import time
import os
from colorama import Fore, Style

def booleanizar(x):

    if x == 'y':
        return True
    elif x == 'n':
        return False
    else:
        return 'Error.'

n = None
mode = None
voice_selec = None
stack = None
diatonic = None
base40 = None

def main():

	global n, mode, diatonic, base40

	parser = argparse.ArgumentParser()
	parser.add_argument("--n", required=True)
	parser.add_argument("--mode", required=True, type=str)
	parser.add_argument("--diatonic", required=True)
	parser.add_argument("--base40", required=True)
	args = parser.parse_args()

	n = args.n
	mode = args.mode
	diatonic = eval(args.diatonic)
	base40 = eval(args.base40)

	return n, mode, diatonic, base40

if __name__ == "__main__":
    main()
