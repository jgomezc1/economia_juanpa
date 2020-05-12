# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:52:09 2020

@author: AX201 GMRS
"""

import numpy as np
import pandas as pd
import geopandas as gpd


shapefile   = 'data/countries_110m/ne_110m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

countries = gdf.sort_values(by=['ADM0_A3'])
countries.columns = ['country', 'country_code', 'geometry']

datafile  = 'data/entrada.xls'
database  =  pd.read_excel(datafile)

rot_temp = database .columns.values.tolist()
ncol = len(rot_temp)
columnas = []
for i in range(2 , ncol):
    columnas.append(rot_temp[i])
timespan = ncol-2
ini_year = columnas[0]
ini_year = int(ini_year)

database  =  database.sort_values(by=['code'])
country_codes = countries['country_code']
database_codes = database['code']

df =database_codes.isin(country_codes)
filtered_database = database[df]
ncountries = len(filtered_database.index)

indices= np.zeros((ncountries) , dtype = int)
i = 0
for row in filtered_database.index:
    indices[i] = row
    i = i +1

df = country_codes.isin(database_codes)

filtered_countries = countries[df]
filtered_countries.set_index(indices , inplace=True)

years = filtered_database[columnas]

my_arreglo = years.to_numpy(copy = True)
new_array = my_arreglo.flatten()
new_series = pd.Series(new_array)

anio = np.zeros((timespan*ncountries), dtype = int)
for j in range(ncountries):
    y = ini_year
    k = j*timespan
    for i in range(timespan):
        anio[k] = y
        k = k + 1
        y = y + 1

new_anio = pd.Series(anio)
paises_names = filtered_database['entity']
paises_codes = filtered_database['code']
mis_paises = paises_names.array
mis_codes  = paises_codes.array

new_pais = []
new_code = []

for i in range(ncountries):
    pais = mis_paises[i]
    code = mis_codes[i]
    
    for j in range(timespan):
        new_pais.append(pais)
        new_code.append(code)

chimba = pd.DataFrame(list(zip(new_pais , new_code , new_anio , new_series)))
chimba.columns = ['country', 'country_code', 'year' , 'indicator']
chimba.to_csv('data/chimba.csv' , index=False)

llaves = []
values = []

max = 70.0
for i in range (ncol-2):
    serie = filtered_database[columnas[i]]
    i_max = serie.max()
    if i_max > max:
        max = i_max
print('Maximum value in the table=' , max)

























