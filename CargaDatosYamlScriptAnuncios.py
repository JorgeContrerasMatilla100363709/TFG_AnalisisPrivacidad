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

# Análisis de anuncios

# Contar número de scripts relacionados con anuncios por navegador
ads_count = df_all.groupby('browser')['ads'].apply(lambda x: x.str.len().sum())

# Imprimir resultados en la terminal
print("Número de Scripts de Anuncios por Navegador:")
print(ads_count)

# Gráfico de barras
ads_count.plot(kind='bar', color=['blue'])
plt.title('Número de Scripts de Anuncios por Navegador')
plt.xlabel('Navegador')
plt.ylabel('Cantidad de Scripts de Anuncios')
plt.show()

