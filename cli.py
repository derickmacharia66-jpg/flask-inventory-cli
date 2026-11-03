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
        print("6. Import Product from OpenFoodFacts into Inventory")
        print("7. Search Inventory")
        print("8. Low Stock Report")
        print("9. Inventory Summary")
        print("10. Exit")

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
            barcode = input("Enter Barcode: ")
            price = float(input("Price (OpenFoodFacts doesn't provide this): "))
            stock = int(input("Stock: "))
            res = requests.post(f"{BASE_URL}/external-product/{barcode}/import", json={"price": price, "stock": stock})
            print(res.json())
        elif choice == '7':
            q = input("Search term: ")
            res = requests.get(f"{BASE_URL}/inventory/search", params={"q": q})
            print(res.json())
        elif choice == '8':
            threshold = input("Threshold (default 10): ") or 10
            res = requests.get(f"{BASE_URL}/inventory/low-stock", params={"threshold": threshold})
            print(res.json())
        elif choice == '9':
            res = requests.get(f"{BASE_URL}/inventory/summary")
            print(res.json())
        elif choice == '10':
            break


if __name__ == '__main__':
    main()