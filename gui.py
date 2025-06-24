### gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from bot import BasicBot
import os
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException

# Load keys
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
bot = BasicBot(API_KEY, API_SECRET)

# ─────────────────── GUI ───────────────────
root = tk.Tk()
root.title("📈 Binance Futures Testnet Bot")
root.geometry("600x700")
root.resizable(False, False)

# ─── THEME ──────────────────────────────────
theme = {"bg": "#ffffff", "fg": "#000000"}

def apply_theme():
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Entry, tk.Button, tk.Text, ttk.Combobox)):
            try:
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            except:
                pass
        if isinstance(widget, tk.Text):
            widget.configure(insertbackground=theme["fg"])

def toggle_theme():
    if theme["bg"] == "#ffffff":
        theme.update({"bg": "#222222", "fg": "#eeeeee"})
    else:
        theme.update({"bg": "#ffffff", "fg": "#000000"})
    apply_theme()

# ─── Variables ──────────────────────────────
symbol_var = tk.StringVar(value="BTCUSDT")
side_var = tk.StringVar(value="BUY")
order_type_var = tk.StringVar(value="MARKET")
qty_var = tk.StringVar()
price_var = tk.StringVar()
stop_price_var = tk.StringVar()
limit_price_var = tk.StringVar()
tp_price_var = tk.StringVar()
oco_stop_price_var = tk.StringVar()
oco_stop_limit_var = tk.StringVar()
cancel_id_var = tk.StringVar()

# ─── Output Log ─────────────────────────────
output_box = tk.Text(root, height=12, width=70, bg="#f7f7f7", wrap="word")
output_box.insert(tk.END, "🔹 Bot started. Ready to place orders.\n")
output_box.configure(state='disabled')

def log(msg):
    output_box.configure(state='normal')
    output_box.insert(tk.END, msg + "\n")
    output_box.see(tk.END)
    output_box.configure(state='disabled')

# ─── Dynamic Field Visibility ───────────────
def update_fields(*args):
    t = order_type_var.get()
    for entry in [price_entry, stop_price_entry, stop_limit_entry]:
        entry.grid_remove()

    if t == "LIMIT":
        price_entry.grid()
    elif t == "STOP_LIMIT":
        stop_price_entry.grid()
        stop_limit_entry.grid()

# ─── Order Actions ──────────────────────────
def place_order():
    try:
        symbol = symbol_var.get().upper()
        side = side_var.get().upper()
        qty = float(qty_var.get())

        if order_type_var.get() == "MARKET":
            try:
                resp = bot.market(symbol, side, qty)
                if isinstance(resp, dict) and "error" in resp:
                    log(f"❌ {resp['error']}")
                else:
                    log("✅ Market order sent.")
            except BinanceAPIException as e:
                log(f"❌ Market order failed: {e.message}")

        elif order_type_var.get() == "LIMIT":
            price = float(price_var.get())
            resp = bot.limit(symbol, side, qty, price)
            if isinstance(resp, dict) and "error" in resp:
                log(f"❌ {resp['error']}")
            else:
                log(f"✅ Limit order at {price} sent.")

        elif order_type_var.get() == "STOP_LIMIT":
            sp = float(stop_price_var.get())
            lp = float(limit_price_var.get())
            resp = bot.stop_limit(symbol, side, qty, sp, lp)
            if isinstance(resp, dict) and "error" in resp:
                log(f"❌ {resp['error']}")
            else:
                log(f"✅ Stop-Limit order sent: Stop {sp}, Limit {lp}")

        else:
            messagebox.showerror("Invalid", "Select a valid order type.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        log("❌ Order failed.")

def view_open_orders():
    symbol = symbol_var.get().upper()
    try:
        orders = bot.client.futures_get_open_orders(symbol=symbol)
        if not orders:
            log("📭 No open orders.")
        else:
            log("📋 Open Orders:")
            for o in orders:
                log(f"ID {o['orderId']} | {o['type']} {o['side']} Qty={o['origQty']} Price={o['price']} Status={o['status']}")
    except Exception as e:
        log("❌ Failed to fetch open orders.")

def cancel_order():
    symbol = symbol_var.get().upper()
    oid = cancel_id_var.get()
    if not oid.isdigit():
        messagebox.showerror("Invalid", "Enter a valid Order ID.")
        return
    try:
        bot.cancel(symbol, int(oid))
        log(f"✅ Cancelled Order ID {oid}")
    except Exception as e:
        log(f"❌ Cancel failed for ID {oid}")

def simulate_oco():
    try:
        symbol = symbol_var.get().upper()
        side = side_var.get().upper()
        qty = float(qty_var.get())
        tp = float(tp_price_var.get())
        sp = float(oco_stop_price_var.get())
        sl = float(oco_stop_limit_var.get())

        tp_resp, sl_resp = bot.oco_simulated(symbol, side, qty, tp, sp, sl)
        if isinstance(tp_resp, dict) and "error" in tp_resp:
            log(f"❌ TP Error: {tp_resp['error']}")
        if isinstance(sl_resp, dict) and "error" in sl_resp:
            log(f"❌ SL Error: {sl_resp['error']}")
        if not (isinstance(tp_resp, dict) and "error" in tp_resp) and not (isinstance(sl_resp, dict) and "error" in sl_resp):
            log("📈 OCO simulation started.")
    except Exception as e:
        log("❌ OCO failed: " + str(e))

# ─── GUI Layout ─────────────────────────────
tk.Button(root, text="🌗 Toggle Theme", command=toggle_theme).grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(root, text="Symbol").grid(row=1, column=0, sticky="w", padx=10)
tk.Entry(root, textvariable=symbol_var).grid(row=1, column=1)

tk.Label(root, text="Side").grid(row=2, column=0, sticky="w", padx=10)
ttk.Combobox(root, textvariable=side_var, values=["BUY", "SELL"]).grid(row=2, column=1)

tk.Label(root, text="Order Type").grid(row=3, column=0, sticky="w", padx=10)
ot = ttk.Combobox(root, textvariable=order_type_var, values=["MARKET", "LIMIT", "STOP_LIMIT"])
ot.grid(row=3, column=1)
order_type_var.trace("w", update_fields)

tk.Label(root, text="Quantity").grid(row=4, column=0, sticky="w", padx=10)
tk.Entry(root, textvariable=qty_var).grid(row=4, column=1)

tk.Label(root, text="Limit Price").grid(row=5, column=0, sticky="w", padx=10)
price_entry = tk.Entry(root, textvariable=price_var)
price_entry.grid(row=5, column=1)

tk.Label(root, text="Stop Price").grid(row=6, column=0, sticky="w", padx=10)
stop_price_entry = tk.Entry(root, textvariable=stop_price_var)
stop_price_entry.grid(row=6, column=1)

tk.Label(root, text="Stop-Limit Price").grid(row=7, column=0, sticky="w", padx=10)
stop_limit_entry = tk.Entry(root, textvariable=limit_price_var)
stop_limit_entry.grid(row=7, column=1)

tk.Button(root, text="✅ Place Order", bg="green", fg="white", command=place_order)\
    .grid(row=8, column=0, columnspan=2, pady=10)

# OCO Inputs
tk.Label(root, text="OCO Take Profit").grid(row=9, column=0, sticky="w", padx=10)
tk.Entry(root, textvariable=tp_price_var).grid(row=9, column=1)

tk.Label(root, text="OCO Stop Price").grid(row=10, column=0, sticky="w", padx=10)
tk.Entry(root, textvariable=oco_stop_price_var).grid(row=10, column=1)

tk.Label(root, text="OCO Stop-Limit").grid(row=11, column=0, sticky="w", padx=10)
tk.Entry(root, textvariable=oco_stop_limit_var).grid(row=11, column=1)

tk.Button(root, text="🟡 Simulate OCO", command=simulate_oco)\
    .grid(row=12, column=0, columnspan=2, pady=10)

# Cancel / View
tk.Label(root, text="Cancel Order ID").grid(row=13, column=0, sticky="w", padx=10)
tk.Entry(root, textvariable=cancel_id_var).grid(row=13, column=1)

tk.Button(root, text="❌ Cancel Order", command=cancel_order).grid(row=14, column=0, columnspan=2)

tk.Button(root, text="📋 View Open Orders", command=view_open_orders).grid(row=15, column=0, columnspan=2, pady=10)

tk.Label(root, text="📜 Log Output").grid(row=16, column=0, columnspan=2)
output_box.grid(row=17, column=0, columnspan=2, padx=10, pady=10)

# ─── Run Setup ──────────────────────────────
update_fields()
apply_theme()
root.mainloop()
