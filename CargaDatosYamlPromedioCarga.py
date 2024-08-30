import yaml
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Cargar archivos YAML
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Cargar datos de varios navegadores
data_chrome = load_yaml('results_chrome.yaml')
data_edge = load_yaml('results_edge.yaml')
data_brave = load_yaml('results_brave.yaml')
data_firefox = load_yaml('results_firefox.yaml')

# Convertir en DataFrames
df_chrome = pd.json_normalize(data_chrome)
df_edge = pd.json_normalize(data_edge)
df_brave = pd.json_normalize(data_brave)
df_firefox = pd.json_normalize(data_firefox)

# Añadir una columna para identificar el navegador
df_chrome['browser'] = 'Chrome'
df_edge['browser'] = 'Edge'
df_brave['browser'] = 'Brave'
df_firefox['browser'] = 'Firefox'

# Concatenar todos los DataFrames
df_all = pd.concat([df_chrome, df_edge, df_brave, df_firefox], ignore_index=True)

# Análisis de rendimiento

# Promedio de tiempos de carga
performance_metrics = [ 'performance.loadEventEnd']
performance_df = df_all.groupby('browser')[performance_metrics].mean()

# Imprimir resultados en la terminal
print("Tiempos Promedio de Carga por Navegador (en ms):")
print(performance_df)

# Gráfico de líneas
performance_df.plot(kind='bar', color=['blue'])
plt.title('Tiempos Promedio de Carga por Navegador')
plt.xlabel('Navegador')
plt.ylabel('Tiempo en ms')
plt.show()

