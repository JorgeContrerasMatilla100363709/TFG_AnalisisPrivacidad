# run_brave_analysis.py
from config import BROWSERS, URLS, save_results_to_yaml
from browser_automation import run_analysis

browser_name = "brave"
results = run_analysis(browser_name, BROWSERS[browser_name], URLS)
save_results_to_yaml(results, f'results_{browser_name}.yaml')