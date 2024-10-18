import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

class PasswordGeneratorGUI:
    def _init_(self, master):
        self.master = master
        master.title("Random Password Generator")
        master.resizable(False, False)
        master.geometry("400x300")
        master.configure(padx=20, pady=20)

        # Password Length
        self.length_label = tk.Label(master, text="Password Length:")
        self.length_label.grid(row=0, column=0, sticky="w")

        self.length_var = tk.IntVar(value=12)
        self.length_entry = tk.Entry(master, textvariable=self.length_var)
        self.length_entry.grid(row=0, column=1, pady=5, sticky="e")

        # Character Types
        self.letters_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.letters_check = tk.Checkbutton(master, text="Letters (A-Z, a-z)", variable=self.letters_var)
        self.letters_check.grid(row=1, column=0, columnspan=2, sticky="w")

        self.numbers_check = tk.Checkbutton(master, text="Numbers (0-9)", variable=self.numbers_var)
        self.numbers_check.grid(row=2, column=0, columnspan=2, sticky="w")

        self.symbols_check = tk.Checkbutton(master, text="Symbols (!@#$...)", variable=self.symbols_var)
        self.symbols_check.grid(row=3, column=0, columnspan=2, sticky="w")

        # Exclude Characters
        self.exclude_label = tk.Label(master, text="Exclude Characters:")
        self.exclude_label.grid(row=4, column=0, sticky="w", pady=(10,0))

        self.exclude_entry = tk.Entry(master)
        self.exclude_entry.grid(row=4, column=1, pady=(10,0), sticky="e")

        # Generate Button
        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Password Display
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(master, textvariable=self.password_var, width=30, state='readonly')
        self.password_entry.grid(row=6, column=0, columnspan=2, pady=5)

        # Copy Button
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=7, column=0, columnspan=2, pady=5)

    def generate_password(self):
        try:
            length = self.length_var.get()
            if length < 4:
                messagebox.showerror("Error", "Password length should be at least 4.")
                return

            include_letters = self.letters_var.get()
            include_numbers = self.numbers_var.get()
            include_symbols = self.symbols_var.get()

            if not (include_letters or include_numbers or include_symbols):
                messagebox.showerror("Error", "Select at least one character type.")
                return

            exclude_chars = self.exclude_entry.get()

            character_set = ''
            if include_letters:
                character_set += string.ascii_letters
            if include_numbers:
                character_set += string.digits
            if include_symbols:
                character_set += string.punctuation

            # Remove excluded characters
            if exclude_chars:
                character_set = ''.join([c for c in character_set if c not in exclude_chars])

            if not character_set:
                messagebox.showerror("Error", "No characters available to generate password after exclusions.")
                return

            # Ensure at least one character from each selected set is included
            password = []
            if include_letters:
                letters = ''.join([c for c in string.ascii_letters if c not in exclude_chars])
                if letters:
                    password.append(random.choice(letters))
                else:
                    messagebox.showerror("Error", "No letters available after exclusions.")
                    return
            if include_numbers:
                numbers = ''.join([c for c in string.digits if c not in exclude_chars])
                if numbers:
                    password.append(random.choice(numbers))
                else:
                    messagebox.showerror("Error", "No numbers available after exclusions.")
                    return
            if include_symbols:
                symbols = ''.join([c for c in string.punctuation if c not in exclude_chars])
                if symbols:
                    password.append(random.choice(symbols))
                else:
                    messagebox.showerror("Error", "No symbols available after exclusions.")
                    return

            if len(password) > length:
                messagebox.showerror("Error", "Password length is too short for the selected criteria.")
                return

            # Fill the rest of the password length
            if len(password) < length:
                password += random.choices(character_set, k=length - len(password))

            # Shuffle to prevent predictable sequences
            random.shuffle(password)

            final_password = ''.join(password)
            self.password_var.set(final_password)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first.")

def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "_main_":
    main()