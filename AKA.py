import mysql.connector
import time
import sys
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.setrecursionlimit(2000)

def fetch_product_names():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="gpu data"  # Nama database harus sesuai
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT productName FROM gpu_spec_final LIMIT 2000"
            cursor.execute(query)
            result = cursor.fetchall()
            return [row[0] for row in result]

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if connection and connection.is_connected():
            connection.close()

def fetch_product_row_and_name(target):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="gpu data"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT productName FROM gpu_spec_final WHERE productName = %s"
            cursor.execute(query, (target,))
            result = cursor.fetchone()
            return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection and connection.is_connected():
            connection.close()

def iterative_sequential_search(data, target):
    n = len(data)  
    for i in range(n):  
        if data[i].lower() == target.lower():
            return i
    return -1


def recursive_sequential_search(data, target, index=0):
    if index >= len(data):
        return -1
    if data[index].lower() == target.lower():
        return index
    return recursive_sequential_search(data, target, index + 1)

def perform_iterative_search():
    target_product = entry.get()
    products = fetch_product_names()

    if products:
        start_time = time.time()
        result_iterative = iterative_sequential_search(products, target_product)
        end_time = time.time()
        iterative_time = end_time - start_time

        if result_iterative != -1:
            product_data = fetch_product_row_and_name(target_product)
            result_iterative_text.set(
                f"Iterative: Found '{product_data[0]}' at row {result_iterative}."
            )
        else:
            result_iterative_text.set(f"Iterative: '{target_product}' not found.")
        time_iterative_text.set(f"Iterative search time: {iterative_time:.6f} seconds")

        iterative_times.append(iterative_time)
        update_comparison_graph()
    else:
        messagebox.showerror("Error", "No products found in the database.")

def perform_recursive_search():
    target_product = entry.get()
    products = fetch_product_names()

    if products:
        start_time = time.time()
        result_recursive = recursive_sequential_search(products, target_product)
        end_time = time.time()
        recursive_time = end_time - start_time

        if result_recursive != -1:
            product_data = fetch_product_row_and_name(target_product)
            result_recursive_text.set(
                f"Recursive: Found '{product_data[0]}' at row {result_recursive}."
            )
        else:
            result_recursive_text.set(f"Recursive: '{target_product}' not found.")
        time_recursive_text.set(f"Recursive search time: {recursive_time:.6f} seconds")

        recursive_times.append(recursive_time)
        update_comparison_graph()
    else:
        messagebox.showerror("Error", "No products found in the database.")

def update_comparison_graph():
    # Calculate cumulative times for iterative and recursive search
    cumulative_iterative_times = [sum(iterative_times[:i + 1]) for i in range(len(iterative_times))]
    cumulative_recursive_times = [sum(recursive_times[:i + 1]) for i in range(len(recursive_times))]

    # Clear the previous plot
    ax.clear()
    
    # Plot cumulative times
    ax.plot(cumulative_iterative_times, label='Cumulative Iterative Search', color='blue')
    ax.plot(cumulative_recursive_times, label='Cumulative Recursive Search', color='red')

    # Set graph labels and title
    ax.set_title('Cumulative Comparison of Iterative and Recursive Search Times')
    ax.set_xlabel('Search Attempt')
    ax.set_ylabel('Cumulative Time (seconds)')
    ax.legend()

    # Redraw the graph
    canvas.draw()

root = tk.Tk()
root.title("Product Search")

# Label untuk input pencarian
label = tk.Label(root, text="Enter the product name to search:")
label.pack(pady=10)

# Input field
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Tombol pencarian
iterative_button = tk.Button(root, text="Search Iterative", command=perform_iterative_search)
iterative_button.pack(pady=5)

recursive_button = tk.Button(root, text="Search Recursive", command=perform_recursive_search)
recursive_button.pack(pady=5)

# Hasil pencarian iterative
result_iterative_text = tk.StringVar()
result_iterative_label = tk.Label(root, textvariable=result_iterative_text, wraplength=300)
result_iterative_label.pack(pady=5)

time_iterative_text = tk.StringVar()
time_iterative_label = tk.Label(root, textvariable=time_iterative_text, wraplength=300)
time_iterative_label.pack(pady=5)

# Hasil pencarian recursive
result_recursive_text = tk.StringVar()
result_recursive_label = tk.Label(root, textvariable=result_recursive_text, wraplength=300)
result_recursive_label.pack(pady=5)

time_recursive_text = tk.StringVar()
time_recursive_label = tk.Label(root, textvariable=time_recursive_text, wraplength=300)
time_recursive_label.pack(pady=5)

# Matplotlib figure
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)
canvas.draw()

# Variabel untuk menyimpan waktu pencarian
iterative_times = []
recursive_times = []

root.mainloop()