import tkinter as tk
import string  # To check for printable characters

# Function to check the key and convert text to binary and XOR with key
def update_xor_and_check_key(event):
    key = key_entry.get().strip()  # Get the key from the entry box
    input_text = text_box.get("1.0", tk.END).strip()  # Get the text from the text box

    # Clear the output boxes
    source_binary_output.delete("1.0", tk.END)
    key_binary_output.delete("1.0", tk.END)
    xor_binary_output.delete("1.0", tk.END)

    if not key:  # If no key is entered, disable the text box and return
        text_box.config(state=tk.DISABLED)
        return
    else:  # Unlock the text box if a key is entered
        text_box.config(state=tk.NORMAL)

    # Ensure the key loops continuously until it matches the input text length
    extended_key = (key * ((len(input_text) // len(key)) + 1))[:len(input_text)]

    # XOR each character of the input with the corresponding character of the key
    xor_result = [chr(ord(a) ^ ord(b)) for a, b in zip(input_text, extended_key)]

    # Convert source text to binary
    source_binary = ' '.join(format(ord(char), '08b') for char in input_text)
    source_binary_output.insert(tk.END, source_binary)

    # Convert key text to binary (extended key)
    key_binary = ' '.join(format(ord(char), '08b') for char in extended_key)
    key_binary_output.insert(tk.END, key_binary)

    # Convert XOR result to binary and append the ASCII character or '?' for non-printable
    xor_binary_with_ascii = ' '.join(
        f"{format(ord(char), '08b')} ({char if char in string.printable and char.isprintable() else '?'})"
        for char in xor_result
    )
    xor_binary_output.insert(tk.END, xor_binary_with_ascii)

# Function to increase font size
def increase_font_size():
    current_font = text_box.cget("font")
    current_size = int(current_font.split()[1])  # Extract current font size
    new_size = current_size + 2
    update_font_size(new_size)

# Function to decrease font size
def decrease_font_size():
    current_font = text_box.cget("font")
    current_size = int(current_font.split()[1])  # Extract current font size
    new_size = max(current_size - 2, 6)  # Ensure font size doesn't go below 6
    update_font_size(new_size)

# Function to update font size for all relevant widgets
def update_font_size(size):
    font_config = ("Arial", size)
    text_box.config(font=font_config)
    key_entry.config(font=font_config)  # Update font size of the key input
    source_binary_output.config(font=font_config)
    key_binary_output.config(font=font_config)
    xor_binary_output.config(font=font_config)

# Create the main window
root = tk.Tk()
root.title("Text XOR with Key to Binary Converter")

# Create a text box for input text (initially disabled)
text_box = tk.Text(root, height=5, width=50, state=tk.DISABLED, font=("Arial", 10))
text_box.pack()

# Create a label and an entry field for the XOR key
key_label = tk.Label(root, text="XOR Key:")
key_label.pack()
key_entry = tk.Entry(root, font=("Arial", 10))
key_entry.pack()

# Bind both the text box and key entry to the combined function
text_box.bind("<KeyRelease>", update_xor_and_check_key)
key_entry.bind("<KeyRelease>", update_xor_and_check_key)  # Also bind to the combined function

# Create labels and text boxes for displaying the binary output
source_binary_label = tk.Label(root, text="Source Text Binary:")
source_binary_label.pack()
source_binary_output = tk.Text(root, height=5, width=50, font=("Arial", 10))
source_binary_output.pack()

key_binary_label = tk.Label(root, text="Key Binary:")
key_binary_label.pack()
key_binary_output = tk.Text(root, height=5, width=50, font=("Arial", 10))
key_binary_output.pack()

xor_binary_label = tk.Label(root, text="XOR Result Binary (with ASCII or '?'):")
xor_binary_label.pack()
xor_binary_output = tk.Text(root, height=5, width=50, font=("Arial", 10))
xor_binary_output.pack()

# Create buttons for changing font size
font_buttons_frame = tk.Frame(root)
font_buttons_frame.pack(pady=10)

increase_font_button = tk.Button(font_buttons_frame, text="Bigger Font", command=increase_font_size)
increase_font_button.pack(side=tk.LEFT, padx=10)

decrease_font_button = tk.Button(font_buttons_frame, text="Smaller Font", command=decrease_font_size)
decrease_font_button.pack(side=tk.LEFT, padx=10)

# Run the application
root.mainloop()
