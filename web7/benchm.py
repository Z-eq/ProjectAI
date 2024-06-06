import time
import logging
import os
from utils import query_openai_gpt, initialize_db, save_version, get_versions, get_version_by_id
from file_indexer import index_files, get_indexed_files, get_file_content

logging.basicConfig(level=logging.INFO)

# Mappa över funktioner och deras beskrivningar för benchmark
benchmark_tests = {
    "query_openai_gpt": {
        "function": query_openai_gpt,
        "description": "Query OpenAI GPT",
        "params": ["What is the capital of France?"]
    },
    "initialize_db": {
        "function": initialize_db,
        "description": "Initialize the database",
        "params": []
    },
    "save_version": {
        "function": save_version,
        "description": "Save a version of a generated webpage",
        "params": ["test_page", "<html>Test content</html>"]
    },
    "get_versions": {
        "function": get_versions,
        "description": "Get all versions of generated webpages",
        "params": []
    },
    "get_version_by_id": {
        "function": get_version_by_id,
        "description": "Get content of a specific version of a generated webpage",
        "params": [1]
    },
    "index_files": {
        "function": index_files,
        "description": "Index files in a directory",
        "params": [r'C:\Users\Z\Documents\Skol-Material\Lektioner\Filer']
    },
    "get_indexed_files": {
        "function": get_indexed_files,
        "description": "Get all indexed files",
        "params": []
    },
    "get_file_content": {
        "function": get_file_content,
        "description": "Get content of a specific file",
        "params": [r'C:\Users\Z\Documents\Skol-Material\Lektioner\Filer\somefile.txt']
    }
}

def run_benchmark():
    for test_name, test_info in benchmark_tests.items():
        logging.info(f"Running benchmark for: {test_info['description']}")
        start_time = time.time()
        try:
            result = test_info['function'](*test_info['params'])
            logging.info(f"Result: {result}")
        except Exception as e:
            logging.error(f"Error during {test_info['description']}: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"{test_info['description']} took {elapsed_time:.4f} seconds\n")

if __name__ == "__main__":
    run_benchmark()
