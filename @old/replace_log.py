import os
import csv
import re
import logging
import tkinter as tk
from tkinter import filedialog

def find_AP_files(directory):
    AP_files = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if "AP" in file_name and file_name.endswith(".log"):
                file_path = os.path.join(root, file_name)
                AP_files.append(file_path)
    return AP_files

def read_replacement_patterns(csv_file):
    patterns = []
    try:
        with open(csv_file, 'r', encoding='utf-8', errors='ignore', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    search_text = row[0].replace('\\n', '\n')  # 改行を正しく処理
                    replacement_text = row[1].replace('\\n', '\n') if row[1].strip() else ""
                    patterns.append((search_text, replacement_text))
        logging.info("Loaded patterns:")
        for pattern in patterns:
            logging.info(f"Search: '{pattern[0]}' | Replace: '{pattern[1]}'")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
    return patterns

def replace_multiline_text_in_file(file_path, patterns):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        logging.error(f"Error reading log file: {e}")
        return

    new_content = content
    total_replacements = 0
    for search_text, replacement_text in patterns:
        escaped_search_text = re.escape(search_text)  # 正規表現用にエスケープ
        new_content, num_replacements = re.subn(escaped_search_text, replacement_text, new_content, flags=re.DOTALL)
        if num_replacements > 0:
            total_replacements += num_replacements
            logging.info(f"Pattern found and replaced: '{search_text}' -> '{replacement_text}' in {file_path}")

    if total_replacements > 0:
        try:
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                file.write(new_content)
            logging.info(f"Total replacements in {file_path}: {total_replacements}")
        except Exception as e:
            logging.error(f"Error writing log file: {e}")
    else:
        logging.info(f"No patterns found in {file_path}")

def process_files_in_directory(directory, patterns):
    AP_files = find_AP_files(directory)
    for file_path in AP_files:
        replace_multiline_text_in_file(file_path, patterns)

def select_directory(initial_dir):
    root = tk.Tk()
    root.withdraw()  # Close the root window
    directory = filedialog.askdirectory(initialdir=initial_dir)
    return directory

def select_csv_file(initial_dir):
    root = tk.Tk()
    root.withdraw()  # Close the root window
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("CSV files", "*.csv")])
    return file_path

if __name__ == "__main__":
    # Set up logging to file with append mode
    logging.basicConfig(filename='log_replacement.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

    # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Select the directory and CSV file using a dialog
    directory = select_directory(script_dir).strip('"')
    csv_file = select_csv_file(script_dir).strip('"')

    # Read replacement patterns from the CSV file
    patterns = read_replacement_patterns(csv_file)

    # Process files in the selected directory
    process_files_in_directory(directory, patterns)
