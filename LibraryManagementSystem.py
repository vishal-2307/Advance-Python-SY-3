class Book:
    # Changed from _init_ to __init__
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def display(self):
        status = "Available" if self.available else "Borrowed"
        print(f"Title: {self.title}, Author: {self.author}, Status: {status}")


class Patron:
    # Changed from _init_ to __init__
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def display(self):
        print(f"Patron: {self.name}")
        if self.borrowed_books:
            print("Borrowed Books:")
            for book in self.borrowed_books:
                print("-", book.title)
        else:
            print("No borrowed books.")


class Library:
    # Changed from _init_ to __init__
    def __init__(self):
        self.books = []
        self.patrons = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        print(f"Book '{title}' added successfully.")

    def register_patron(self, name):
        patron = Patron(name)
        self.patrons.append(patron)
        print(f"Patron '{name}' registered successfully.")

    def borrow_book(self, patron_name, book_title):
        patron = next((p for p in self.patrons if p.name == patron_name), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if patron and book:
            if book.available:
                book.available = False
                patron.borrowed_books.append(book)
                print(f"{patron_name} borrowed '{book_title}'.")
            else:
                print("Book is already borrowed.")
        else:
            print("Patron or Book not found.")

    def return_book(self, patron_name, book_title):
        patron = next((p for p in self.patrons if p.name == patron_name), None)

        if patron:
            for book in patron.borrowed_books:
                if book.title == book_title:
                    book.available = True
                    patron.borrowed_books.remove(book)
                    print(f"{patron_name} returned '{book_title}'.")
                    return
            print("Book not borrowed by the person.")
        else:
            print("Patron not found.")

    def show_books(self):
        print("\nLibrary Books:")
        for book in self.books:
            book.display()

    def show_patrons(self):
        print("\nRegistered Patrons:")
        for patron in self.patrons:
            patron.display()


# Driver Code
library = Library()

library.add_book("Atomic Habits", "James Clear")
library.add_book("The Power of Now", "Eckhart Tolle")
library.add_book("Tuesdays with Morrie", " Mitch Albom")

library.register_patron("Vishal")
library.register_patron("Chaitanya")

library.borrow_book("Vishal", "Atomic Habits")

library.show_books()
library.show_patrons()

library.return_book("Vishal", "Atomic Habits")
library.show_books()