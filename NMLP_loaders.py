from music21 import *
from fractions import Fraction
import pandas as pd
from os import listdir
import os
import nltk
import random
import json
import string
import re
from progress.bar import Bar
import gzip
import traceback
import numpy as np
from numpy import arange
#import zipfile
from colorama import Fore, Style
## Selecciona una carpeta por su nombre. Se adapta a diferentes tamaños de batch.

## lista de carpetas seleccionadas

def match_lengths(x, y):
        
        l_x = len(x)
        l_y = len(y)
        rst = None
        if l_x > l_y:
                return (True, x[:l_y], x)
                        
        else:
                return (False, x)

selected = list()

def select_files(multiple_folder_selection=False, split_by_voices=True):
        composer = None
        files = None
        dct = dict()
        if multiple_folder_selection is True:
                files = list()
                composer = list()
                status = True
                while status is True:
                        print(f'Los datasets disponibles son:\n')
                        print([i for i in listdir('Comp') if i not in selected])
                        inp = input('Introduzca los directorios de interés, escriba "OK" para terminar, simplemente "All" o "All-[carpeta a excluir]"": ')
                        
                        if inp == 'All':
                                for com in [i for i in listdir('Comp') if i not in selected]:
                                        temp_list = listdir(f'Comp/{com}')
                                        files.extend(temp_list)
                                        composer.extend([com]*len(temp_list))
                                status = False
                                continue

                        if bool(re.search('All-', inp)) is True:
                                leaved_out = inp.split('-')[1]
                                for com in [i for i in listdir('Comp') if i not in selected and i != leaved_out]:
                                        temp_list = listdir(f'Comp/{com}')
                                        files.extend(temp_list)
                                        composer.extend([com]*len(temp_list))
                                status = False
                                continue

                        ## cutre pero funciona por ahora
                        selected.append(inp)

                        if inp == 'OK':
                                status = False
                                continue
                        temp_list = listdir(f'Comp/{inp}')
                        files.extend(temp_list)
                        composer.extend([inp]*len(temp_list))
        else:
                composer = input('Introduzca el nombre del directorio de obras a cargar: ')
                selected.append(composer)
                files = listdir(f'Comp/{composer}')
                composer = [composer]*len(files)

	##solo trabaja con musicxml y kern
        ##Falta implementarlo para cuando se elige más de una carpeta de archivos.
        if split_by_voices is False:
                return [files, 'All', composer]
        else:
                for i, n in zip(files, composer):
                        if bool(re.search('krn', i)) == True:
                                file = open(f'Comp/{n}/' + i, 'r')
                                data = file.read()
                                ## problema con esta búsqueda.
                                parts = len(re.findall("\*\*kern\t", data))+1
                                try:
                                        dct[parts].append(i)
                                except:
                                        dct[parts] = [i]
                                continue

                        ## no funciona con algunos archivos

                        #file = None
                        # if bool(re.search('.mxl', i)) == True:
                        #         file = extract_mxl(f'Comp/{n}/' + i)['META-INF/container.xml']
                        #         ocurrences = file.count("<part id=")
                        # else:
                        #         file = open(f'Comp/{n}/' + i, 'r')
                        #         data = file.read()
                        #         ocurrences = data.count("<part id=")

                        ## menos eficiente pero por ahora es lo que mejor funciona

                        parts = len(converter.parse(f'Comp/{n}/' + i).parts)
                        
                        try:
                                dct[parts].append([i, n])
                        except:
                                dct[parts] = [[i, n]]
        
        x = input(f'El conjunto contiene obras clasificadas en {len(dct)} agrupaciones diferentes con {sorted(dct.keys())} voces. ¿Qué subset desea importar? ')  
        ##Debe ser un entero de la lista. Si se introduce otra cosa dará error.
        return [dct, int(x)]