import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database setup
def init_db():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# BMI Calculation and Classification
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# GUI Application
class BMICalculatorApp:
    def _init_(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.create_widgets()

    def create_widgets(self):
        # User Frame
        user_frame = ttk.Frame(self.root, padding="10")
        user_frame.grid(row=0, column=0, sticky="W")

        ttk.Label(user_frame, text="Username:").grid(row=0, column=0, sticky="W")
        self.username_entry = ttk.Entry(user_frame)
        self.username_entry.grid(row=0, column=1, sticky="W")
        self.login_button = ttk.Button(user_frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=2, padx=5)

        # Input Frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=1, column=0, sticky="W")

        ttk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0, sticky="W")
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Height (m):").grid(row=1, column=0, sticky="W")
        self.height_entry = ttk.Entry(input_frame)
        self.height_entry.grid(row=1, column=1, padx=5)

        self.calculate_button = ttk.Button(input_frame, text="Calculate BMI", command=self.calculate_bmi_action)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Result Frame
        result_frame = ttk.Frame(self.root, padding="10")
        result_frame.grid(row=2, column=0, sticky="W")

        self.bmi_label = ttk.Label(result_frame, text="BMI: N/A")
        self.bmi_label.grid(row=0, column=0, sticky="W")

        self.category_label = ttk.Label(result_frame, text="Category: N/A")
        self.category_label.grid(row=1, column=0, sticky="W")

        # History Frame
        history_frame = ttk.Frame(self.root, padding="10")
        history_frame.grid(row=3, column=0, sticky="W")

        ttk.Label(history_frame, text="BMI History:").grid(row=0, column=0, sticky="W")

        self.tree = ttk.Treeview(history_frame, columns=("Date", "Weight", "Height", "BMI", "Category"), show='headings')
        for col in ("Date", "Weight", "Height", "BMI", "Category"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, sticky="W")

        self.refresh_button = ttk.Button(history_frame, text="Refresh History", command=self.load_history)
        self.refresh_button.grid(row=2, column=0, pady=5)

        # Plot Frame
        plot_frame = ttk.Frame(self.root, padding="10")
        plot_frame.grid(row=4, column=0, sticky="W")

        self.plot_button = ttk.Button(plot_frame, text="Show BMI Trend", command=self.plot_bmi_trend)
        self.plot_button.grid(row=0, column=0, pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
        conn = sqlite3.connect('bmi_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            self.user_id = result[0]
        else:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            self.user_id = cursor.lastrowid
            conn.commit()
            messagebox.showinfo("Welcome", f"New user '{username}' created.")
        conn.close()
        self.load_history()

    def calculate_bmi_action(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers for weight and height.")
            return

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        self.bmi_label.config(text=f"BMI: {bmi:.2f}")
        self.category_label.config(text=f"Category: {category}")

        # Save to database
        conn = sqlite3.connect('bmi_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bmi_records (user_id, date, weight, height, bmi, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi, category))
        conn.commit()
        conn.close()

        self.load_history()

    def load_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect('bmi_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, weight, height, bmi, category FROM bmi_records
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (self.user_id,))
        records = cursor.fetchall()
        for record in records:
            self.tree.insert("", "end", values=record)
        conn.close()

    def plot_bmi_trend(self):
        conn = sqlite3.connect('bmi_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, bmi FROM bmi_records
            WHERE user_id = ?
            ORDER BY date
        ''', (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No BMI records to plot.")
            return

        dates = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S") for record in data]
        bmis = [record[1] for record in data]

        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(dates, bmis, marker='o', linestyle='-')
        ax.set_title("BMI Trend Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.grid(True)

        # Clear previous plot if exists
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

        # Create new window for plot
        plot_window = tk.Toplevel(self.root)
        plot_window.title("BMI Trend")

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Initialize the database
init_db()

# Run the application
def main():
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()

if __name__ == "_main_":
    main()