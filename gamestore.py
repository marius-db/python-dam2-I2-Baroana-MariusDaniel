# Dictionary to store our inventory items
# Each item maps to a dict with: price (sale price), stock (quantity on hand),
# cost (how much we paid per unit), provider (who supplied it)
inventory = {
    # A themed initial selection (games, consoles, merch, figures)
    'Gawr Gura Plushie (Small)': {'price': 24.99, 'stock': 10, 'cost': 8.00, 'provider': 'Hololive Merch Hub'},
    'Hololive Tee - Gura': {'price': 29.99, 'stock': 6, 'cost': 12.00, 'provider': 'Hololive Merch Hub'},
    'Megumin Figure - GSC Exclusive': {'price': 89.99, 'stock': 3, 'cost': 45.00, 'provider': 'GoodSmileCo'},
    'Chibi Amiibo Set': {'price': 14.99, 'stock': 12, 'cost': 4.50, 'provider': 'GoodSmileCo'},
    'Indie Pixel Adventure': {'price': 19.99, 'stock': 14, 'cost': 6.00, 'provider': 'IndieSupply'},
    'OmegaStation X Pro': {'price': 449.99, 'stock': 1, 'cost': 260.00, 'provider': 'ConsoleCorp'},
    'RetroBox Mini Classic': {'price': 79.99, 'stock': 5, 'cost': 42.00, 'provider': 'RetroWorks'},
    'Pikachu Cushion': {'price': 21.99, 'stock': 8, 'cost': 7.00, 'provider': 'KawaiiGoods'},
    'Dragon King Statue': {'price': 129.99, 'stock': 2, 'cost': 60.00, 'provider': 'FigurineWorld'},
    'Pro Controller - Carbon': {'price': 54.99, 'stock': 9, 'cost': 22.00, 'provider': 'ConsoleCorp'}
}

# Player/store money (cash on hand). We start with some capital to buy from providers.
store_money = 2000.00

def clear_screen():
    """Clears the console screen"""
    print("\n" * 50)

def pause():
    """Pause until user presses Enter so outputs stay visible before menu redraw."""
    try:
        input("\nPress Enter to return to the main menu...")
    except Exception:
        pass

def show_welcome():
    """Display a simple ASCII welcome and wait for Enter."""
    art = r"""
  ____                        _____ _                      _           _  _
 / ___| __ _ _ __ ___   ___  |  ___| | __ _ _ __ ___   ___| |__   __ _| || |
| |  _ / _` | '_ ` _ \ / _ \ | |_  | |/ _` | '_ ` _ \ / _ \ '_ \ / _` | || |_
| |_| | (_| | | | | | |  __/ |  _| | | (_| | | | | | |  __/ | | | (_| |__   _|
 \____|\__,_|_| |_| |_|\___| |_|   |_|\__,_|_| |_| |_|\___|_| |_|\__,_|  |_|

            Welcome to GameStore simulator
"""
    print(art)
    try:
        input('Press Enter to continue...')
    except Exception:
        pass

def get_valid_number(prompt, is_integer=False):
    """Helper function to get valid numeric input from user
    Args:
        prompt (str): Message to show user
        is_integer (bool): Whether the number should be an integer
    Returns:
        float/int: Valid number entered by user
    """
    while True:
        try:
            num = input(prompt)
            if is_integer:
                num = int(num)
            else:
                num = float(num)
            if num < 0:
                print("Please enter a positive number!")
                continue
            return num
        except ValueError:
            print("Please enter a valid number!")

def add_item():
    """Deprecated: direct adding by user is not allowed anymore.

    New items can only be added by buying from providers. Keep this function
    for backward compatibility but show a message to the user.
    """
    print("\nDirect item creation is disabled. Buy from providers to add new items.")
    pause()

def modify_item():
    """Modify an existing item in the inventory"""
    try:
        print("\n=== Modify Item ===")
        name = input("Enter the name of the item to modify: ").strip()

        if name not in inventory:
            print("Item not found in inventory!")
            return

        # Show current details and provider
        print("\nCurrent item details:")
        print(f"Name: {name}")
        print(f"Price: ${inventory[name]['price']:.2f}")
        print(f"Stock: {inventory[name]['stock']}")
        print(f"Provider: {inventory[name].get('provider', 'Unknown')}")

        # The user is allowed only to change price and stock (not the name).
        print("\nWhat would you like to modify?")
        print("1. Price")
        print("2. Stock")

        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            new_price = get_valid_number("Enter new price: $")
            inventory[name]['price'] = new_price
            print("Price updated successfully!")
            pause()

        elif choice == '2':
            new_stock = get_valid_number("Enter new stock quantity: ", True)
            inventory[name]['stock'] = new_stock
            print("Stock updated successfully!")
            pause()

        else:
            print("Invalid choice!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pause()

def remove_item():
    """Remove an item from the inventory"""
    try:
        print("\n=== Remove Item ===")
        name = input("Enter the name of the item to remove: ").strip()
        
        if name not in inventory:
            print("Item not found in inventory!")
            return
            
        print(f"\nCurrent item details:")
        print(f"Name: {name}")
        print(f"Price: ${inventory[name]['price']:.2f}")
        print(f"Stock: {inventory[name]['stock']}")
        
        confirm = input("\nAre you sure you want to remove this item? (yes/no): ").lower()
        if confirm == 'yes':
            del inventory[name]
            print("Item removed successfully!")
        else:
            print("Operation cancelled.")
            pause()
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pause()

def calculate_inventory_value():
    """Calculate and display the total value of inventory"""
    try:
        total_value = 0
        total_cost = 0
        # Sum sale value and total cost invested in inventory
        for item, details in inventory.items():
            item_value = details['price'] * details['stock']
            total_value += item_value
            # cost may not exist for very old entries, default to 0
            item_cost = details.get('cost', 0) * details['stock']
            total_cost += item_cost
        print(f"\nTotal inventory sale value: ${total_value:.2f}")
        print(f"Total inventory cost (what you paid): ${total_cost:.2f}")
        pause()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pause()

def find_most_expensive():
    """Find and display the most expensive item"""
    try:
        if not inventory:
            print("\nInventory is empty!")
            return
            
        most_expensive = max(inventory.items(), key=lambda x: x[1]['price'])
        print(f"\nMost expensive item:")
        print(f"Name: {most_expensive[0]}")
        print(f"Price: ${most_expensive[1]['price']:.2f}")
        print(f"Stock: {most_expensive[1]['stock']}")
        print(f"Provider: {most_expensive[1].get('provider','Unknown')}")
        pause()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pause()

def calculate_average_price():
    """Calculate and display the average price of items"""
    try:
        if not inventory:
            print("\nInventory is empty!")
            return
            
        total_price = 0
        total_items = 0
        # Average per *item type* (not weighted by stock)
        for item in inventory.values():
            total_price += item['price']
            total_items += 1

        average = total_price / total_items
        print(f"\nAverage price per product type: ${average:.2f}")

        # Also provide weighted average by stock
        total_price_stock = 0
        total_stock = 0
        for item in inventory.values():
            total_price_stock += item['price'] * item['stock']
            total_stock += item['stock']
        if total_stock > 0:
            weighted = total_price_stock / total_stock
            print(f"Weighted average price (by stock): ${weighted:.2f}")
        pause()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# ---------------- Providers and buying logic ----------------
# Providers are sources where we can buy stock to add to our store.
# Each provider has items available with a cost and available quantity.
providers = {
    # New set of providers with expanded catalogs (up to 10 items each)
    'Hololive Merch Hub': {
        'Gawr Gura Plushie (Small)': {'cost': 8.00, 'available': 50},
        'Hololive Tee - Gura': {'cost': 12.00, 'available': 30},
        'Gura Keychain': {'cost': 3.00, 'available': 100},
        'Gura Acrylic Stand': {'cost': 6.00, 'available': 40},
        'Gura Poster A2': {'cost': 4.00, 'available': 60},
        'Gura Hoodie': {'cost': 20.00, 'available': 15},
        'Gura Cap': {'cost': 7.00, 'available': 20},
        'Gura Socks': {'cost': 2.50, 'available': 50},
        'Hololive Collab Sticker Set': {'cost': 1.20, 'available': 200},
        'Gura Plushie (Large)': {'cost': 14.00, 'available': 10}
    },
    'GoodSmileCo': {
        'Megumin Figure - GSC': {'cost': 45.00, 'available': 20},
        'Chibi Amiibo Set': {'cost': 4.50, 'available': 60},
        'Figma Action Figure': {'cost': 30.00, 'available': 25},
        'Nendoroid Mystery': {'cost': 22.00, 'available': 18},
        'Scale Figure 1/7': {'cost': 55.00, 'available': 12},
        'GSC Poster Pack': {'cost': 3.50, 'available': 80},
        'Collectible Stand': {'cost': 6.00, 'available': 40},
        'Limited Edition Box': {'cost': 70.00, 'available': 6},
        'Character Badge Set': {'cost': 2.00, 'available': 120},
        'Mini Diorama Kit': {'cost': 9.00, 'available': 30}
    },
    'ConsoleCorp': {
        'OmegaStation X Pro': {'cost': 260.00, 'available': 5},
        'Pro Controller - Carbon': {'cost': 22.00, 'available': 40},
        'Console Carrying Case': {'cost': 12.00, 'available': 50},
        'HDMI Elite Cable': {'cost': 5.00, 'available': 80},
        'Charging Dock': {'cost': 9.00, 'available': 45},
        'Console Skin - Blue': {'cost': 3.00, 'available': 100},
        'Exclusive Bundle Pack': {'cost': 95.00, 'available': 10},
        'Retro Adapter': {'cost': 7.00, 'available': 35},
        'Controller Thumb Grips': {'cost': 1.50, 'available': 200},
        'Console Stand': {'cost': 8.00, 'available': 25}
    },
    'IndieSupply': {
        'Indie Pixel Adventure': {'cost': 6.00, 'available': 60},
        'Indie Sticker Pack': {'cost': 1.50, 'available': 150},
        'Soundtrack Digital Code': {'cost': 2.00, 'available': 200},
        'Artbook Mini': {'cost': 4.00, 'available': 40},
        'Collector Card': {'cost': 0.80, 'available': 300},
        'Indie Poster (Signed)': {'cost': 7.00, 'available': 20},
        'Limited Demo Cartridge': {'cost': 10.00, 'available': 15},
        'Developer Sticker Set': {'cost': 1.20, 'available': 120},
        'Game Jam Tee': {'cost': 8.00, 'available': 30},
        'Indie Soundtrack Vinyl': {'cost': 9.00, 'available': 25}
    },
    'KawaiiGoods': {
        'Pikachu Cushion': {'cost': 7.00, 'available': 40},
        'Pikachu Mug': {'cost': 3.50, 'available': 60},
        'Cute Plush Bundle': {'cost': 10.00, 'available': 30},
        'Anime Socks Pack': {'cost': 2.00, 'available': 100},
        'Chibi Backpack': {'cost': 15.00, 'available': 20},
        'Cute Phone Charm': {'cost': 1.20, 'available': 200},
        'Kawaii Keycap Set': {'cost': 5.00, 'available': 25},
        'Sticker Mega Pack': {'cost': 2.50, 'available': 120},
        'Plush Repair Kit': {'cost': 1.00, 'available': 80},
        'Desk Mat - Cute': {'cost': 6.50, 'available': 18}
    }
}

def show_providers():
    """Display providers and their items."""
    try:
        print("\n=== Providers ===")
        for pname, items in providers.items():
            print(f"\nProvider: {pname}")
            for iname, details in items.items():
                print(f" - {iname}: cost ${details['cost']:.2f}, available {details['available']}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    pause()

def buy_from_provider():
    """Buy stock from a provider. New products can only be added through this flow."""
    global store_money
    try:
        print("\n=== Buy from Provider ===")
        # List providers
        plist = list(providers.keys())
        for i, pname in enumerate(plist, 1):
            print(f"{i}. {pname}")
        choice = input("Select a provider by number (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            print("Cancelled.")
            pause()
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(plist):
            print("Invalid provider choice!")
            return
        provider_name = plist[int(choice)-1]
        # Show items from provider
        items = providers[provider_name]
        print(f"\nItems from {provider_name}:")
        item_list = list(items.keys())
        for i, iname in enumerate(item_list, 1):
            d = items[iname]
            print(f"{i}. {iname} - cost ${d['cost']:.2f}, available {d['available']}")

        ichoice = input("Select item by number (or 'c' to cancel): ").strip()
        if ichoice.lower() == 'c':
            print("Cancelled.")
            pause()
            return
        if not ichoice.isdigit() or int(ichoice) < 1 or int(ichoice) > len(item_list):
            print("Invalid item choice!")
            return
        item_name = item_list[int(ichoice)-1]
        available = items[item_name]['available']
        cost = items[item_name]['cost']

        print(f"\nSelected: {item_name} from {provider_name} - cost ${cost:.2f}, available {available}")
        qty = get_valid_number("Enter quantity to buy: ", True)
        if qty > available:
            print("Provider doesn't have that many available!")
            pause()
            return
        total_cost = cost * qty
        print(f"Total cost will be: ${total_cost:.2f}")
        print(f"Store money available: ${store_money:.2f}")
        confirm = input("Proceed with purchase? (yes/no): ").lower()
        if confirm != 'yes':
            print("Purchase cancelled.")
            pause()
            return
        if total_cost > store_money:
            print("Not enough money to complete purchase!")
            pause()
            return

        # Deduct money, reduce provider stock
        store_money -= total_cost
        providers[provider_name][item_name]['available'] -= qty

        # If item exists in inventory, just increase stock and update cost (simple average)
        if item_name in inventory:
            # Update average cost per unit (weighted)
            old_stock = inventory[item_name].get('stock', 0)
            old_cost = inventory[item_name].get('cost', 0)
            if old_stock + qty > 0:
                new_cost = ((old_cost * old_stock) + (cost * qty)) / (old_stock + qty)
            else:
                new_cost = cost
            inventory[item_name]['stock'] = old_stock + qty
            inventory[item_name]['cost'] = new_cost
            # Keep sale price as-is; user can modify price later
            print(f"Bought {qty} of existing item '{item_name}'. Stock now {inventory[item_name]['stock']}")
            pause()
        else:
            # New item — add to inventory with provider and cost
            # Default sale price is cost * 2 (simple markup), user can modify later
            sale_price = round(cost * 2, 2)
            inventory[item_name] = {'price': sale_price, 'stock': qty, 'cost': cost, 'provider': provider_name}
            print(f"Bought new item '{item_name}' and added to inventory with price ${sale_price:.2f}")
            pause()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# ---------------- Sales simulation ----------------
def simulate_day_sales():
    """Simulate a day of sales.

    This uses a simple approach: for each product we simulate a small chance of selling
    0..some units (bounded by stock). We calculate revenue, cost of goods sold, and profit.
    """
    global store_money
    try:
        if not inventory:
            print("No inventory to simulate sales.")
            return

        print("\n=== Simulate Day of Sales ===")
        # Ask for a simple aggressiveness factor to control how busy the day is
        factor = get_valid_number("Enter day demand factor (0.0 - quiet, 1.0 - normal, 2.0 - busy): ")
        if factor < 0:
            print("Factor cannot be negative. Using 1.0")
            factor = 1.0

        total_revenue = 0
        total_cogs = 0
        total_items_sold = 0
        sales_details = []

        # Iterate through inventory and simulate sales for each item
        for name, details in inventory.items():
            # Simple rule: expected sales = min(stock, round(factor * (stock * 0.2)))
            stock = details['stock']
            if stock <= 0:
                continue
            expected = int(round(factor * (stock * 0.2)))
            # We'll simulate actually sold between 0 and expected
            # Because we can't import random, we use a deterministic simple pseudo-random:
            # Use the length of the name and price to vary outcomes.
            pseudo = (len(name) + int(details['price'])) % (expected + 1) if expected > 0 else 0
            sold = pseudo
            if sold > stock:
                sold = stock

            revenue = sold * details['price']
            cogs = sold * details.get('cost', 0)
            total_revenue += revenue
            total_cogs += cogs
            total_items_sold += sold
            # reduce stock
            inventory[name]['stock'] = stock - sold
            sales_details.append((name, sold, revenue, cogs))

        profit = total_revenue - total_cogs
        store_money += profit

        # Show summary
        print(f"\nDay sales summary:")
        print(f"Total items sold: {total_items_sold}")
        print(f"Total revenue: ${total_revenue:.2f}")
        print(f"Total cost of goods sold: ${total_cogs:.2f}")
        print(f"Profit (revenue - COGS): ${profit:.2f}")
        print(f"Store money after sales: ${store_money:.2f}")

        print("\nDetailed sales per item:")
        for name, sold, revenue, cogs in sales_details:
            print(f" - {name}: sold {sold}, revenue ${revenue:.2f}, cogs ${cogs:.2f}")
        pause()

    except Exception as e:
        print(f"An error occurred during sales simulation: {str(e)}")

def display_inventory():
    """Display all items in the inventory"""
    try:
        if not inventory:
            print("\nInventory is empty!")
            return
            
        print("\n=== Current Inventory ===")
        for item, details in inventory.items():
            print(f"\nName: {item}")
            print(f"Price: ${details['price']:.2f}")
            print(f"Stock: {details['stock']}")
            print("-" * 20)
        pause()
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    """Main program loop"""
    while True:
        try:
            print("\n=== Game Store Inventory Management ===")
            print("1. Add new item (disabled - buy from providers)")
            print("2. Modify item (price/stock)")
            print("3. Remove item")
            print("4. Display inventory")
            print("5. Calculate total inventory value")
            print("6. Find most expensive item")
            print("7. Calculate average price")
            print("8. Show providers and their catalog")
            print("9. Buy from provider")
            print("10. Simulate a day of sales")
            print("11. Show store money")
            print("0. Exit")

            choice = input("\nEnter your choice (number): ")
            
            clear_screen()
            
            if choice == '1':
                add_item()
            elif choice == '2':
                modify_item()
            elif choice == '3':
                remove_item()
            elif choice == '4':
                display_inventory()
            elif choice == '5':
                calculate_inventory_value()
            elif choice == '6':
                find_most_expensive()
            elif choice == '7':
                calculate_average_price()
            elif choice == '8':
                show_providers()
            elif choice == '9':
                buy_from_provider()
            elif choice == '10':
                simulate_day_sales()
            elif choice == '11':
                print(f"\nStore money: ${store_money:.2f}")
                pause()
            elif choice == '0':
                print("Thank you for using the Game Store Inventory Management System!")
                break
            else:
                print("Invalid choice! Please try again.")
                
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    # Show welcome screen first, then enter main loop
    try:
        show_welcome()
    except Exception:
        pass
    main()
