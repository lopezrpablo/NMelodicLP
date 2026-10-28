# Natural Melodic Language Processing (NMLP)
# Copyright (C) 2026 Pablo López-Rocamora
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


from NMLP_loaders import loadMelodic, select_files, corpora_parser, match_lengths, csv_export, csv_import
from music21 import *
import argparse
import time
import os
from decouple import config, AutoConfig
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

inp = input(f"La carpeta contenedora de la música es {config('MUSIC_FOLDER')}. Introduzca un nombre distinto o N, para conservar el nombre: ")

if inp.upper() != 'N':
    with open('.env', 'r') as f:
        lines = f.readlines()

    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('MUSIC_FOLDER='):
                f.write(f'MUSIC_FOLDER={inp}\n')
            else:
                f.write(line)
    os.environ['MUSIC_FOLDER'] = inp
else:
    os.environ['MUSIC_FOLDER'] = config('MUSIC_FOLDER')
    
guardian = False
spt = None

while guardian is False:
    spt = input('¿Desea realizar una carga parcial de los datasets basada en el número de voces de sus obras? y/n: ').lower()

    if spt == 'y' or spt == 'n':
        spt = True
        guardian = True
        
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        continue

mfol_1 = None
mfol_2 = None

guardian_2 = False

while guardian_2 is False:
    mfol_1 = booleanizar(input('¿Desea realizar una selección multi-carpeta en el conjunto 1? y/n: ').lower())
    if isinstance(mfol_1, bool):
        mfol_1 = mfol_1
    else:
        continue
    mfol_2 = booleanizar(input('¿Desea realizar una selección multi-carpeta en el conjunto 2? y/n: ').lower())
    if isinstance(mfol_2, bool):
        mfol_2 = mfol_2
        guardian_2 = True
        continue
    else:
        continue

os.system('cls' if os.name == 'nt' else 'clear')

morales_fnames_and_others = select_files(split_by_voices=spt, multiple_folder_selection=mfol_1)
otros_fnames_and_others = select_files(split_by_voices=spt, multiple_folder_selection=mfol_2)

print(Fore.GREEN + 'Los ficheros cargaron correctamente.' + Style.RESET_ALL)
time.sleep(3)

os.system('cls' if os.name == 'nt' else 'clear')

comp1 = input('Introduzca el identificador para el primer compositor o grupo de compositores seleccionados: ')
comp2 = input('Introduzca el identificador para el segundo compositor o grupo de compositores seleccionados: ')

print('OK!')

os.system('cls' if os.name == 'nt' else 'clear')

#### extraccion

## definir voice selec
# y stack

stack = None
voice_selec = None

try:
	voice_selec = int(input('Introduzca el número ordinal de la voz del interés de su análisis o, en su lugar, All: '))
	stack = False
except:
	voice_selec = 'All'
	stack = True

try:
	n = int(n)
	print('Extrayendo {0}-gramas'.format(n))
	morales = corpora_parser(n, morales_fnames_and_others, otros_fnames_and_others, diatonic=diatonic, base40=base40, stack=stack, mode=mode, voice_selec=voice_selec)
	otros = corpora_parser(n, otros_fnames_and_others, morales_fnames_and_others, diatonic=diatonic, base40=base40, stack=stack, mode=mode, voice_selec=voice_selec)
	csv_export(morales, composer=comp1)
	csv_export(otros, composer=comp2)

except:
	nn = n.split('-')
	start = int(nn[0])
	end = int(nn[1])
	for i in range(start, end+1):
		print('Extrayendo {0}-gramas'.format(i))
		morales = corpora_parser(i, morales_fnames_and_others, otros_fnames_and_others, diatonic=diatonic, base40=base40, stack=stack, mode=mode, voice_selec=voice_selec)
		otros = corpora_parser(i, otros_fnames_and_others, morales_fnames_and_others, diatonic=diatonic, base40=base40, stack=stack, mode=mode, voice_selec=voice_selec)
		csv_export(morales, composer=comp1)
		csv_export(otros, composer=comp2)
		os.system('cls' if os.name == 'nt' else 'clear')


print(Fore.GREEN + 'La ejecución ha finalizado.' + Style.RESET_ALL)
