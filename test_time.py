import time
import requests
import logging

# Sidor for testning
web_generator_url = "http://127.0.0.1:5000/web_generator"
file_query_url = "http://127.0.0.1:5000/file_query"

# Sample data for requests
generate_page_data = {
    "page_name": "test_page",
    "page_description": "",
    "template_choice": "corporate"
}

query_list_files_data = {
    "query": "list my files",
    "read_files_toggle": "on"
}

query_summarize_files_data = {
    "query": "summarize my files",
    "read_files_toggle": "on"
}

def benchmark_endpoint(endpoint, data=None):
    start_time = time.time()
    if data:
        response = requests.post(endpoint, data=data)
    else:
        response = requests.get(endpoint)
    elapsed_time = time.time() - start_time
    return response.status_code, elapsed_time

def main():
    logging.basicConfig(level=logging.INFO)
    
    endpoints = [
        (web_generator_url, generate_page_data, "Generate a new web page"),
        (file_query_url, query_list_files_data, "Query list my files"),
        (file_query_url, query_summarize_files_data, "Query summarize my files"),
    ]
    
    for endpoint, data, description in endpoints:
        logging.info(f"Running benchmark for: {description}")
        try:
            status_code, elapsed_time = benchmark_endpoint(endpoint, data)
            logging.info(f"{description} took {elapsed_time:.4f} seconds with status code {status_code}")
        except Exception as e:
            logging.error(f"Error during {description}: {e}")

if __name__ == "__main__":
    main()
