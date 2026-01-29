import tkinter as tk
import tkinter.font as tkfont
import hashlib
import itertools
import string

# Global variable to track if the rainbow table has been generated
rainbow_table = {}

# Generate rainbow table for strings of 0-4 characters, only lowercase a-z
def generate_rainbow_table():
    global rainbow_table
    rainbow_table = {}  # Clear any existing table

    # Generate strings of lengths 0 to 4 using lowercase a-z
    chars = string.ascii_lowercase # + string.ascii_uppercase
    for length in range(5):  # 0 to 4 characters
        for combo in itertools.product(chars, repeat=length):
            plain_text = ''.join(combo)
            md5_hash = hashlib.md5(plain_text.encode()).hexdigest().lower()
            rainbow_table[md5_hash] = plain_text

    # Update the status to show the count of generated entries
    status_label.config(text="Rainbow table generated with {} entries.".format(len(rainbow_table)))

# Function to look up hash in the rainbow table
def lookup_hash():
    # If the rainbow table hasn't been generated yet, generate it
    if not rainbow_table:
        generate_rainbow_table()

    hash_to_lookup = hash_entry.get().strip().lower()

    if hash_to_lookup in rainbow_table:
        result_text.set("Match found: {}".format(rainbow_table[hash_to_lookup]))
    else:
        result_text.set("No match found in the rainbow table.")

# Create the main window
root = tk.Tk()
root.title("MD5 Rainbow Table Lookup")

# Set default font for all widgets
default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(size=22)
root.option_add("*Font", default_font)

# Create a button to generate the rainbow table
generate_button = tk.Button(root, text="Generate Rainbow Table", command=generate_rainbow_table)
generate_button.pack(pady=10)

# Create an entry box to input the hash to lookup
hash_label = tk.Label(root, text="MD5 Hash to Lookup:")
hash_label.pack()
hash_entry = tk.Entry(root, width=50)
hash_entry.pack(pady=5)

# Create a button to perform the hash lookup
lookup_button = tk.Button(root, text="Lookup Hash", command=lookup_hash)
lookup_button.pack(pady=10)

# Create a label to display the lookup result
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, fg="blue")
result_label.pack(pady=10)

# Status label for rainbow table generation
status_label = tk.Label(root, text="Rainbow table not generated yet.")
status_label.pack(pady=10)

# Run the application
root.mainloop()
