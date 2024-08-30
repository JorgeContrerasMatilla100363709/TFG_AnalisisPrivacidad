import yaml
import pandas as pd
import matplotlib.pyplot as plt

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

# Análisis de encabezados de seguridad
security_headers = ['strict-transport-security', 'content-security-policy', 'x-frame-options', 'x-content-type-options']

for header in security_headers:
    df_all[header] = df_all['headers'].apply(lambda x: header in x.lower())

# Calcular el porcentaje de páginas que tienen cada encabezado de seguridad
security_headers_count = df_all.groupby('browser')[security_headers].mean() * 100

# Mostrar los resultados numéricos en la terminal
for header in security_headers:
    header_presence = df_all.groupby('browser')[header].mean() * 100
    print(f"\nPorcentaje de Páginas con {header.replace('-', ' ').title()} por Navegador:")
    print(header_presence)

# Gráfico de barras apiladas con diferentes colores para cada encabezado
security_headers_count.plot(kind='bar', color=['blue', 'green', 'orange', 'red'], figsize=(10, 6))
plt.title('Análisis de Encabezados de Seguridad por Navegador')
plt.xlabel('Navegador')
plt.ylabel('Porcentaje de Páginas con Encabezado de Seguridad')
plt.legend(title='Encabezados de Seguridad')
plt.show()
