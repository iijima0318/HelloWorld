import os
import difflib
from tkinter import Tk, filedialog

# Function to select folder using a popup
def select_folder(prompt):
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=prompt)
    return folder_selected

# Function to read and preprocess the lines from the file
def read_and_preprocess_file(file_path, hostname):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='shift_jis') as file:
            lines = file.readlines()
    processed_lines = [
        line.strip() for line in lines if line.strip() and
        not line.strip().startswith('undo') and
        not line.strip().startswith('poe enable') and
        not line.strip().startswith(f'<{hostname}>') and
        not line.strip().startswith(f'[{hostname}]') and
        not ('password' in line or 'secret' in line) and
        not line.strip().startswith('snmp-agent community write') and
        not line.strip().startswith('snmp-agent local-engineid') and
        not line.strip().startswith('version') and
        not line.strip().startswith('snmp-agent trap enable') and
        not line.strip().startswith('undo snmp-agent trap enable') and
        not line.strip().startswith('#') and
        not line.strip().startswith('loopback-detection enable vlan 1 to 4094') and
        not line.strip().startswith('loopback-detection action shutdown')
    ]
    return processed_lines

# Function to check for specific interface settings
def check_interface_settings(lines):
    interface_check = {
        'GigabitEthernet1/0/25': 'combo enable fiber',
        'GigabitEthernet1/0/26': 'combo enable fiber',
        'GigabitEthernet1/0/27': 'combo enable fiber',
        'GigabitEthernet1/0/28': 'combo enable fiber',
    }
    for iface, setting in interface_check.items():
        iface_found = any(iface in line for line in lines)
        setting_found = any(setting in line for line in lines)
        if iface_found and not setting_found:
            print(f"Missing setting '{setting}' for interface '{iface}'")
            return False
    return True

# Function to write the result to the log file
def write_log(file_path, base_file, compare_file, log_message):
    mode = 'a' if os.path.exists(file_path) else 'w'
    with open(file_path, mode) as log_file:
        if mode == 'a':
            log_file.write('\n' + '-'*20 + '\n')
        log_file.write(f"Base File: {base_file}\n")
        if compare_file:
            log_file.write(f"Comparison File: {compare_file}\n")
        log_file.write(log_message + '\n')

# Function to find and validate the hostname in the files
def validate_hostname(base_lines, compare_lines, compare_file_name):
    base_hostname = None
    for line in base_lines:
        if line.strip().startswith('sysname'):
            base_hostname = line.split()[-1]
            break

    if base_hostname is None:
        print("Base hostname not found.")
        return None, False

    if base_hostname not in compare_file_name:
        print(f"Hostname {base_hostname} not found in file name {compare_file_name}.")
        return base_hostname, False

    compare_hostname = None
    for line in compare_lines:
        if line.strip().startswith('sysname'):
            compare_hostname = line.split()[-1].strip('[]')
            break

    if compare_hostname is None or compare_hostname != base_hostname:
        print(f"Hostname {compare_hostname} in comparison file does not match base hostname {base_hostname}.")
        return base_hostname, False

    return base_hostname, True

# Select folders for base and comparison files
base_folder = select_folder("Select the folder containing the base configuration files")
compare_folder = select_folder("Select the folder containing the comparison configuration files")

# Log file path
log_file_path = 'config_comparison_log.txt'

# Find all base files and process each one
for root, _, files in os.walk(base_folder):
    for file in files:
        if file.endswith(".txt"):
            base_file_path = os.path.join(root, file)
            
            # Read the base file to find the hostname
            try:
                with open(base_file_path, 'r', encoding='utf-8') as f:
                    base_lines_raw = f.readlines()
            except UnicodeDecodeError:
                try:
                    with open(base_file_path, 'r', encoding='shift_jis') as f:
                        base_lines_raw = f.readlines()
                except UnicodeDecodeError:
                    print(f"Encoding error in {base_file_path}. Skipping file.")
                    write_log(log_file_path, base_file_path, '', f"Encoding error in {base_file_path}.")
                    continue
            
            base_hostname = None
            for line in base_lines_raw:
                if line.strip().startswith('sysname'):
                    base_hostname = line.split()[-1]
                    break

            if base_hostname is None:
                print(f"Base hostname not found in {base_file_path}. Skipping file.")
                write_log(log_file_path, base_file_path, '', "Base hostname not found.")
                continue
            
            # Log the extracted hostname
            print(f"Extracted base hostname: {base_hostname}")
            write_log(log_file_path, base_file_path, '', f"Extracted base hostname: {base_hostname}")

            # Preprocess the lines with the hostname
            base_lines = read_and_preprocess_file(base_file_path, base_hostname)

            # Find the corresponding comparison file
            compare_file_path = None
            for comp_root, _, comp_files in os.walk(compare_folder):
                for compare_file in comp_files:
                    if '設定確認' in compare_file and base_hostname in compare_file:
                        compare_file_path = os.path.join(comp_root, compare_file)
                        break
                if compare_file_path:
                    break

            if compare_file_path is None:
                print(f"Comparison configuration file not found for {base_file_path}. Skipping file.")
                write_log(log_file_path, base_file_path, '', "Comparison configuration file not found.")
                continue

            try:
                compare_lines = read_and_preprocess_file(compare_file_path, base_hostname)
            except UnicodeDecodeError:
                print(f"Encoding error in {compare_file_path}. Skipping file.")
                write_log(log_file_path, base_file_path, compare_file_path, f"Encoding error in {compare_file_path}.")
                continue

            # Validate hostnames
            base_hostname, hostnames_match = validate_hostname(base_lines, compare_lines, compare_file_path)
            if not hostnames_match:
                write_log(log_file_path, base_file_path, compare_file_path, f"{base_hostname} - Hostname does not match.")
                continue

            write_log(log_file_path, base_file_path, compare_file_path, f"{base_hostname} - Hostname matches.")

            # Check specific interface settings
            interfaces_valid = check_interface_settings(compare_lines)

            # Define ignored differences
            ignored_diffs = [
                '-version', '+version', '-undo', '+poe enable', '+combo enable fiber', '-snmp-agent trap enable',
                '+snmp-agent local-engineid', '+snmp-agent community write cipher',
                '-loopback-detection enable vlan 1 to 4094', '-loopback-detection action shutdown'
            ]

            # Use difflib to compare the files
            diff = difflib.unified_diff(base_lines, compare_lines, lineterm='')

            # Output the differences
            diff_lines = list(diff)
            filtered_diff_lines = [
                line for line in diff_lines if not any(ignored in line for ignored in ignored_diffs)
            ]
            filtered_diff_lines = [
                line for line in filtered_diff_lines if line.startswith('-') or line.startswith('+')
            ]
            diff_result = '\n'.join(filtered_diff_lines)

            # Write the differences to the log file if there are any differences
            if filtered_diff_lines:
                write_log(log_file_path, base_file_path, compare_file_path, diff_result)
            else:
                write_log(log_file_path, base_file_path, compare_file_path, f"{base_hostname} - No differences found.")

            # Display the differences
            print(diff_result)

            # Check if the interfaces settings are valid
            if interfaces_valid:
                print("All required interface settings are present.")
            else:
                print("Some required interface settings are missing.")
