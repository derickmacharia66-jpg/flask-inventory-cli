import requests

BASE_URL = "http://127.0.0.1:5000"

def main():
    while True:
        print("\n--- Inventory Management CLI ---")
        print("1. View Inventory")
        print("2. Add Inventory Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Lookup Product from OpenFoodFacts (by Barcode)")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            res = requests.get(f"{BASE_URL}/inventory")
            print(res.json())
        elif choice == '2':
            name = input("Product Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            res = requests.post(f"{BASE_URL}/inventory", json={"product_name": name, "price": price, "stock": stock})
            print(res.json())
        elif choice == '3':
            item_id = input("Item ID to update: ")
            price = float(input("New Price: "))
            res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json={"price": price})
            print(res.json())
        elif choice == '4':
            item_id = input("Item ID to delete: ")
            res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
            print(res.json())
        elif choice == '5':
            barcode = input("Enter Barcode: ")
            res = requests.get(f"{BASE_URL}/external-product/{barcode}")
            print(res.json())
        elif choice == '6':
            break

if __name__ == '__main__':
    main()