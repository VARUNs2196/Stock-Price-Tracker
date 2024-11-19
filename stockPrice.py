import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from bse import BSE  # Importing the BSE library

class StockTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Price Tracker")
        self.master.geometry("800x600")  # Set window size

        # Load background image
        self.bg_image = tk.PhotoImage(file=r'C:/Users/VARUN/Desktop/pooja/th.png')  # Update this path
        self.bg_image = self.bg_image.subsample(1,1)  # Resize image
        self.bg_label = tk.Label(master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

        # Create a variable for the exchange selection
        self.exchange_var = tk.StringVar(value='NSE')  # Default value

        # Create a label and entry for the stock ticker
        tk.Label(master, text="Enter Stock Ticker:", bg='lightblue', font=("Arial", 16, "bold")).pack(pady=5)
        self.stock_entry = tk.Entry(master, font=("Arial", 16, "bold"))
        self.stock_entry.pack(pady=5)

        # Create a dropdown for selecting the exchange
        tk.Label(master, text="Select Exchange:", bg='lightblue', font=("Arial", 16, "bold")).pack(pady=5)
        exchange_options = ['NSE', 'BSE']
        exchange_menu = tk.OptionMenu(master, self.exchange_var, *exchange_options)
        exchange_menu.pack(pady=5)

        # Create a button to fetch stock price directly
        fetch_price_button = tk.Button(master, text="Fetch Price", command=self.fetch_and_display_price, font=("Arial", 16, "bold"))
        fetch_price_button.pack(pady=5)

        # Label to display fetched price
        self.price_display_label = tk.Label(master, text="", font=("Arial", 16, "bold"), bg='lightblue')
        self.price_display_label.pack(pady=10)

        # Create a button to add stock to wishlist
        add_button = tk.Button(master, text="Add to Wishlist", command=self.add_to_wishlist, font=("Arial", 16, "bold"))
        add_button.pack(pady=5)

        # Frame to hold stock cards
        self.cards_frame = tk.Frame(master)
        self.cards_frame.pack(pady=10)

    def fetch_stock_price(self, ticker, exchange):
        if exchange == 'BSE':
            try:
                bse = BSE(download_folder='/path/to/your/download/folder')  # Update this path
                scrip_code = bse.getScripCode(ticker)  # Get BSE code for the stock name
                if scrip_code:
                    url = f"https://www.google.com/finance/quote/{scrip_code}:BOM"
                else:
                    return None
            except Exception as e:
                return None
        
        else:  # NSE
            url = f"https://www.google.com/finance/quote/{ticker}:NSE"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            class1 = "YMlKec fxKbKc"  # Class name for stock price
            stock_price = soup.find(class_=class1).get_text()
            return stock_price.strip()
        except Exception as e:
            return None

    def fetch_and_display_price(self):
        ticker = self.stock_entry.get().strip()
        exchange = self.exchange_var.get()
        
        if ticker:
            price = self.fetch_stock_price(ticker, exchange)
            if price:
                self.price_display_label.config(text=f"The current price of {ticker} ({exchange}) is: {price}")
            else:
                messagebox.showerror("Error", "Invalid Stock Ticker or unable to fetch price.")
    
    def add_to_wishlist(self):
        ticker = self.stock_entry.get().strip()
        exchange = self.exchange_var.get()
        
        if ticker:
            price = self.fetch_stock_price(ticker, exchange)
            if price:
                self.create_stock_card(ticker, price, exchange)
                self.stock_entry.delete(0, tk.END)  # Clear entry after adding
            else:
                messagebox.showerror("Error", "Invalid Stock Ticker or unable to fetch price.")
    
    def create_stock_card(self, ticker, price, exchange):
        card_frame = tk.Frame(self.cards_frame, relief=tk.RAISED, borderwidth=2)
        
        card_frame.pack(pady=5, padx=5, fill=tk.X)

        ticker_label = tk.Label(card_frame, text=f"{ticker} ({exchange})", font=("Arial", 18))
        ticker_label.pack(side=tk.LEFT, padx=10)

        price_label = tk.Label(card_frame, text=f"Price: {price}", font=("Arial", 18))
        price_label.pack(side=tk.LEFT, padx=10)

        remove_button = tk.Button(card_frame, text="Remove", command=lambda: self.remove_stock_card(card_frame), font=("Arial", 14))
        remove_button.pack(side=tk.RIGHT, padx=10)

    def remove_stock_card(self, card_frame):
        card_frame.destroy()

    def start_tracking(self):
        for card in self.cards_frame.winfo_children():
            ticker_label = card.winfo_children()[0].cget("text").split(" ")[0]  # Get ticker from label
            exchange_label = card.winfo_children()[0].cget("text").split("(")[-1][:-1]  # Get exchange from label
            price = self.fetch_stock_price(ticker_label, exchange_label)
            if price:
                card.winfo_children()[1].config(text=f"Price: {price}")

# Create the main window and start the application
root = tk.Tk()
app = StockTracker(root)

# Start tracking every 10 seconds (can be adjusted or called separately)
def update_prices():
    app.start_tracking()
    root.after(10000, update_prices)  # Fetch every 10 seconds

update_prices()  # Initial call to start fetching prices
root.mainloop()