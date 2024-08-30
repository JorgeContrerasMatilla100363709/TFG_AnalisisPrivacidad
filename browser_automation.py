# browser_automation.py
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

def configure_browser(browser_name, config):
    if browser_name == "chrome" or browser_name == "brave":
        options = webdriver.ChromeOptions()
        options.binary_location = config["binary_location"]
        driver = webdriver.Chrome(service=ChromeService(config["driver_path"]), options=options)
    elif browser_name == "firefox" or browser_name == "tor":
        options = webdriver.FirefoxOptions()
        options.binary_location = config["binary_location"]
        driver = webdriver.Firefox(service=FirefoxService(config["driver_path"]), options=options)
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        options.binary_location = config["binary_location"]
        driver = webdriver.Edge(service=EdgeService(config["driver_path"]), options=options)
    else:
        raise ValueError("Unsupported browser: " + browser_name)
    return driver

def analyze_url(driver, url):
    driver.get(url)
    time.sleep(5)

    cookies = driver.get_cookies()
    headers = driver.execute_script("""
        var req = new XMLHttpRequest();
        req.open('GET', document.location, false);
        req.send(null);
        var headers = req.getAllResponseHeaders().toLowerCase();
        return headers;
    """)

    # Obtener el contenido HTML de la página
    page_source = driver.page_source

    # Usar BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(page_source, 'lxml')

    # Ejemplo: Encontrar todos los enlaces en la página
    links = [a['href'] for a in soup.find_all('a', href=True)]

    ads = driver.execute_script("""
        return [...document.querySelectorAll('script')].map(script => script.src).filter(src => src.includes('ad') || src.includes('track'));
    """)

    performance = driver.execute_script("""
        let performance = window.performance || window.webkitPerformance || window.mozPerformance || window.msPerformance;
        let timings = performance.getEntriesByType('navigation')[0];
        return {
            "navigationStart": timings.navigationStart,
            "unloadEventStart": timings.unloadEventStart,
            "unloadEventEnd": timings.unloadEventEnd,
            "redirectStart": timings.redirectStart,
            "redirectEnd": timings.redirectEnd,
            "fetchStart": timings.fetchStart,
            "domainLookupStart": timings.domainLookupStart,
            "domainLookupEnd": timings.domainLookupEnd,
            "connectStart": timings.connectStart,
            "connectEnd": timings.connectEnd,
            "secureConnectionStart": timings.secureConnectionStart,
            "requestStart": timings.requestStart,
            "responseStart": timings.responseStart,
            "responseEnd": timings.responseEnd,
            "domLoading": timings.domLoading,
            "domInteractive": timings.domInteractive,
            "domContentLoadedEventStart": timings.domContentLoadedEventStart,
            "domContentLoadedEventEnd": timings.domContentLoadedEventEnd,
            "domComplete": timings.domComplete,
            "loadEventStart": timings.loadEventStart,
            "loadEventEnd": timings.loadEventEnd
        };
    """)

    possible_ads = driver.execute_script("""
        return [...document.querySelectorAll('iframe, img, div')].filter(element => {
            let src = element.src || element.style.backgroundImage || '';
            return src.includes('ad') || src.includes('track') || src.includes('banner') || src.includes('pop');
        }).map(element => element.outerHTML);
    """)

    return {
        "url": url,
        "cookies": cookies,
        "headers": headers,
        "links": links,  # Nuevos datos obtenidos con BeautifulSoup
        "ads": ads,
        "performance": performance,
        "possible_ads": possible_ads
    }
def run_analysis(browser_name, config, urls):
    results = []
    driver = configure_browser(browser_name, config)
    for url in urls:
        try:
            result = analyze_url(driver, url)
            results.append(result)
            print(f"Análisis completado para {url}")
        except Exception as e:
            print(f"Error al analizar {url}: {e}")
    driver.quit()
    return results

