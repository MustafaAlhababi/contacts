import json

class ContactManager:
    def __init__(self, filename):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as file:
                contacts = json.load(file)
            return contacts
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, contact_id=None, name=None, phone=None, email=None):
        if contact_id is None:
            contact_id = self.generate_unique_id()
        
        if self.is_id_unique(contact_id):
            if name is None:
                name = input("Name: ")
            if phone is None:
                phone = input("Phone number: ")
            if email is None:
                email = input("Email: ")

            contact = {
                'id': contact_id,
                'name': name,
                'phone': phone,
                'email': email
            }
            self.contacts.append(contact)
            self.save_contacts()
            print("Contact added successfully!")
        else:
            print("Error: This ID is already in use. Please use another ID.")

    def update_contact(self, contact_id, name, phone, email):
        for contact in self.contacts:
            if contact['id'] == contact_id:
                contact['name'] = name
                contact['phone'] = phone
                contact['email'] = email
                self.save_contacts()
                print("Contact updated successfully!")
                return
        print("Error: Contact not found.")

    def delete_contact(self, contact_id):
        self.contacts = [contact for contact in self.contacts if contact['id'] != contact_id]
        self.save_contacts()
        print("Contact deleted successfully!")

    def display_contacts(self):
        for contact in self.contacts:
            print(f"ID: {contact['id']}")
            print(f"Name: {contact['name']}")
            print(f"Phone number: {contact['phone']}")
            print(f"Email: {contact['email']}")
            print("-------------------------")

    def search_contact(self, keyword):
        results = []
        for contact in self.contacts:
            if (keyword.lower() in contact['name'].lower()) or (keyword in contact['phone']) or (keyword in contact['email']):
                results.append(contact)
        return results

    def is_id_unique(self, contact_id):
        return all(contact['id'] != contact_id for contact in self.contacts)

    def generate_unique_id(self):
        if not self.contacts:
            return 1
        else:
            max_id = max(contact['id'] for contact in self.contacts)
            return max_id + 1

if __name__ == "__main__":
    manager = ContactManager("contacts.json")

    while True:
        print("1. Add a contact")
        print("2. Update a contact")
        print("3. Delete a contact")
        print("4. Display contacts")
        print("5. Search contacts")
        print("6. Exit")

        choice = int(input("Please select an operation: "))

        if choice == 1:
            contact_id_input = input("If you want to manually enter an ID, leave it empty. Otherwise, enter the ID: ")
            if contact_id_input:
                contact_id = int(contact_id_input)
            else:
                contact_id = None
            manager.add_contact(contact_id)

        elif choice == 2:
            contact_id = int(input("ID: "))
            name = input("Name: ")
            phone = input("Phone number: ")
            email = input("Email: ")
            manager.update_contact(contact_id, name, phone, email)

        elif choice == 3:
            contact_id = int(input("ID: "))
            manager.delete_contact(contact_id)

        elif choice == 4:
            manager.display_contacts()

        elif choice == 5:
            keyword = input("Search keyword: ")
            results = manager.search_contact(keyword)
            if results:
                print("Search results:")
                for result in results:
                    print(f"ID: {result['id']}")
                    print(f"Name: {result['name']}")
                    print(f"Phone number: {result['phone']}")
                    print(f"Email: {result['email']}")
                    print("-------------------------")
            else:
                print("No results found.")

        elif choice == 6:
            print("Exiting the program")
            break