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
            database="gpu data"  
        )

        if connection.is_connected():
            print("Successfully connected to MySQL")
            cursor = connection.cursor()
            query = "SELECT productName FROM gpu_spec_final LIMIT 2000"  
            cursor.execute(query)
            cursor.arraysize = 2000
            
            result = []
            while True:
                batch = cursor.fetchmany(cursor.arraysize)
                if not batch:
                    break
                result.extend(batch)

            product_names = [row[0] for row in result]
            return product_names

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed")

def iterative_sequential_search(data, target):
    n = len(data)  
    for i in range(n):  
        if data[i].lower() == target.lower():
            return i
    return -1

def recursive_sequential_search(data, target, index=0):
    n = len(data) 
    if index >= n:  
        return -1
    elif data[index].lower() == target.lower():  
        return index
    else:
        return recursive_sequential_search(data, target, index + 1)  

def perform_iterative_search():
    target_product = entry.get().strip()  
    if not target_product:
        messagebox.showerror("Error", "Please enter a product name to search.")
        return

    products = fetch_product_names()
    if products:
        iterative_times_local = []  
        for _ in range(5):  
            start_time = time.time()  
            result_iterative = iterative_sequential_search(products, target_product)
            end_time = time.time()  
            iterative_time = end_time - start_time
            iterative_times_local.append(iterative_time)

        iterative_times.extend(iterative_times_local)  # Update global list

        if result_iterative != -1:
            result_iterative_text.set(f"Product found: '{products[result_iterative]}'")
        else:
            result_iterative_text.set(f"Product '{target_product}' not found.")
        
        update_comparison_graph()  # Update graph after iterative search

    else:
        messagebox.showerror("Error", "No products found in the database.")

def perform_recursive_search():
    target_product = entry.get().strip()  
    if not target_product:
        messagebox.showerror("Error", "Please enter a product name to search.")
        return

    products = fetch_product_names()
    if products:
        recursive_times_local = []  
        for _ in range(5): 
            start_time = time.time()  
            result_recursive = recursive_sequential_search(products, target_product)
            end_time = time.time()
            recursive_time = end_time - start_time
            recursive_times_local.append(recursive_time)
        
        recursive_times.extend(recursive_times_local)  # Update global list
        
        if result_recursive != -1:
            result_recursive_text.set(f"Product found: '{products[result_recursive]}'")
        else:
            result_recursive_text.set(f"Product '{target_product}' not found.")
        
        update_comparison_graph()  # Update graph after recursive search

    else:
        messagebox.showerror("Error", "No products found in the database.")

# Global variables to track search times
iterative_times = []
recursive_times = []

# Function to update the comparison graph showing both search types together
def update_comparison_graph():
    ax.clear()
    ax.plot(iterative_times, label='Iterative Search', color='blue')
    ax.plot(recursive_times, label='Recursive Search', color='red')
    ax.set_title('Comparison of Iterative and Recursive Search Times')
    ax.set_xlabel('Search Attempt')
    ax.set_ylabel('Time (seconds)')
    ax.legend()

    canvas.draw()

root = tk.Tk()
root.title("Product Search")

# Set up the UI components
label = tk.Label(root, text="Enter the product name to search:")
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Buttons for iterative and recursive search
iterative_button = tk.Button(root, text="Search Iterative (5 times)", command=perform_iterative_search)
iterative_button.pack(pady=10)

recursive_button = tk.Button(root, text="Search Recursive (5 times)", command=perform_recursive_search)
recursive_button.pack(pady=10)

# Display results for iterative search
result_iterative_text = tk.StringVar()
result_iterative_label = tk.Label(root, textvariable=result_iterative_text, wraplength=300)
result_iterative_label.pack(pady=5)

# Display results for recursive search
result_recursive_text = tk.StringVar()
result_recursive_label = tk.Label(root, textvariable=result_recursive_text, wraplength=300)
result_recursive_label.pack(pady=5)

# Set up the matplotlib figure and axes for a single comparison graph
fig, ax = plt.subplots(figsize=(8, 6))  # One single axis for the comparison graph

# Create the Tkinter canvas and embed the plot in the window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)
canvas.draw()

# Run the main loop
root.mainloop()
