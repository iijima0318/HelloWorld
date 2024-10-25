import psutil
import os
import tkinter as tk
from tkinter import filedialog

def get_task_manager_snapshot():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    
    snapshot = "PID     Process Name               CPU%     Memory%\n"
    snapshot += "---------------------------------------------------\n"
    
    for proc in processes[:10]:  # Top 10 processes
        snapshot += f"{proc['pid']:<8} {proc['name']:<25} {proc['cpu_percent']:<8} {proc['memory_percent']:.2f}\n"
    
    return snapshot

def save_snapshot_to_file(snapshot):
    root = tk.Tk()
    root.withdraw()  # Close the root window

    # Get the current directory
    current_directory = os.getcwd()
    
    # Open the file dialog
    file_path = filedialog.asksaveasfilename(initialdir=current_directory, defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(snapshot)
        print(f"Snapshot saved to {file_path}")
    else:
        print("Save operation cancelled")

if __name__ == "__main__":
    snapshot = get_task_manager_snapshot()
    print(snapshot)
    save_snapshot_to_file(snapshot)
