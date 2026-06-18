import matplotlib.pyplot as plt
import numpy as np

def plt_individuals(grupo2, grupo1, pp):

	## Diagrama de dispersión para visualizar la perplejidad por archivo con su desviación standard
	# grupo 1 (principal) vs grupo 2 en la prueba
	plt.figure(figsize=(10, 6))
	plt.scatter(grupo2 + grupo1, pp, marker='o', s=100, alpha=0.5)
	plt.grid(axis = 'y')
	plt.xlabel('Data points')
	plt.ylabel('Perplexity')
	plt.title('Perplexity Scatter Plot')
	plt.xticks(np.arange(len(grupo2 + grupo1)), grupo2 + grupo1, rotation=90)
	plt.tight_layout()
	
	return plt

def plt_individuals_colored(grupo2_files, grupo1_files, pp):

	## Diagrama de dispersión para visualizar la perplejidad por archivo con su desviación standard
	# grupo 1 vs grupo 2 en la prueba. Similaridad entre los diferentes autores.
	autores = grupo2_files + grupo1_files

	# Crear un diccionario para almacenar la posición central x y color de cada autor
	autor_info = {autor: {'posiciones': [], 'color': None} for autor in set(autores)}

	# Crear la figura y los ejes
	fig, ax = plt.subplots(figsize=(15, 10))
	plt.grid(axis='y', linestyle='--', alpha=0.7)

	# Iterar sobre los datos y agregar puntos al scatter plot
	for i, (longitud, autor) in enumerate(zip(pp, autores)):
	    # Obtener la posición central x para el autor
	    if not autor_info[autor]['posiciones']:
	        autor_info[autor]['posiciones'] = [i]
	        autor_info[autor]['color'] = np.random.rand(3,)
	    else:
	        autor_info[autor]['posiciones'].append(i)

	    # Agregar el punto al scatter plot
	    ax.scatter(i, longitud, c=[autor_info[autor]['color']], label=autor, s=50)

	# Calcular y ajustar la posición central para cada autor
	for autor, info in autor_info.items():
	    x_central = np.mean(info['posiciones'])
	    ax.text(x_central, 0, autor, ha='center', va='center', backgroundcolor='white', color=info['color'], bbox=dict(facecolor='white', edgecolor='white'), rotation=90)

	# Configurar el título y las etiquetas de los ejes
	plt.title("Perplejidades por autor")
	plt.ylabel("Perplejidad")


	# Ocultar los números en el eje x y mostrar solo los nombres de los autores
	ax.set_xticks([])
	ax.set_xticklabels([])

	return plt

def plt_folded(grupo2_files, grupo1_files, pp, t_files, pp_test):

	autores = grupo2_files + grupo1_files

	# Crear un diccionario para almacenar las estadísticas de longitud de cada autor
	estadisticas_autores = {autor: {'max': None, 'min': None, 'media': None, 'desviacion': None, 'color': None, 'perplejidades': []} for autor in set(autores)}

	# Calcular estadísticas para cada autor
	for autor in estadisticas_autores:
	    pp_autor = [p for p, a in zip(pp, autores) if a == autor]
	    estadisticas_autores[autor]['max'] = np.max(pp_autor)
	    estadisticas_autores[autor]['min'] = np.min(pp_autor)
	    estadisticas_autores[autor]['media'] = np.mean(pp_autor)
	    estadisticas_autores[autor]['desviacion'] = np.std(pp_autor)
	    estadisticas_autores[autor]['color'] = np.random.rand(3,)
	    estadisticas_autores[autor]['perplejidades'] = pp_autor
	# Configurar el gráfico
	fig, ax = plt.subplots(figsize=(15,10))
	ax.grid(axis='y')

	# Representar las estadísticas de longitud para cada autor
	for i, autor in enumerate(estadisticas_autores):
	    rango = estadisticas_autores[autor]['max'] - estadisticas_autores[autor]['min']
	    media = estadisticas_autores[autor]['media']
	    desviacion = estadisticas_autores[autor]['desviacion']
	    color = estadisticas_autores[autor]['color']
	    pp_autor = estadisticas_autores[autor]['perplejidades']

	    # Barras verticales para representar el rango de longitudes de cada autor
	    ax.bar(x=i, height=rango, bottom=estadisticas_autores[autor]['min'], width=0.3, color=color, alpha=0.3, label=f'Rango {autor}')

	    # Puntos y líneas horizontales para representar la media y desviación estándar de las longitudes de cada autor
	    offset = 0.05  # Ajuste de posición para evitar solapamientos
	    posiciones_x = np.linspace(i - offset, i + offset, len(pp_autor))
	    ax.scatter(posiciones_x, pp_autor, color=color, marker='o', label=f'Longitudes {autor}')
	    ax.hlines(y=media, xmin=i - 0.25, xmax=i + 0.25, color=color, label=f'Media {autor}')
	    ax.hlines(y=media + desviacion, xmin=i - 0.25, xmax=i + 0.25, color=color, linestyle='--', label=f'Desviación {autor}')
	    ax.hlines(y=media - desviacion, xmin=i - 0.25, xmax=i + 0.25, color=color, linestyle='--')

	# Representar la nueva serie de perplejidades como puntos
	offset_nueva_serie = len(estadisticas_autores) + 0.2
	posiciones_x_nueva_serie = np.arange(len(pp_test)) + offset_nueva_serie
	scatter_nueva_serie = ax.scatter(posiciones_x_nueva_serie, pp_test, color='red', marker='o')


	# Etiquetas y leyendas
	ax.set_xticks(range(len(estadisticas_autores) + len(pp_test)))  # Ajustar el número de ticks
	ax.set_xticklabels(list(estadisticas_autores.keys()) + t_files, rotation=90)

	# Configurar el límite del eje x para ampliar el gráfico hacia la derecha
	ax.set_xlim(-0.5, len(estadisticas_autores) + len(pp_test) - 0.5)

	legend = ax.legend(['Perplejidades Individuales', 'Media', 'Desviación Típica'],
	loc='upper left', bbox_to_anchor=(1, 1))   
	# Trazar líneas desde los nuevos puntos hasta el eje y
	for x, y in zip(posiciones_x_nueva_serie, pp_test):
	    ax.hlines(y, 0, x, colors='red', linestyles='--', linewidth=0.8)

	ax.set_ylabel('Perplejidades')

	return plt


def plt_folded_sliding_window(dict1, dict2, dict3, window_size,  files_test, name1=str(), name2=str()):

	pp_1 = dict1[window_size]
	pp_2 = dict2[window_size]
	pp_3 = dict3[window_size]  ## tratamiento especial

	tags = [name1] + [name2] + files_test

	category_stats_dict = {tag: {'max': None, 'min': None, 'media': None, 'desviacion': None, 'color': None, 'perplejidades': []} for tag in set(tags)}
	
	for tag in category_stats_dict:

		if tag == name1:
			category_stats_dict[tag]['max'] = np.max(pp_1)
			category_stats_dict[tag]['min'] = np.min(pp_1)
			category_stats_dict[tag]['media'] = np.mean(pp_1)
			category_stats_dict[tag]['desviacion'] = np.std(pp_1)
			category_stats_dict[tag]['color'] = np.random.rand(3,)
			category_stats_dict[tag]['perplejidades'] = pp_1

		elif tag == name2:
			category_stats_dict[tag]['max'] = np.max(pp_2)
			category_stats_dict[tag]['min'] = np.min(pp_2)
			category_stats_dict[tag]['media'] = np.mean(pp_2)
			category_stats_dict[tag]['desviacion'] = np.std(pp_2)
			category_stats_dict[tag]['color'] = np.random.rand(3,)
			category_stats_dict[tag]['perplejidades'] = pp_2

		else:
			work_idx = files_test.index(tag)
			category_stats_dict[tag]['max'] = np.max(pp_3[work_idx])
			category_stats_dict[tag]['min'] = np.min(pp_3[work_idx])
			category_stats_dict[tag]['media'] = np.mean(pp_3[work_idx])
			category_stats_dict[tag]['desviacion'] = np.std(pp_3[work_idx])
			category_stats_dict[tag]['color'] = np.random.rand(3,)
			category_stats_dict[tag]['perplejidades'] = pp_3[work_idx]
	    
	# Configurar el gráfico
	fig, ax = plt.subplots(figsize=(15,10))
	ax.grid(axis='y')

	for n, tag in enumerate(category_stats_dict):
	    rango = category_stats_dict[tag]['max'] - category_stats_dict[tag]['min']
	    media = category_stats_dict[tag]['media']
	    desviacion = category_stats_dict[tag]['desviacion']
	    color = category_stats_dict[tag]['color']
	    pp_autor = category_stats_dict[tag]['perplejidades']

	    # Barras verticales para representar el rango de longitudes de cada autor
	    ax.bar(x=n, height=rango, bottom=category_stats_dict[tag]['min'], width=0.3, color=color, alpha=0.3, label=f'Rango {tag}')

	    # Puntos y líneas horizontales para representar la media y desviación estándar de las longitudes de cada autor
	    offset = 0.05  # Ajuste de posición para evitar solapamientos
	    posiciones_x = np.linspace(n - offset, n + offset, len(pp_autor))
	    ax.scatter(posiciones_x, pp_autor, color=color, marker='o', label=f'Longitudes {tag}')
	    ax.hlines(y=media, xmin=n - 0.25, xmax=n + 0.25, color=color, label=f'Media {tag}')
	    ax.hlines(y=media + desviacion, xmin=n - 0.25, xmax=n + 0.25, color=color, linestyle='--', label=f'Desviación {tag}')
	    ax.hlines(y=media - desviacion, xmin=n - 0.25, xmax=n + 0.25, color=color, linestyle='--')

	similarity_threshold = category_stats_dict[name1]['media'] - category_stats_dict[name1]['desviacion']

	plt.axhline(y=similarity_threshold, color='red', linestyle='--', linewidth=2) ## umbral de similaridad


	# Etiquetas y leyendas
	ax.set_xticks(range(len(category_stats_dict)))  # Ajustar el número de ticks
	ax.set_xticklabels(list(category_stats_dict.keys()), rotation=90)

	# Configurar el límite del eje x para ampliar el gráfico hacia la derecha
	ax.set_xlim(-0.5, len(category_stats_dict) - 0.5)

	legend = ax.legend(['Perplejidades Individuales', 'Media', 'Desviación Típica'],
	loc='upper left', bbox_to_anchor=(1, 1))   
	
	ax.set_ylabel('Perplejidades')

	return plt


def plt_by_classes(max1, max2, min1, min2, dev1, dev2, med1, med2, pp1, pp2):

	fig, ax = plt.subplots()
	ax.grid(axis = 'y')
	# Agrega barras verticales para representar el rango de perplejidades de la Clase 1
	ax.bar(x=0, height=max1 - min1, bottom=min1, width=0.3, color='lightblue', alpha=0.3, label='Rango Morales')

	# Agrega puntos y líneas horizontales para representar la media y desviación estándar de las perplejidades de la Clase 1
	ax.scatter([0]*len(pp1), pp1, color='blue', marker='o', label='Perplejidades Morales')
	ax.hlines(y=med1, xmin=-0.25, xmax=0.25, color='blue', label='Media Clase 1')
	ax.hlines(y=med1 + dev1, xmin=-0.25, xmax=0.25, color='blue', linestyle='--', label='Desviación Estándar Morales')
	ax.hlines(y=med1 - dev1, xmin=-0.25, xmax=0.25, color='blue', linestyle='--')

	# Agrega barras verticales para representar el rango de perplejidades de la Clase 2
	ax.bar(x=1, height=max2 - min2, bottom=min2, width=0.3, color='lightsalmon', alpha=0.3, label='Rango Otros')

	# Agrega puntos y líneas horizontales para representar la media y desviación estándar de las perplejidades de la Clase 2
	ax.scatter([1]*len(pp2), pp2, color='orange', marker='o', label='Perplejidades Clase 2')
	ax.hlines(y=med2, xmin=0.75, xmax=1.25, color='orange', label='Media Otros')
	ax.hlines(y=med2 + dev2, xmin=0.75, xmax=1.25, color='orange', linestyle='--', label='Desviación Otros')
	ax.hlines(y=med2 - dev2, xmin=0.75, xmax=1.25, color='orange', linestyle='--')

	# Etiquetas y leyendas
	ax.set_xticks([0,1])
	ax.set_xticklabels(['Perplexity Morales', 'Perplexity Otros'])
	ax.set_ylabel('Perplejidad')

	# Coloca la leyenda fuera del gráfico
	ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

	return plt


def progresion(pp, files, archivo, stdev_otros):
	
	_, idx = np.unique(files, return_index=True)
	arr_sin_duplicados = files[np.sort(idx)]
	f_idx = np.where(arr_sin_duplicados == archivo)[0][0]
	n_points = len(pp[f_idx])
	y = pp[f_idx]

	plt.plot(range(0, n_points), y, label=f'Evolución de perplejidades en\n {archivo}', color='blue')

	plt.axhline(y=stdev_otros, color='red', linestyle='--', label=f'Umbral mínimo de similaridad con Morales')

	plt.xlabel('X (posición de la sliding window)')
	plt.ylabel('Y (medidas de perplejidad)')
	plt.suptitle(f'Evolución de las predicciones a lo largo de sliding windows de longitud 324')
	plt.title(archivo)


	plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
	return plt
