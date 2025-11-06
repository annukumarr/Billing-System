# ==========================================================
# Billing System for a Shop (GUI Version)
# Developed by: Annu Kumar Pal | UID: 25MCI10230
# Course: MCA (AI & ML) | Chandigarh University, Mohali
# ==========================================================

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os

# -------------------------------------------
# Item Class
# -------------------------------------------
class Item:
    def __init__(self, name, price, quantity):
        self.name = name.strip()
        self.price = float(price)
        self.quantity = int(quantity)
        self.total = self.price * self.quantity


# -------------------------------------------
# Bill Class
# -------------------------------------------
class Bill:
    def __init__(self):
        self.items = []
        self.gst_rate = 0.05
        self.discount_rate = 0.10
        self.save_directory = r"C:\Users\Asus\OneDrive\Desktop\CU\Python\Project"

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def add_item(self, name, price, quantity):
        try:
            item = Item(name, price, quantity)
            self.items.append(item)
            return True
        except ValueError:
            return False

    def _totals(self):
        subtotal = sum(i.total for i in self.items)
        gst = subtotal * self.gst_rate
        discount = subtotal * self.discount_rate
        final_total = subtotal + gst - discount
        return subtotal, gst, discount, final_total

    def save_bill(self):
        if not self.items:
            return None

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Bill_{timestamp}.txt"
        filepath = os.path.join(self.save_directory, filename)

        lines = []
        lines.append("===== ANNU’S SHOP BILL RECEIPT =====")
        lines.append("Item Name       Price      Qty        Total")
        lines.append("-----------------------------------------------")
        for item in self.items:
            lines.append(f"{item.name[:15]:15} {item.price:<10.2f} {item.quantity:<10} {item.total:<10.2f}")

        subtotal, gst, discount, final_total = self._totals()
        lines.append("-----------------------------------------------")
        lines.append(f"Subtotal: ₹{subtotal:.2f}")
        lines.append(f"GST (5%): ₹{gst:.2f}")
        lines.append(f"Discount (10%): ₹{discount:.2f}")
        lines.append(f"Final Amount: ₹{final_total:.2f}")
        lines.append("-----------------------------------------------")
        lines.append(f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        content = "\n".join(lines)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            os.startfile(filepath)
            return filepath
        except Exception as e:
            return str(e)


# -------------------------------------------
# GUI Application
# -------------------------------------------
class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧾 Annu’s Billing System")
        self.root.geometry("800x600")
        self.root.config(bg="#F9F9F9")

        self.bill = Bill()

        # ====== Title ======
        title = tk.Label(root, text="🛒 ANNU’S SHOP BILLING SYSTEM", font=("Arial", 18, "bold"), bg="#2E86C1", fg="white", pady=10)
        title.pack(fill=tk.X)

        # ====== Input Frame ======
        frame = tk.Frame(root, bg="#F9F9F9", pady=10)
        frame.pack()

        tk.Label(frame, text="Item Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame, text="Price (₹):", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(frame, text="Quantity:", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=5)

        self.name_entry = tk.Entry(frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=10)

        self.price_entry = tk.Entry(frame, width=10)
        self.price_entry.grid(row=0, column=3, padx=10)

        self.qty_entry = tk.Entry(frame, width=10)
        self.qty_entry.grid(row=0, column=5, padx=10)

        add_btn = tk.Button(frame, text="➕ Add Item", command=self.add_item, bg="#28B463", fg="white", font=("Arial", 11, "bold"), width=12)
        add_btn.grid(row=0, column=6, padx=10)

        # ====== Table Frame ======
        self.tree = ttk.Treeview(root, columns=("Name", "Price", "Quantity", "Total"), show='headings', height=12)
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Price", text="Price (₹)")
        self.tree.heading("Quantity", text="Qty")
        self.tree.heading("Total", text="Total (₹)")

        self.tree.column("Name", width=200)
        self.tree.column("Price", width=100, anchor=tk.CENTER)
        self.tree.column("Quantity", width=100, anchor=tk.CENTER)
        self.tree.column("Total", width=120, anchor=tk.CENTER)
        self.tree.pack(pady=10)

        # ====== Summary Frame ======
        self.summary_label = tk.Label(root, text="Subtotal: ₹0.00 | GST: ₹0.00 | Discount: ₹0.00 | Final: ₹0.00", font=("Arial", 12, "bold"), bg="#F9F9F9", fg="#2E4053")
        self.summary_label.pack(pady=10)

        # ====== Buttons ======
        btn_frame = tk.Frame(root, bg="#F9F9F9")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="💾 Save Bill", command=self.save_bill, bg="#5DADE2", fg="white", font=("Arial", 11, "bold"), width=15).grid(row=0, column=0, padx=15)
        tk.Button(btn_frame, text="🧾 View Totals", command=self.update_summary, bg="#AF7AC5", fg="white", font=("Arial", 11, "bold"), width=15).grid(row=0, column=1, padx=15)
        tk.Button(btn_frame, text="❌ Exit", command=root.quit, bg="#E74C3C", fg="white", font=("Arial", 11, "bold"), width=15).grid(row=0, column=2, padx=15)

    # ====== Functions ======
    def add_item(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        qty = self.qty_entry.get()

        if not name or not price or not qty:
            messagebox.showwarning("Input Error", "Please fill all fields!")
            return

        if self.bill.add_item(name, price, qty):
            last_item = self.bill.items[-1]
            self.tree.insert("", "end", values=(last_item.name, f"{last_item.price:.2f}", last_item.quantity, f"{last_item.total:.2f}"))
            self.update_summary()
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Price must be a number & Quantity must be an integer!")

    def update_summary(self):
        if not self.bill.items:
            self.summary_label.config(text="No items added yet!")
            return

        subtotal, gst, discount, final_total = self.bill._totals()
        self.summary_label.config(
            text=f"Subtotal: ₹{subtotal:.2f} | GST: ₹{gst:.2f} | Discount: ₹{discount:.2f} | Final: ₹{final_total:.2f}"
        )

    def save_bill(self):
        path = self.bill.save_bill()
        if path:
            messagebox.showinfo("Bill Saved", f"Bill saved successfully!\nLocation:\n{path}")
        else:
            messagebox.showwarning("Save Failed", "No items to save or error occurred!")


# -------------------------------------------
# Run the App
# -------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
