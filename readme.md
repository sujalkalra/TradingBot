# 📈 Binance Futures Testnet Trading Bot

This is a simplified CLI-based trading bot built using the Binance Futures **Testnet API**.  
Designed for internship task submission — clean, modular, and ready for extension.

---

## ✅ Features

- 🛒 Place **Market Orders**
- 📉 Place **Limit Orders**
- 🛑 Place **Stop-Limit Orders**
- 📋 View **Open Orders**
- ❌ Cancel Open Orders
- 🔁 CLI menu for interaction
- 🔒 .env for API key security
- 🪵 Logging all activity to `bot.log`

---

## 🛠️ Setup Instructions

### 1. 📦 Install dependencies

Make sure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

### 2. 🔐 Create a .env file

In the root directory of the project, create a file named `.env` and add your Binance Testnet API keys:

```ini
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
```

💡 **Don't use real keys.** Use https://testnet.binancefuture.com  
Go to Settings → API Key → Create Testnet Key

### 3. 🚀 Run the bot

```bash
python bot.py
```

---

## 🧪 Example Usage

```bash
==== Binance Futures Testnet Bot ====
1. Market order
2. Limit order
3. Stop-Limit order
4. View open orders
5. Cancel an order
6. Exit
Choose (1-6):
```

You'll be prompted step-by-step in the CLI to enter symbol, quantity, price, etc.

---

## 📁 Project Structure

```
binance-bot/
├── bot.py             # Main bot file (class-based)
├── .env               # Your API credentials (DO NOT SHARE)
├── bot.log            # Log of orders & errors
├── requirements.txt   # Python packages
└── README.md          # You're here
```

---

## 📘 Requirements

```text
python-binance
python-dotenv
```

Install using `pip install -r requirements.txt`

---

## 🎁 Bonus Features Implemented

✅ **Advanced Order:** Stop-Limit  
✅ **CLI Menu** with Looping UX  
✅ **Logging** with logging module  
✅ **Validation** for Binance's notional value limit  
✅ **OOP design** using a BasicBot class

---

## 📌 Notes

- This bot only works with **Binance Futures Testnet**.
- **Order minimum:** $100 notional value per Binance rules.
- All actions are logged to `bot.log`.

---

## 📫 Author

**Sujal Kalra**  
Python Developer | [LinkedIn/GitHub link if applicable]

---

## 🔐 Disclaimer

This project is for my knowledge purposes only. Never use real funds without proper testing and understanding of the risks.

---