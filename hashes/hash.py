import tkinter as tk
import hashlib

# Function to update the hash values when text or salt is typed
def update_hashes(event):
    input_text = text_box.get("1.0", tk.END).strip()  # Get the input text from the text box
    salt = salt_entry.get().strip()  # Get the salt from the salt entry box

    # Concatenate input text and salt
    salted_text = input_text + salt

    # Compute MD5, SHA1, and SHA256 hashes
    md5_hash = hashlib.md5(salted_text.encode()).hexdigest()
    sha1_hash = hashlib.sha1(salted_text.encode()).hexdigest()
    sha256_hash = hashlib.sha256(salted_text.encode()).hexdigest()

    # Clear the output boxes
    md5_output.delete("1.0", tk.END)
    sha1_output.delete("1.0", tk.END)
    sha256_output.delete("1.0", tk.END)

    # Insert the hashes into the output text boxes
    md5_output.insert(tk.END, md5_hash)
    sha1_output.insert(tk.END, sha1_hash)
    sha256_output.insert(tk.END, sha256_hash)

# Create the main window
root = tk.Tk()
root.title("Real-time Hash Generator with Salt")

# Create a text box for input text
text_label = tk.Label(root, text="Input Text:")
text_label.pack()
text_box = tk.Text(root, height=5, width=50)
text_box.pack()

# Create a label and entry for salt
salt_label = tk.Label(root, text="Salt Value:")
salt_label.pack()
salt_entry = tk.Entry(root)
salt_entry.pack()

# Bind both the text box and salt entry to the update_hashes function, updating on each key release
text_box.bind("<KeyRelease>", update_hashes)
salt_entry.bind("<KeyRelease>", update_hashes)

# Create labels and text boxes for MD5, SHA1, and SHA256 outputs
md5_label = tk.Label(root, text="MD5 Hash:")
md5_label.pack()
md5_output = tk.Text(root, height=2, width=50)
md5_output.pack()

sha1_label = tk.Label(root, text="SHA-1 Hash:")
sha1_label.pack()
sha1_output = tk.Text(root, height=2, width=50)
sha1_output.pack()

sha256_label = tk.Label(root, text="SHA-256 Hash:")
sha256_label.pack()
sha256_output = tk.Text(root, height=2, width=50)
sha256_output.pack()

# Run the application
root.mainloop()
