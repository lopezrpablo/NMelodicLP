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
from colorama import Fore, Style
from decouple import config

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

def corpora_parser(n, data, data2, diatonic=False, base40=True, stack=True, mode='Iibd', voice_selec='All'):
        ## si se selecciona voice_selec como All, esto aplicará necesariamente a todo, 
        ## de otra manera no tendría sentido hacer esto. 
        
        ## mode puede ser Iibd para TODO; o bien Ii, Ib, bd, etc... distintas combinaciones

        if diatonic is True:
                ## por seguridad.
                ## los intervalos diatónicos se despojan de información extra: alteraciones, etc. Ralentiza mucho la extracción.

                #puede que esto no esté funcionando
                base40 = False


        word_corpus = list()
        ngram_corpus = list()
        histogram = list()
        if data[1] == 'All':
                bar = Bar('Processing', max=len(data[0]))
                for z,(i, x) in enumerate(zip(data[0], data[2])):
                        #print('Parsing file ' + str(z) + f': {i}')
                        raw = converter.parse(f"{os.environ['MUSIC_FOLDER']}/{x}/{i}").stripTies()
                        strings = loadMelodic(raw, base40, mode, diatonic)
                        if 'I' in mode:

                                hist_temp = loadMelodic(raw, base40, mode, diatonic).iors_histogram()
                                histogram.extend(hist_temp)

                        else:pass
                                
                        temp = strings.tokenize(n, stack, mode)
                        if voice_selec == 'All':
                                temp_2 = list(temp)
                                ngram_corpus.append(temp_2)
                        else:
                                ## debe ser un número entero, de 1 a 4, por ejemplo.
                                temp_2 = temp[voice_selec].dropna()
                                ngram_corpus.append(list(temp_2))
                                
                        wds = strings.words(stack, mode)
                        ## WORDS
                        if stack is False:
                                wds = wds[voice_selec].dropna()
                                word_corpus.append(list(wds))
                        else:
                                wds = list(wds)
                                word_corpus.append(wds)
                        bar.next()
                bar.finish()
                return [ngram_corpus, word_corpus, histogram, data[0], (n, mode, voice_selec, base40, diatonic)]
        
        else: 
                ## este bloque iguala la cantidad de puntos de datos para cada conjunto si no son equiparables. REVISAR.
                """filtered = match_lengths(data[0][data[1]], data2[0][data2[1]])
                
                if filtered[0] is False:
                        pass
                else:print(Fore.RED + f'Aviso: la longitud de este conjunto se ha acortado desde {len(filtered[2])} a {len(filtered[1])} items, para emparejarlo en cuanto a volumen con el restante.' + Style.RESET_ALL)"""
                
                #bar = Bar('Processing', max=len(filtered[1]))
                bar = Bar('Processing', max=len(data[0][data[1]]))

                #for z,i in enumerate(filtered[1]):
                for z,i in enumerate(data[0][data[1]]):
                        c = i[1]
                        f = i[0]

                        #print('Parsing file ' + str(z) + f': {f}')
                        raw = converter.parse(f"{os.environ['MUSIC_FOLDER']}/{c}/{f}").stripTies()

                        ## Dataframes con cada parte codificada por voz de una sola obra
                        # La columna 1 equivale a la voz 1

                        strings = loadMelodic(raw, base40, mode, diatonic)

                        if 'I' in mode:
                                hist_temp = loadMelodic(raw, base40, mode, diatonic).iors_histogram()
                                histogram.extend(hist_temp)
                        else:pass
                                
                        ## Añadir modo: everything, ior, intervals
                        ### NGRAMAS
                        #se puede procesar por voces separadas o combinar todos
                        ## stack = True apila los ngramas de todas las voces verticalmente, si no, False
                        #por ahora el enfoque es meterlo todo en un mismo saco
                        ##lo convierto en lista. Con stack=True se puede dado que se trata de una sola columna.
                        temp = strings.tokenize(n, stack, mode)
                        if voice_selec == 'All':
                                temp_2 = list(temp)
                                ngram_corpus.append(temp_2)
                        else:
                                ## debe ser un número entero, de 1 a 4, por ejemplo.
                                temp_2 = temp[voice_selec].dropna()
                                ngram_corpus.append(list(temp_2))
                                
                        wds = strings.words(stack, mode)
                        ## WORDS
                        if stack is False:
                                wds = wds[voice_selec].dropna()
                                word_corpus.append(list(wds))
                        else:
                                wds = list(wds)
                                word_corpus.append(wds)
                        bar.next()
                bar.finish()
                try:
                        return [ngram_corpus, word_corpus, histogram, [i[0] for i in filtered], (n, mode, voice_selec, base40, diatonic)]
                except:
                        return [ngram_corpus, word_corpus, histogram, [i[0] for i in data[0][data[1]]], (n, mode, voice_selec, base40, diatonic)]

def csv_export(data, composer=str()):

        n = data[4][0]
        words = data[1]
        mode = data[4][1]
        voice = data[4][2]
        b40 = data[4][3]
        diat = data[4][4]

        features_csv = '; '.join([i for i in mode]) + '\n'

        name = ''
        if b40 is True:
                name = f'{composer}_{n}grams_{mode}_voice-{voice}_b40.csv'
        elif diat is True:
                name = f'{composer}_{n}grams_{mode}_voice-{voice}_dia.csv'
        else:
                name = f'{composer}_{n}grams_{mode}_voice-{voice}.csv'
                
        if os.path.isdir('Exports'):
                f = gzip.open(f'Exports/{name}' + '.gz', 'wb')
        else:
                os.mkdir('Exports')
                f = gzip.open(f'Exports/{name}' + '.gz', 'wb')

        f.write(features_csv.encode('utf-8'))
        for i, z, e in zip(data[0], data[3], words):
                line = ''
                for x in i:
                        line += str(x) + '; '
                line += z
                f.write(str(line + '\n').encode('utf-8'))
                f.write(str(str(tuple(e)) + '\n').encode('utf-8'))

        return f'Backup file {name} correcty generated. Navegate to Exports directory.'


def str2tuple(lst, rid=None, indexes=None, header=None):

        myList = list(eval(lst))
        myList2 = list()

        if indexes is None:
                myList2 = myList
        else:
                n_deletions = len(indexes)
                n_heads = len(header)

                if n_deletions >= n_heads:
                        return 'Error grave. El parámetro rid puede contener hasta un máximo de tres caracteres'

                for z in myList:
                        if bool(re.search('<R>', z)) == True:

                                if 'd' in header and header.index('d') not in indexes:

                                        temp = re.sub('<R>', '~', z)
                                        temp2 = ''
                                        for n, i in enumerate(temp):
                                                if n in indexes:pass
                                                else:temp2 += i

                                        myList2.append(re.sub('~', '<R>', temp2))
   
                                else:
                                        myList2.append('<R>' * (n_heads - n_deletions))

                        elif bool(re.search('<s>', z)) == True:
                                myList2.append('<s>')

                        elif bool(re.search('</s>', z)) == True:
                                myList2.append('</s>')
                        else:
                                rst = ''.join(z[i] for i in range(len(header)) if i not in indexes)
                                myList2.append(rst)                                
        myList = list(map(str, myList2))
        myTuple = tuple(myList)
        return myTuple

def csv_import(file, rid=None):

        with gzip.open(file, 'rt') as compressed:
                f = compressed.read().split('\n')

        if rid is not None:
                header = f[0].split('; ')
                indexes = [header.index(i) for i in rid]
        
        files = list()
        ngrams = list()
        words = list()
        for n, i in enumerate(f):

                if n == 0:continue # header

                if n == len(f)-1:break

                if (n+1) % 2 != 0:
                        if rid is None:
                            lst = list(str2tuple(i))
                        else:
                            lst = list(str2tuple(i, rid, indexes, header))
                        if 'Error' in lst:
                                return traceback.print_stack()
                        words.append(lst)

                else:
                        line = i.split('; ')
                        files.append(line[-1])
                        work_list = list()
                        for x in line[:-1]:
                                tpl = None
                                if rid is None:
                                        tpl = str2tuple(x.rstrip().lstrip())
                                else:
                                        tpl = str2tuple(x.rstrip().lstrip(), rid, indexes, header)
                                        if 'Error' in tpl:
                                                return traceback.print_stack()

                                work_list.append(tpl)

                        ngrams.append(work_list)
        return ngrams, files, words


def unique_ior_addition(ior_dic, dur):
        new_value = None
        while True:
                valor = random.choice(string.ascii_letters)
                if valor not in ior_dic.values():
                        new_value = valor
                        break

        ior_dic[dur] = new_value
        with open('iors.json', 'w') as durations:
                json.dump(ior_dic, durations, indent=4)

## Aquí se produce toda el preprocesamiento de las partituras      

def getSimultaneousMusicCount(el, s, counter):

        offset_begin = el.getOffsetInHierarchy(s)
        offset_end = el.getOffsetInHierarchy(s)+el.quarterLength

        condiciones = ((counter[:, 0] >= offset_begin) & (counter[:, 1] <= offset_end) |
                     (counter[:, 0] <= offset_begin) & (counter[:, 1] <= offset_end) & (counter[:, 1] > offset_begin)|
                        (counter[:, 0] >= offset_begin) & (counter[:, 0] < offset_end) & (counter[:, 1] >= offset_end))

        matches = counter[condiciones]

        return int(len(matches))



class loadMelodic:
        
        def __init__(self, x, base40, mode, diatonic):
                self.x = x
                self.data = self.x.recurse().getElementsByClass(['Part','Note', 'Chord', 'Rest'])
                self.base40 = base40
                self.diatonic = diatonic
                self.mode = mode
                ## offsets almacenados evitar iteraciones innecesarias
                self.offsets = np.empty((0, 2), dtype=float)

                for i in self.x.recurse().getElementsByClass(['Note', 'Chord']):
                        if isinstance(i, note.Note):
                                starting_p = i.getOffsetInHierarchy(self.x)
                                end_p = i.getOffsetInHierarchy(self.x)+i.quarterLength
                                new = np.array([[starting_p, end_p]])
                                self.offsets = np.vstack([self.offsets, new])
                        else:
                                for n in range(0, len(i)):
                                        starting_p = i.getOffsetInHierarchy(self.x)
                                        end_p = i.getOffsetInHierarchy(self.x)+i.quarterLength
                                        new = np.array([[starting_p, end_p]])
                                        self.offsets = np.vstack([self.offsets, new])

                ######
                # ahora mode es hasta 'iIbd' con diferentes combinaciones
                ######

                p_counter = len(self.data.parts)
                for i in range(0, p_counter):
                        
                        if 'i' in self.mode:
                                globals()[f'pitch_p%s_grams' % (i+1)] = list()
                        if 'I' in self.mode:
                                globals()[f'dur_p%s_grams' % (i+1)] = list()
                        if 'b' in self.mode:
                                globals()[f'beat_p%s_grams' % (i+1)] = list()
                        if 'd' in self.mode:
                                globals()[f'density_p%s_grams' % (i+1)] = list()

                curr_part = 0
                #rest_ticks = 0
                music = False
                active_rest = False
                rest_counterpoint = None

                for i in self.data:

                        if isinstance(i, stream.Part):
                                curr_part += 1
                                #rest_ticks = 0
                                music = False
                                active_rest = False
                                if rest_counterpoint is not None:
                                        globals()[f'density_p%s_grams' % (curr_part-1)].append(rest_counterpoint)
                                        rest_counterpoint = None
                                continue

                        if isinstance(i, note.Rest) and music is False:
                                continue

                        if isinstance(i, note.Note):
                                music = True
                                active_rest = False

                                if rest_counterpoint is not None:
                                        globals()[f'density_p%s_grams' % (curr_part)].append(rest_counterpoint)
                                        rest_counterpoint = None

                                #rest_ticks = 0

                                if self.base40 is False and self.diatonic is True:

                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append(i.nameWithOctave)
                                        if 'I' in self.mode:
                                                ticks = midi.translate.durationToMidiTicks(i.duration)
                                                globals()[f'dur_p%s_grams' % (curr_part)].append(ticks)
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append(i.beatStrength)
                                        if 'd' in self.mode:
                                                globals()[f'density_p%s_grams' % (curr_part)].append(getSimultaneousMusicCount(i, self.x, self.offsets)-1)

                                if self.base40 is False and self.diatonic is False:
                                        ## modelo de María Hontanilla, al menos en intervalos e IORs
                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append(pitch.Pitch(i.nameWithOctave).midi)
                                        if 'I' in self.mode:
                                                ticks = midi.translate.durationToMidiTicks(i.duration)
                                                globals()[f'dur_p%s_grams' % (curr_part)].append(ticks)
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append(i.beatStrength)
                                        if 'd' in self.mode:
                                                globals()[f'density_p%s_grams' % (curr_part)].append(getSimultaneousMusicCount(i, self.x, self.offsets)-1)
                                        
                                else:
                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append(musedata.base40.pitchToBase40(pitch.Pitch(i.nameWithOctave)))
                                        if 'I' in self.mode:
                                                ticks = midi.translate.durationToMidiTicks(i.duration)
                                                globals()[f'dur_p%s_grams' % (curr_part)].append(ticks)
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append(i.beatStrength)
                                        if 'd' in self.mode:
                                                globals()[f'density_p%s_grams' % (curr_part)].append(getSimultaneousMusicCount(i, self.x, self.offsets)-1)

                        elif isinstance(i, chord.Chord):
                                music = True
                                active_rest = False

                                if rest_counterpoint is not None:
                                        globals()[f'density_p%s_grams' % (curr_part)].append(rest_counterpoint)
                                        rest_counterpoint = None

                                #rest_ticks = 0
                                if self.base40 is False and self.diatonic is True:

                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append(i[-1].nameWithOctave)
                                        if 'I' in self.mode:
                                                ticks = midi.translate.durationToMidiTicks(i[-1].duration)
                                                globals()[f'dur_p%s_grams' % (curr_part)].append(ticks)
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append(i[-1].beatStrength)
                                        if 'd' in self.mode:
                                                globals()[f'density_p%s_grams' % (curr_part)].append(getSimultaneousMusicCount(i, self.x, self.offsets)-1)

                                if self.base40 is False and self.diatonic is False:
                                        ## modelo de María Hontanilla, al menos en intervalos e IORs
                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append(pitch.Pitch(i[-1].nameWithOctave).midi)
                                        if 'I' in self.mode:
                                                ticks = midi.translate.durationToMidiTicks(i[-1].duration)
                                                globals()[f'dur_p%s_grams' % (curr_part)].append(ticks)
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append(i[-1].beatStrength)
                                        if 'd' in self.mode:
                                                globals()[f'density_p%s_grams' % (curr_part)].append(getSimultaneousMusicCount(i, self.x, self.offsets)-1)
                                        
                                else:
                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append(musedata.base40.pitchToBase40(pitch.Pitch(i[-1].nameWithOctave)))
                                        if 'I' in self.mode:
                                                ticks = midi.translate.durationToMidiTicks(i[-1].duration)
                                                globals()[f'dur_p%s_grams' % (curr_part)].append(ticks)
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append(i[-1].beatStrength)
                                        if 'd' in self.mode:
                                                globals()[f'density_p%s_grams' % (curr_part)].append(getSimultaneousMusicCount(i, self.x, self.offsets)-1)


                        elif isinstance(i, note.Rest):
                                music = True

                                if active_rest is False:

                                        if 'i' in self.mode:
                                                globals()[f'pitch_p%s_grams' % (curr_part)].append('<R>')
                                        if 'I' in self.mode:
                                                globals()[f'dur_p%s_grams' % (curr_part)].append('<R>')
                                        if 'b' in self.mode:
                                                globals()[f'beat_p%s_grams' % (curr_part)].append('<R>')
                                        if 'd' in self.mode:
                                                rest_counterpoint = getSimultaneousMusicCount(i, self.x, self.offsets)-1
                                        active_rest = True
                                        continue
                                else:
                                        if 'd' in self.mode:
                                                rest_counterpoint += getSimultaneousMusicCount(i, self.x, self.offsets)-1

                                        #rest_ticks = midi.translate.durationToMidiTicks(i.duration)
                                        #globals()[f'dur_p%s_grams' % (curr_part)][-1] += rest_ticks
                                        #rest_ticks = 0

                        else:
                                pass

                if rest_counterpoint is not None:
                        globals()[f'density_p%s_grams' % (curr_part-1)].append(rest_counterpoint)
                        rest_counterpoint = None

                self.voicesQuantity = p_counter
                        
        
        def intervals(self, base40, diatonic):

                itv_dic = {'0':'Y', '1':'A','2':'B','3':'C','4':'D','5':'E','6':'F','7':'G','8':'H','9':'I','10':'J','11':'K','12':'L',
                        '-1':'a','-2':'b','-3':'c','-4':'d','-5':'e','-6':'f','-7':'g','-8':'h','-9':'i','-10':'j','-11':'k','-12':'l'}

                itv_dia_dic = {'1':'A','2':'B','3':'C','4':'D','5':'E','6':'F','7':'G','8':'H','-1':'a','-2':'b','-3':'c',
                '-4':'d','-5':'e','-6':'f','-7':'g','-8':'h'}

                base40_dic = {str(n): str(i) for i, n in zip(string.printable[10:], range(-40,41))}
                
                df = pd.DataFrame()
                names = [i+1 for i in range(0, self.voicesQuantity)]
                for z in range(0,self.voicesQuantity):
                        lstt = list()


                        if self.base40 is False and self.diatonic is True:
                                for n, i in enumerate(globals()[f'pitch_p%s_grams' % (str(z+1))]):
                                        if n == len(globals()[f'pitch_p%s_grams' % (str(z+1))])-1:break
                                        if i == '<R>':
                                                lstt.append(i)
                                                int_start = pitch.Pitch(globals()[f'pitch_p%s_grams' % (str(z+1))][n-1])
                                                int_end = pitch.Pitch(globals()[f'pitch_p%s_grams' % (str(z+1))][n+1])
                                                itv = interval.Interval(int_start, int_end).generic.semiSimpleDirected

                                        elif globals()[f'pitch_p%s_grams' % (str(z+1))][n+1] == '<R>':
                                                continue

                                        else:
                                                int_start = pitch.Pitch(i)
                                                int_end = pitch.Pitch(globals()[f'pitch_p%s_grams' % (str(z+1))][n+1])
                                                itv = interval.Interval(int_start, int_end).generic.semiSimpleDirected
                                        ###
                                                
                                        if str(itv) in itv_dia_dic.keys():
                                                lstt.append(itv_dia_dic[str(itv)])
                                        else:
                                                print('Error en intervalo diatonico ' + str(itv))

                                df = pd.concat([df, pd.DataFrame(lstt)], axis=1)
                        elif self.base40 is False and self.diatonic is False:
                                for n, i in enumerate(globals()[f'pitch_p%s_grams' % (str(z+1))]):
                                        if n == len(globals()[f'pitch_p%s_grams' % (str(z+1))])-1:break
                                        if i == '<R>':
                                                lstt.append(i)
                                                itv = (globals()[f'pitch_p%s_grams' % (str(z+1))][n-1] - globals()[f'pitch_p%s_grams' % (str(z+1))][n+1]) * -1
                                        elif globals()[f'pitch_p%s_grams' % (str(z+1))][n+1] == '<R>':
                                                continue

                                        else:
                                                itv = (i - globals()[f'pitch_p%s_grams' % (str(z+1))][n+1]) * -1
                                        ###
                                                
                                        mod = None
                                        if itv > 0:
                                                if itv%12 == 0:
                                                        mod = str(12)
                                                else:
                                                        mod = str(itv%12)
                                        elif itv < 0:
                                                if itv%-12 == 0:
                                                        mod = str(-12)
                                                else:
                                                        mod = str(itv%-12)
                                        else:
                                                mod = '0'

                                        if mod in itv_dic.keys():
                                                lstt.append(itv_dic[str(mod)])
                                        else:
                                                print('Error en intervalo ' + str(mod))
                                df = pd.concat([df, pd.DataFrame(lstt)], axis=1)
                                #df.columns = names
                        else:
                                for n, i in enumerate(globals()[f'pitch_p%s_grams' % (str(z+1))]):
                                        if n == len(globals()[f'pitch_p%s_grams' % (str(z+1))])-1:break
                                        if i == '<R>':
                                                lstt.append(i)
                                                itv = (globals()[f'pitch_p%s_grams' % (str(z+1))][n-1] - globals()[f'pitch_p%s_grams' % (str(z+1))][n+1]) * -1

                                        elif globals()[f'pitch_p%s_grams' % (str(z+1))][n+1] == '<R>':
                                                continue

                                        else:
                                                itv = (i - globals()[f'pitch_p%s_grams' % (str(z+1))][n+1]) * -1
                                                
                                        mod = None
                                        if itv > 0:
                                                if itv%40 == 0:
                                                        mod = str(40)
                                                else:
                                                        mod = str(itv%40)
                                        elif itv < 0:
                                                if itv%-40 == 0:
                                                        mod = str(-40)
                                                else:
                                                        mod = str(itv%-40)
                                        else:
                                                mod = '0'

                                        if mod in base40_dic.keys():
                                                lstt.append(base40_dic[str(mod)])
                                        else:
                                                print('Error en intervalo ' + str(mod))
                                df = pd.concat([df, pd.DataFrame(lstt)], axis=1)

                return df

        
        def beatRatios(self):

                def getClosest(keys, value):

                        return keys[min(range(len(keys)), key = lambda i: abs(keys[i]-value))]

                bt_dic = {str(round(n, 1)): str(i) for i, n in zip(string.printable[10:], arange(0.0,4.1, 0.10))}

                #bt_dic = {'0.0': 'A', '0.25':'B','0.5':'C','0.75':'D','1.0':'E','1.25':'F','1.5':'G','1.75':'H','2.0':'I', 
                #'2.25':'J', '2.5':'K','2.75':'L','3.0':'M','3.25':'N','3.5':'O','3.75':'P','4.0':'Q'}
                extremos = {n: str(i) for i, n in zip(string.printable[len(bt_dic.values())+10:], ['>4', '>6', '>8', '>10']) if i not in bt_dic.values()}

                ### todas las opciones tal y como están en ior_dic (tipo string)
                keys = [float(i) for i in list(bt_dic.keys())]

                
                df = pd.DataFrame()
                names = [i+1 for i in range(0, self.voicesQuantity)]
                for z in range(0,self.voicesQuantity):
                        lstt = list()

                        for n, i in enumerate(globals()[f'beat_p%s_grams' % (str(z+1))]):
                                if n == len(globals()[f'beat_p%s_grams' % (str(z+1))])-1:break
                                if i == '<R>':
                                        lstt.append(i)
                                        beat_before = globals()[f'beat_p%s_grams' % (str(z+1))][n-1]
                                        beat_after = globals()[f'beat_p%s_grams' % (str(z+1))][n+1]
                                        ratio = beat_after / beat_before
                                        if ratio > 10:
                                                br = extremos['>10']
                                        
                                        if ratio > 8:
                                                br = extremos['>8']
                                        
                                        if ratio > 6:
                                                br = extremos['>6']
                                        
                                        if ratio > 4:
                                                br = extremos['>4']

                                        else:
                                                closest_key = getClosest(keys, ratio)
                                                br = bt_dic[str(closest_key)]

                                elif globals()[f'beat_p%s_grams' % (str(z+1))][n+1] == '<R>':
                                        continue

                                else:
                                        beat_after = globals()[f'beat_p%s_grams' % (str(z+1))][n+1]
                                        ratio = beat_after / i
                                        
                                        ## se encuentran valores mayores que cuatro repetidas veces entre la muestra (independientemente del autor)
                                        ## igualmente lo más común es entre 1 y 4 o incluso 5

                                        if ratio > 10:
                                                br = extremos['>10']
                                        
                                        if ratio > 8:
                                                br = extremos['>8']
                                        
                                        if ratio > 6:
                                                br = extremos['>6']
                                        
                                        if ratio > 4:
                                                br = extremos['>4']

                                        else:
                                                closest_key = getClosest(keys, ratio)
                                                br = bt_dic[str(closest_key)]

                                if str(br) in bt_dic.values():
                                        lstt.append(str(br))
                                        
                                elif str(br) in extremos.values():
                                        lstt.append(str(br))
                                else:
                                        print('Error en beat ratio ' + str(br))

                        df = pd.concat([df, pd.DataFrame(lstt)], axis=1)
                return df

        
        def iors(self):

                df = pd.DataFrame()
                ior_dic = {'1':'Z', '6/5':'A','5/4':'B','4/3':'C','3/2':'D','5/3':'E','2':'F','5/2':'G','3':'H','4':'I','>4.5':'Y',
                '5/6':'a','4/5':'b','3/4':'c','2/3':'d','3/5':'e','1/2':'f','2/5':'g','1/3':'h','1/4':'i','<1/4.5':'y'}
                rm = ['>4.5','<1/4.5']

                ### todas las opciones tal y como están en ior_dic (strings)
                keys_not_formated = [i for i in list(ior_dic.keys())]

                ## opciones como tipo float
                keys = [float(Fraction(i)) for i in list(ior_dic.keys()) if i not in rm] ## las opciones de rm fallarán
                keys.extend([4.5,1/4.5])  ## se añaden después en el formato adecuado

                def getClosest(keys, value):
                        
                        return keys[min(range(len(keys)), key = lambda i: abs(keys[i]-value))]
                        
                names = [i+1 for i in range(0, self.voicesQuantity)]
                histogram = list()
                for y in range(0, self.voicesQuantity):
                        lst = list()
                        nt = None
                        for n,i in enumerate(globals()[f'dur_p%s_grams' % (str(y+1))]):

                                if n == len(globals()[f'dur_p%s_grams' % (str(y+1))])-1:break

                                if i == '<R>':
                                        lst.append(i)
                                        fr = Fraction(globals()[f'dur_p%s_grams' % (str(y+1))][n+1], globals()[f'dur_p%s_grams' % (str(y+1))][n-1])
                                elif globals()[f'dur_p%s_grams' % (str(y+1))][n+1] == '<R>':
                                        continue

                                else:
                                        fr = Fraction(globals()[f'dur_p%s_grams' % (str(y+1))][n+1], globals()[f'dur_p%s_grams' % (str(y+1))][n])
                                                
                                dur = f'{fr.numerator}/{fr.denominator}'
                                
                                if dur in ior_dic.keys():
                                        lst.append(ior_dic[dur])
                                        histogram.append(dur)
                                        continue
                                else:
                                        innt = False
                                        for z in range(0,4):
                                                if fr == z+1:
                                                        lst.append(ior_dic[str(z+1)])
                                                        histogram.append(str(z+1))
                                                        innt = True
                                        if innt is True:
                                                continue

                                        if fr.numerator / fr.denominator >= 4.5:
                                                lst.append(ior_dic['>4.5'])
                                                histogram.append('>4.5')
                                                continue

                                        elif fr.numerator / fr.denominator <= 1/4.5:
                                                lst.append(ior_dic['<1/4.5'])
                                                histogram.append('<1/4.5')
                                                continue

                                        else:
                                                ## redondeo a los valores estandarizados
                                                closest_index = keys.index(getClosest(keys, Fraction(dur)))
                                                kw = keys_not_formated[closest_index]
                                                lst.append(ior_dic[kw])
                                                histogram.append(dur)
        ## Paralelamente se puede almacenar                                      

                        df = pd.concat([df, pd.DataFrame(lst)], axis=1)
                        #df.columns = names
                                                         
                return df

        
        def iors_histogram(self):

                df = pd.DataFrame()
                ior_dic = {'1':'Z', '6/5':'A','5/4':'B','4/3':'C','3/2':'D','5/3':'E','2':'F','5/2':'G','3':'H','4':'I','>4.5':'Y',
                '5/6':'a','4/5':'b','3/4':'c','2/3':'d','3/5':'e','1/2':'f','2/5':'g','1/3':'h','1/4':'i','<1/4.5':'y'}
                rm = ['>4.5','<1/4.5']
                keys_not_formated = [i for i in list(ior_dic.keys())]
                keys = [float(Fraction(i)) for i in list(ior_dic.keys()) if i not in rm]
                keys.extend([4.5,1/4.5])

                def getClosest(keys, value):
                        
                        return keys[min(range(len(keys)), key = lambda i: abs(keys[i]-value))]
                        
                histogram = list()


                for y in range(0,self.voicesQuantity):
                        nt = None
                        for n,i in enumerate(globals()[f'dur_p%s_grams' % (str(y+1))]):

                                if n == len(globals()[f'dur_p%s_grams' % (str(y+1))])-1:break

                                if i == '<R>':
                                        fr = Fraction(globals()[f'dur_p%s_grams' % (str(y+1))][n+1], globals()[f'dur_p%s_grams' % (str(y+1))][n-1])
                                elif globals()[f'dur_p%s_grams' % (str(y+1))][n+1] == '<R>':
                                        continue

                                else:
                                        fr = Fraction(globals()[f'dur_p%s_grams' % (str(y+1))][n+1], globals()[f'dur_p%s_grams' % (str(y+1))][n])
                                                
                                dur = f'{fr.numerator}/{fr.denominator}'
                                
                                if dur in ior_dic.keys():
                                        histogram.append(dur)
                                        continue
                                else:
                                        innt = False
                                        for z in range(0,4):
                                                if fr == z+1:
                                                        histogram.append(str(z+1))
                                                        innt = True
                                        if innt is True:
                                                continue

                                        if fr.numerator / fr.denominator >= 4.5:
                                                histogram.append('>4.5')
                                                continue

                                        elif fr.numerator / fr.denominator <= 1/4.5:
                                                histogram.append('<1/4.5')
                                                continue

                                        else:
                                                histogram.append(dur)
                                                         
                return histogram

        
        def contrapuntalDensityRatio(self):

                def getClosest(keys, value):

                        return keys[min(range(len(keys)), key = lambda i: abs(keys[i]-value))]

                densities_dct = {str(round(n, 1)): str(i) for i, n in zip(string.printable[10:], arange(0.0,4.1, 0.10))}

                extremos = {n: str(i) for i, n in zip(string.printable[len(densities_dct.values())+10:], ['>4', '>6', '>8', '>10']) if i not in densities_dct.values()}

                ## se generaliza demasiado. Hay muchos values intermedios, mejor con saltos de 0.10
                #densities_dct = {'0.0':'A', '0.25':'B', '0.5':'C', '0.75':'D', '1.0':'E', '1.25':'F', '1.5':'G', '1.75':'H', '2.0':'I', '2.25':'J', '2.5':'K', '2.75':'L', '3.0':'M', '3.25':'N', '3.5':'O', '3.75':'P', '4.0':'Q'}
                
                keys = [float(i) for i in list(densities_dct.keys())]
                
                df = pd.DataFrame()
                names = [i+1 for i in range(0, self.voicesQuantity)]
                for z in range(0,self.voicesQuantity):
                        
                        lstt = list()

                        for n, i in enumerate(globals()[f'density_p%s_grams' % (str(z+1))]):

                                if n == len(globals()[f'density_p%s_grams' % (str(z+1))])-1:break
                                
                                else:

                                        density_after = globals()[f'density_p%s_grams' % (str(z+1))][n+1]

                                        try:
                                                ratio = density_after / i
                                        except:

                                                lstt.append(str('+' + str(density_after)))
                                                continue
                                
                                if str(ratio) in densities_dct.keys():
                                        lstt.append(densities_dct[str(ratio)])

                                elif ratio < 4:
                                        closest_index = keys.index(getClosest(keys, ratio))
                                        kw = str(keys[closest_index])
                                        lstt.append(densities_dct[kw])

                                elif ratio > 10:
                                        lstt.append(extremos['>10'])

                                elif ratio > 8:
                                        lstt.append(extremos['>8'])
                                elif ratio > 6:
                                        lstt.append(extremos['>6'])

                                elif ratio > 4:
                                        lstt.append(extremos['>4'])
                                else:
                                        print('Error en density ratio ' + str(ratio))

                        df = pd.concat([df, pd.DataFrame(lstt)], axis=1)
                return df

        
        def concatVoices(self, mode):

                df = pd.DataFrame()
                names = [i+1 for i in range(0, self.voicesQuantity)]
                        
                for i in range(0, self.voicesQuantity):
                        temp = pd.Series()
                        for n, j in enumerate(mode):
                                if 'i' == j:
                                        ints = pd.Series(self.intervals(self.base40, self.diatonic).iloc[:, i])
                                        if n == 0:
                                                temp = ints
                                        else:
                                                temp = temp.str.cat(ints, sep='')

                                elif 'I' == j:
                                        durs = pd.Series(self.iors().iloc[:, i])

                                        if n == 0:
                                                temp = durs
                                        else:
                                                temp = temp.str.cat(durs, sep='')

                                elif 'b' == j:
                                        bts = pd.Series(self.beatRatios().iloc[:, i])
                                        if n == 0:
                                                temp = bts
                                        else:
                                                temp = temp.str.cat(bts, sep='')

                                elif 'd' == j:
                                        dst = pd.Series(self.contrapuntalDensityRatio().iloc[:, i])
                                        if n == 0:
                                                temp = dst
                                        else:
                                                temp = temp.str.cat(dst, sep='')

                        df = pd.concat([df, pd.DataFrame(temp)], axis=1)

                df.columns = names
                return df

        
        def words(self, stack, mode):

                lst = list()
                new = pd.DataFrame()
                names = [i+1 for i in range(0, self.voicesQuantity)]
                for i in self.concatVoices(mode).columns:
                        temp = self.concatVoices(mode)[i].dropna()
                        curr_ngram = pd.Series(temp)

                        if stack is True:
                                new = pd.concat([new, curr_ngram], axis=0)
                        else:
                                new = pd.concat([new, curr_ngram], axis=1)
                if stack is True:
                        new = list(new[new.columns[0]].values)
                else:
                        new.columns = names

                return new

        ##tokenizar como N-gramas y añadir padding

        
        def tokenize(self, n, stack, mode):
                lst = list()
                new = pd.DataFrame()
                names = [i+1 for i in range(0, self.voicesQuantity)]
                for i in self.concatVoices(mode).columns:

                        temp = self.concatVoices(mode)[i].dropna()
                        curr_ngram = pd.Series(nltk.ngrams(temp,n, pad_right=True, pad_left=True, left_pad_symbol="<s>", right_pad_symbol="</s>"))
                        if stack is True:
                                new = pd.concat([new, curr_ngram], axis=0)
                        else:
                                new = pd.concat([new, curr_ngram], axis=1)
                if stack is True:
                        new = list(new[new.columns[0]].values)
                else:
                        new.columns = names

                return new


def getSection(file, part, start, end):
        measures = list()
        x = converter.parse(file).stripTies()
        data = x.recurse().getElementsByClass(['Part','Note', 'Chord', 'Rest'])

        music = False
        active_rest = False
        counter = 0
        
        for i in data.parts[part-1].recurse().getElementsByClass(['Note','Rest','Chord']):

                if isinstance(i, note.Rest) and music is False:
                        continue

                elif isinstance(i, note.Note):
                        music = True
                        active_rest = False
                        counter += 1


                elif isinstance(i, chord.Chord):
                        music = True
                        active_rest = False
                        counter += 1

                elif isinstance(i, note.Rest):
                        music = True

                        if active_rest is False:
                                active_rest = True
                                counter += 1
                        else:
                                continue

                else:pass

                if counter-1 < start:
                        
                        continue

                elif counter-1 == start:
                        i.style.color = 'red'
                        measures.append(i.measureNumber)

                elif counter-1 == end:
                        i.style.color = 'red'
                        measures.append(i.measureNumber)

                elif counter > end:
                        return measures, x.measures(measures[0], measures[1]), start, end
                        
                else:
                        i.style.color = 'red'

        return measures, x.measures(measures[0], measures[1]), start, end

def getPatternOcurrences(file, part, indexes):
        measures = list()
        st = converter.parse(file).stripTies()
        data = st.recurse().getElementsByClass(['Part','Note', 'Chord', 'Rest'])

        music = False
        active_rest = False
        counter = 0

        for x in indexes:
                start = x[0]
                end = x[-1]+1
        
                for i in data.parts[part-1].recurse().getElementsByClass(['Note','Rest','Chord']):

                        if isinstance(i, note.Rest) and music is False:
                                continue

                        elif isinstance(i, note.Note):
                                music = True
                                active_rest = False
                                counter += 1


                        elif isinstance(i, chord.Chord):
                                music = True
                                active_rest = False
                                counter += 1

                        elif isinstance(i, note.Rest):
                                music = True

                                if active_rest is False:
                                        active_rest = True
                                        counter += 1
                                else:
                                        continue

                        else:pass

                        if counter-1 < start:
                                continue

                        elif counter-1 >= start and counter-1 <= end:
                                i.style.color = 'red'
                                
                        else:
                                music = False
                                active_rest = False
                                counter = 0
                                break
                        
        return st 

def getConsecutive(pattern, seq, comp, wildcards, base40, mode, stack, voice_selec):
    ## validar patrón
    if wildcards == 'Wildcards':
        wildcards = True
    else:wildcards = False
    
    data = corpora_parser(4, [[seq],'All',[comp],''], 
                         ['']*4, base40=base40, stack=stack, mode=mode, voice_selec=1)[1][0]
    dct = dict()
    
    if len(pattern.split()) == 1:
        temp = [i for i in range(len(data)) if data[i] == pattern]
        
    for e in pattern.split():
        
        temp = [i for i in range(len(data)) if data[i] == e]
        dct[e] = temp
        
    indexes = list()
    
    if len(pattern.split()) == 1:
        
        return 'The program requires 2-item patterns at least'
    
    else:
        values = list(dct.values())
        for i in product(*values):
            condition = None
            for n, x in enumerate(i):

                if condition is False:
                    break
                
                if n < len(i)-1:
                    pass
                
                else:break
            
                if i[n+1] == x+1:
                    condition = True
                
                else:
                    if wildcards is True:
                        if i[n+1] == x+2:
                            condition = True
                        
                        else:
                            condition = False
                            break
                        
                    else:
                        condition = False
                        break
                    
            if condition is False:
                pass
            else:
                indexes.append(list(i))
                
    if len(indexes) == 0:
        return 'Pattern not found'
    else:
        print(f'{len(indexes)} ocurrences found.')
        print(indexes)
        out = getPatternOcurrences(f"{os.environ['MUSIC_FOLDER']}/{comp}/{seq}", 1, indexes)
        return out
