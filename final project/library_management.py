from database import setup_database, add_material, add_user, checkout_item, return_item, search_materials, list_overdue_items

def print_menu():
    print("\nLibrary Management System Menu:")
    print("1 - Checkout an item")
    print("2 - Return an item")
    print("3 - Search for an item")
    print("4 - List overdue items")
    print("5 - Exit")

def main():
    setup_database()

    # Sample data for demonstration
    add_material("The Great Gatsby", "F. Scott Fitzgerald", "American Literature", "SN12345", "book")
    add_user("John Doe", "johndoe@example.com")

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            user_id = input("Enter user ID: ")
            material_id = input("Enter material ID: ")
            if checkout_item(int(user_id), int(material_id)):
                print("Checkout successful!")
            else:
                print("Checkout failed: Item might be unavailable or already checked out.")

        elif choice == '2':
            material_id = input("Enter material ID to return: ")
            return_item(int(material_id))
            print("Item returned successfully!")

        elif choice == '3':
            keyword = input("Enter search keyword (title, author, subject, or serial number): ")
            results = search_materials(keyword)
            if results:
                print("Search Results:")
                for item in results:
                    print(item)
            else:
                print("No items found matching the criteria.")

        elif choice == '4':
            overdue_items = list_overdue_items()
            if overdue_items:
                print("Overdue Items:")
                for item in overdue_items:
                    print(item)
            else:
                print("No overdue items.")

        elif choice == '5':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
