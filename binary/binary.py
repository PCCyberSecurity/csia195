import tkinter as tk
import tkinter.font as tkfont

# Function to convert text to binary and display it
def display_binary(event):
    input_text = text_box.get("1.0", tk.END).strip()  # Get the text from the text box
    binary_output.delete("1.0", tk.END)  # Clear the output box
    binary_values = ' '.join(format(ord(char), '08b') for char in input_text)
    binary_output.insert(tk.END, binary_values)

# Create the main window
root = tk.Tk()
root.title("Text to Binary Converter")

# Set default font for all widgets
default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(size=22)
root.option_add("*Font", default_font)

# Create a text box for input
text_box = tk.Text(root, height=5, width=50)
text_box.pack()

# Bind the key release event to update the binary output
text_box.bind("<KeyRelease>", display_binary)

# Create a text box for displaying binary output
binary_output = tk.Text(root, height=5, width=50)
binary_output.pack()

# Run the application
root.mainloop()
