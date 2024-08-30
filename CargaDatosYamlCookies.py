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
data_firefox = load_yaml('results_firefox.yaml')
data_edge = load_yaml('results_edge.yaml')
data_brave = load_yaml('results_brave.yaml')

# Convertir en DataFrames
df_chrome = pd.json_normalize(data_chrome)
df_firefox = pd.json_normalize(data_firefox)
df_edge = pd.json_normalize(data_edge)
df_brave = pd.json_normalize(data_brave)

# Añadir una columna para identificar el navegador
df_chrome['browser'] = 'Chrome'
df_firefox['browser'] = 'Firefox'
df_edge['browser'] = 'Edge'
df_brave['browser'] = 'Brave'

# Concatenar todos los DataFrames
df_all = pd.concat([df_chrome, df_edge, df_brave, df_firefox], ignore_index=True)


# Análisis detallado de Cookies
def analyze_cookies(cookies_list):
    secure_count = 0
    http_only_count = 0
    total_count = len(cookies_list)

    for cookie in cookies_list:
        if cookie.get('secure', False):
            secure_count += 1
        if cookie.get('httpOnly', False):
            http_only_count += 1

    return {
        "total": total_count,
        "secure": secure_count,
        "http_only": http_only_count,
    }


# Analizando cookies para cada navegador
df_cookies_analysis = pd.DataFrame(columns=["browser", "total", "secure", "http_only"])

for browser in df_all['browser'].unique():
    browser_cookies = df_all[df_all['browser'] == browser]['cookies'].sum()
    analysis = analyze_cookies(browser_cookies)
    analysis["browser"] = browser
    df_cookies_analysis = pd.concat([df_cookies_analysis, pd.DataFrame([analysis])], ignore_index=True)

# Mostrar la tabla de resultados en la terminal
print("Resultados del Análisis de Cookies por Navegador:")
print(df_cookies_analysis)

# Visualizando todas las categorías de cookies en la misma gráfica

# Gráfico de barras combinado para todas las categorías de cookies
df_cookies_analysis.set_index('browser')[["total", "secure", "http_only"]].plot(
    kind='bar',
    color=['blue', 'green', 'red'],
    figsize=(10, 6)
)
plt.title('Análisis de Cookies por Navegador')
plt.xlabel('Navegador')
plt.ylabel('Cantidad de Cookies')
plt.legend(['Total', 'Seguras', 'HTTP Only'])
plt.show()
