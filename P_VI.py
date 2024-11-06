import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import levene, ttest_ind

companies_df = pd.read_csv('./project_sql_result_01.csv')
dropoff_df = pd.read_csv('./project_sql_result_04.csv')
consulta_df = pd.read_csv('./project_sql_result_07.csv')

print('A continuacion haremos un análisis exploratorio de los datos proporcionados, revisaremos si los datos están en un formato correcto, si hay valores nulos o repetidos, mediante gráficos expresaremos los datos que estos dataframes contienen para ver su comportamiento y tendencia y así tener una idea clara su contenido para pdoer tomar decisiones. Se examinaron las 10 empresas con mas viajes, para su analisis mediante gráficos que nos representen una mejor visualizacion de las interacciones entre ellos. También corroboraremos la diferencia de promedios en tiempos de viaje con diferentes condicdiones climáticas, para ver en cuanto cambia el tiempo dependiendo la condicion.')
print()

print(companies_df.head())
print()

print(dropoff_df.head())
print()

print(companies_df.info())
print()

print(dropoff_df.info())
print()

print(companies_df.describe())
print()

print(dropoff_df.describe())
print()

duplicados_companies = companies_df.duplicated().sum()
print(f'Filas duplicadas : {duplicados_companies}')
print()

duplicados_dropoff = dropoff_df.duplicated().sum()
print(f'Filas duplicadas : {duplicados_dropoff}')
print()

nulos_companies = companies_df.isna().sum()
print(f'Valores nulos : \n{nulos_companies}')
print()

nulos_dropoff = dropoff_df.isna().sum()
print(f'Valores nulos : \n{nulos_dropoff}')
print()

print('Despues de este analisis podemos observar que no hay valores nulos ni repetidos en ambos dataframes, por lo que no será necesario remplazar ni modificar nada de las tablas.')
print()

location_name_10 = dropoff_df.nlargest(10, ['average_trips'])
print(location_name_10)
print()

sns.set_theme(rc = {'figure.figsize':(15,10)})
sns.barplot(
data = companies_df.nlargest(10,['trips_amount']),
x = 'company_name',
y = 'trips_amount',
)
plt.title('Viajes por compañia')
plt.xlabel('Compañias')
plt.ylabel('Cantidad de viajes')
plt.xticks(rotation = 90)
plt.show()

print('Podemos observar que casi la mitad de las compañias que están dentro de este estudio tienen una cantidad de viajes muy baja, podríamos decir que son menores a 500. A diferencia de la compañia Flash Cab que tiene un estimado de viajes de casi 20,000')
print()

sns.set_theme(rc = {'figure.figsize':(15,10)})
sns.barplot(
data = location_name_10,
x = 'dropoff_location_name',
y = 'average_trips',
)
plt.title('Promedio por Barrios')
plt.xlabel('Barrios')
plt.ylabel('Viajes')
plt.xticks(rotation = 90)
plt.show()

print('El barrio en donde se tienen mas viajes es Loop con mas de 10000 de promedio, los ultimos 6 tienen menos de la mitad que los 4 primeros.')
print()

print(consulta_df.head())
print()

print(consulta_df.info())
print()

nulos_consulta = consulta_df.isna().sum()
print(f'Valores nulos : \n{nulos_consulta}')
print()

consulta_df.rename(columns={'duration_seconds' : 'duration_minutes'}, inplace = True)
consulta_df['duration_minutes'] = consulta_df['duration_minutes'] / 60
print(consulta_df.head())
print()

consulta_df['start_ts'] = pd.to_datetime(consulta_df['start_ts'])
consulta_df['day_of_week'] = consulta_df['start_ts'].dt.dayofweek
consulta_df['is_rainy'] = consulta_df['weather_conditions'].str.contains('Bad')
print(consulta_df.info())
print()

print(consulta_df.head())
print()

saturdays_bad = consulta_df[(consulta_df['day_of_week'] == 5) & (consulta_df['weather_conditions'] == 'Bad')]
print(saturdays_bad)
print()

avg_duration_bad = saturdays_bad['duration_minutes'].mean()
print(f'La duración media de viajes los días sábados y con malas condiciones es : {avg_duration_bad}')
print()

saturdays_good = consulta_df[(consulta_df['day_of_week'] == 5) & (consulta_df['weather_conditions'] == 'Good')]
avg_sabados = saturdays_good['duration_minutes'].mean()
print(f'La duración media de viajes los días sábados con distintas condiciones es: {avg_sabados}')
print()

print('De estos dos analisis podemos observar que en efecto los días sábados con malas condiciones aumenta la media en tiempo de viajes a diferencia de un sábado con condiciones buenas o malas')
print()

t_stat, p_value = stats.ttest_ind(saturdays_bad['duration_minutes'], saturdays_good['duration_minutes'], equal_var = False)

alpha = 0.5
print(f'Estadistico t: {t_stat}, p-value: {p_value}')
print()

if p_value < alpha:
    print("Rechazamos la hipótesis nula: Hay evidencia de que la duración promedio de los viajes cambia bajo condiciones de sábados con mal condicion climática")
else:
    print("No rechazamos la hoipótesis nula: No hay evidencia suficiente par afirmar que la duración promedio de los viajes cambia los sábados con mal condicion climática")
print()

saturdays= consulta_df[consulta_df['day_of_week'] == 5]
rainy_variance = saturdays_bad['duration_minutes'].var()
no_rainy_variance = saturdays_good['duration_minutes'].var()

levene_stat, levene_p = levene(saturdays_bad['duration_minutes'], saturdays_good['duration_minutes'])
print(f"Levene's test statistic: {levene_stat}, p-value: {levene_p}")
print()

equal_var = levene_p > 0.05

t_stat, p_val = ttest_ind(
    saturdays_bad['duration_minutes'],
    saturdays_good['duration_minutes'],
    equal_var=equal_var
)

print(f"T-test statistic: {t_stat}, p-value: {p_val}")
print()

alpha = 0.05
if p_val < alpha:
    print("Rechazamos la hipótesis nula. La duración promedio de los viajes cambia los sábados lluviosos.")
else:
    print("No podemos rechazar la hipótesis nula. La duración promedio de los viajes no cambia los sábados lluviosos.")
print()

print('Mediante el analisis realizado obteniendo las varianzas, pudimos comprobar que en efecto hay un cambio de tiempo promedio en recorrido del viaje cuando las condiciones climaticas no son favorables, esto nos ayudará a identificar y tomar decisiones en cuanto a precios bajo esas condiciones, para contrarretrar el tiempo aumentado.')
print()

