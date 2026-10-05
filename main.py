import functools
import json
from datetime import date, datetime


# =========================================================
# BOOK CLASSES
# =========================================================


class Book:

    GENRES = [
        "Fiction",
        "Mystery & Thriller",
        "Romance",
        "Science Fiction",
        "Fantasy",
        "Horror",
        "Historical Fiction",
        "Biography & Autobiography",
        "History",
        "Philosophy",
        "Psychology",
        "Religion & Spirituality",
        "Science",
        "Technology",
        "Business & Economics",
        "Politics & Society",
        "Self-Help",
        "Health & Fitness",
        "Travel",
        "Art & Design",
        "Poetry",
        "Drama",
        "Children's",
        "Education & Reference",
        "Other"
    ]

    def __init__(self, title, author, year, genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return (
            f"Title: {self.title} | "
            f"Author: {self.author} | "
            f"Year: {self.year} | "
            f"Genre: {self.genre}"
        )

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre
        }


class PrintedBook(Book):

    def __init__(self, title, author, year, genre, pages, status):
        super().__init__(title, author, year, genre)

        self.pages = pages
        self.status = status
        self.person = None
        self.borrowed_date = None

    def borrow_book(self, person, borrowed_date):
        self.status = "Borrowed Out"
        self.person = person
        self.borrowed_date = borrowed_date

    def return_book(self, status):
        self.status = status
        self.person = None
        self.borrowed_date = None

    def __str__(self):
        result = (
            f"{super().__str__()} | "
            f"Type: Printed Book | "
            f"Pages: {self.pages} | "
            f"Status: {self.status}"
        )

        if self.status == "Borrowed Out":
            result += (
                f" | Borrowed by: {self.person}"
                f" | Date: {self.borrowed_date}"
            )

        return result

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "pages": self.pages,
            "status": self.status,
            "person": self.person,
            "borrowed_date": self.borrowed_date
        })

        return data


class EBook(Book):

    def __init__(self, title, author, year, genre, pages, status):
        super().__init__(title, author, year, genre)

        self.pages = pages
        self.status = status

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Type: eBook | "
            f"Pages: {self.pages} | "
            f"Status: {self.status}"
        )

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "pages": self.pages,
            "status": self.status
        })

        return data


class AudioBook(Book):

    def __init__(
        self,
        title,
        author,
        year,
        genre,
        hours,
        minutes,
        status
    ):
        super().__init__(title, author, year, genre)

        self.hours = hours
        self.minutes = minutes
        self.status = status

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Type: AudioBook | "
            f"Duration: {self.hours}h {self.minutes}m | "
            f"Status: {self.status}"
        )

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "hours": self.hours,
            "minutes": self.minutes,
            "status": self.status
        })

        return data


# =========================================================
# DISPLAY
# =========================================================


def print_book_details(number, book):

    print(f"\n{number}. {book.title}")

    print(f"   Author: {book.author}")
    print(f"   Year: {book.year}")
    print(f"   Genre: {book.genre}")

    # Printed Book

    if isinstance(book, PrintedBook):

        print("   Type: Printed Book")
        print(f"   Pages: {book.pages}")
        print(f"   Status: {book.status}")

        if book.status == "Borrowed Out":

            print(
                f"   Borrowed by: {book.person}"
            )

            print(
                f"   Borrowed date: "
                f"{book.borrowed_date}"
            )

    # eBook

    elif isinstance(book, EBook):

        print("   Type: eBook")
        print(f"   Pages: {book.pages}")
        print(f"   Status: {book.status}")

    # AudioBook

    elif isinstance(book, AudioBook):

        print("   Type: AudioBook")

        print(
            f"   Duration: "
            f"{book.hours}h "
            f"{book.minutes}m"
        )

        print(f"   Status: {book.status}")


# =========================================================
# BOOK MANAGER
# =========================================================


class BookManager:

    def __init__(self):
        self.filename = "books.json"
        self.books = []

        self.load_books()

    # -----------------------------------------------------
    # ADD BOOK
    # -----------------------------------------------------

    def add_book(self, book):
        self.books.append(book)

        self.save_books()

        print(f'\n"{book.title}" was added successfully.')

    # -----------------------------------------------------
    # SAVE BOOKS TO JSON
    # -----------------------------------------------------

    def save_books(self):
        books_data = []

        for book in self.books:
            books_data.append(book.to_dict())

        with open(
            self.filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                books_data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------------------------------
    # LOAD BOOKS FROM JSON
    # -----------------------------------------------------

    def load_books(self):

        try:

            with open(
                self.filename,
                "r",
                encoding="utf-8"
            ) as file:

                books_data = json.load(file)

        except FileNotFoundError:
            return

        except json.JSONDecodeError:
            print(
                "Error: books.json contains invalid JSON."
            )
            return

        for data in books_data:

            book_type = data["type"]

            # Printed Book

            if book_type == "PrintedBook":

                book = PrintedBook(
                    data["title"],
                    data["author"],
                    data["year"],
                    data["genre"],
                    data["pages"],
                    data["status"]
                )

                if data["status"] == "Borrowed Out":

                    book.borrow_book(
                        data["person"],
                        data["borrowed_date"]
                    )

            # eBook

            elif book_type == "EBook":

                book = EBook(
                    data["title"],
                    data["author"],
                    data["year"],
                    data["genre"],
                    data["pages"],
                    data["status"]
                )

            # AudioBook

            elif book_type == "AudioBook":

                book = AudioBook(
                    data["title"],
                    data["author"],
                    data["year"],
                    data["genre"],
                    data["hours"],
                    data["minutes"],
                    data["status"]
                )

            else:
                continue

            self.books.append(book)

    # -----------------------------------------------------
    # SHOW ALL BOOKS
    # -----------------------------------------------------

    def show_books(self):

        if not self.books:
            print("\nNo books available.")
            return

        print("\n==============================")
        print("       PERSONAL LIBRARY")
        print("==============================")

        for number, book in enumerate(
            self.books,
            start=1
        ):

            print_book_details(number, book)

        print("\n==============================")

    # -----------------------------------------------------
    # SEARCH BOOK
    # -----------------------------------------------------

    def search_book(self, title):

        for book in self.books:

            if book.title.lower() == title.lower():
                return book

        return None

    # -----------------------------------------------------
    # SEARCH BOOKS BY AUTHOR
    # -----------------------------------------------------

    def search_by_author(self, author):

        found_books = []

        for book in self.books:

            if author.lower() in book.author.lower():
                found_books.append(book)

        return found_books

    # -----------------------------------------------------
    # GET LENT OUT BOOKS
    # -----------------------------------------------------

    def get_lent_out_books(self):

        lent_out_books = []

        for book in self.books:

            if (
                isinstance(book, PrintedBook)
                and book.status == "Borrowed Out"
            ):
                lent_out_books.append(book)

        # Oldest loans first

        lent_out_books.sort(
            key=lambda book: book.borrowed_date or ""
        )

        return lent_out_books

    # -----------------------------------------------------
    # LEND / RETURN BOOK
    # -----------------------------------------------------

    def lend_book(self, book, person, borrowed_date):

        book.borrow_book(
            person,
            borrowed_date
        )

        self.save_books()

    def return_book(self, book):

        book.return_book(
            "In Library"
        )

        self.save_books()


# =========================================================
# DECORATORS
# =========================================================


def retry_on_invalid(error_message):
    """
    Keep calling the decorated input function until it
    returns a value.

    - If the function raises ValueError (for example,
      int() on non-numeric input), error_message is shown.
    - If the function returns None, it already printed its
      own error, so we simply ask again.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            while True:

                try:

                    result = func(*args, **kwargs)

                    if result is not None:
                        return result

                except ValueError:

                    print(error_message)

        return wrapper

    return decorator


# =========================================================
# INPUT VALIDATION FUNCTIONS
# =========================================================


def get_valid_text(message):

    while True:

        value = input(message).strip()

        if value:
            return value

        print(
            "Error: This field cannot be empty."
        )


@retry_on_invalid("Error: Please enter a valid year.")
def get_valid_year():

    year = int(
        input("Enter publication year: ")
    )

    if year <= 0:

        print(
            "Error: Year must be greater than 0."
        )

        return None

    return year


@retry_on_invalid("Error: Please enter a valid number.")
def get_valid_pages():

    pages = int(
        input("Enter number of pages: ")
    )

    if pages <= 0:

        print(
            "Error: Number of pages "
            "must be greater than 0."
        )

        return None

    return pages


def get_genre():

    print("\n--- SELECT GENRE ---")

    for number, genre in enumerate(
        Book.GENRES,
        start=1
    ):

        print(f"{number}. {genre}")

    return choose_genre()


@retry_on_invalid("Error: Please enter a number.")
def choose_genre():

    choice = int(
        input("Choose genre: ")
    )

    if 1 <= choice <= len(Book.GENRES):

        return Book.GENRES[
            choice - 1
        ]

    print(
        "Error: Invalid genre."
    )

    return None


def get_status(printed=False):

    print("\n--- SELECT STATUS ---")

    print("1. Wish List")
    print("2. In Library")

    if printed:
        print("3. Borrowed Out")

    while True:

        choice = input(
            "Choose status: "
        ).strip()

        if choice == "1":

            return "Wish List"

        elif choice == "2":

            return "In Library"

        elif choice == "3" and printed:

            return "Borrowed Out"

        else:

            print(
                "Error: Invalid status."
            )


@retry_on_invalid("Error: Please enter valid numbers.")
def get_audio_duration():

    hours = int(
        input("Enter duration hours: ")
    )

    minutes = int(
        input("Enter duration minutes: ")
    )

    if hours < 0:

        print(
            "Error: Hours cannot be negative."
        )

        return None

    if minutes < 0 or minutes > 59:

        print(
            "Error: Minutes must be "
            "between 0 and 59."
        )

        return None

    if hours == 0 and minutes == 0:

        print(
            "Error: Duration must be "
            "greater than 0."
        )

        return None

    return hours, minutes


def get_valid_name(message):

    while True:

        value = input(message).strip()

        # Allow names like "Mary-Jane", "O'Brien" or "De Silva"

        letters_only = (
            value
            .replace("-", "")
            .replace("'", "")
            .replace(" ", "")
        )

        if letters_only.isalpha():
            return value

        print(
            "Error: Please enter a valid name "
            "(letters only)."
        )


@retry_on_invalid(
    "Error: Please enter a valid date "
    "in YYYY-MM-DD format."
)
def get_valid_date(message):

    value = input(message).strip()

    borrowed_date = datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()

    if borrowed_date > date.today():

        print(
            "Error: Date cannot be in the future."
        )

        return None

    return borrowed_date.isoformat()


def get_borrow_details():

    first_name = get_valid_name(
        "Enter borrower's first name: "
    )

    last_name = get_valid_name(
        "Enter borrower's surname: "
    )

    borrowed_date = get_valid_date(
        "Enter date lent out (YYYY-MM-DD): "
    )

    return (
        f"{first_name} {last_name}",
        borrowed_date
    )


# =========================================================
# ADD NEW BOOK
# =========================================================


def add_new_book(manager):

    print("\n--- ADD BOOK ---")

    print("1. Printed Book")
    print("2. eBook")
    print("3. AudioBook")
    print("0. Back")

    while True:

        book_type = input(
            "Choose book type: "
        ).strip()

        if book_type in [
            "0",
            "1",
            "2",
            "3"
        ]:
            break

        print(
            "Error: Please choose 0, 1, 2, or 3."
        )

    if book_type == "0":
        return

    # Basic information

    title = get_valid_text(
        "Enter book title: "
    )

    author = get_valid_text(
        "Enter author: "
    )

    year = get_valid_year()

    genre = get_genre()

    # -----------------------------------------------------
    # PRINTED BOOK
    # -----------------------------------------------------

    if book_type == "1":

        pages = get_valid_pages()

        status = get_status(
            printed=True
        )

        book = PrintedBook(
            title,
            author,
            year,
            genre,
            pages,
            status
        )

        if status == "Borrowed Out":

            person, borrowed_date = (
                get_borrow_details()
            )

            book.borrow_book(
                person,
                borrowed_date
            )

    # -----------------------------------------------------
    # EBOOK
    # -----------------------------------------------------

    elif book_type == "2":

        pages = get_valid_pages()

        status = get_status()

        book = EBook(
            title,
            author,
            year,
            genre,
            pages,
            status
        )

    # -----------------------------------------------------
    # AUDIOBOOK
    # -----------------------------------------------------

    else:

        hours, minutes = (
            get_audio_duration()
        )

        status = get_status()

        book = AudioBook(
            title,
            author,
            year,
            genre,
            hours,
            minutes,
            status
        )

    manager.add_book(book)


# =========================================================
# SEARCH BOOKS
# =========================================================


def search_books(manager):

    print("\n--- SEARCH BOOK ---")

    print("1. Search by Title")
    print("2. Search by Author")
    print("0. Back")

    while True:

        search_type = input(
            "Choose search type: "
        ).strip()

        if search_type in [
            "0",
            "1",
            "2"
        ]:
            break

        print(
            "Error: Please choose 0, 1, or 2."
        )

    if search_type == "0":
        return

    # -----------------------------------------------------
    # SEARCH BY TITLE
    # -----------------------------------------------------

    if search_type == "1":

        title = get_valid_text(
            "Enter book title: "
        )

        book = manager.search_book(
            title
        )

        if book:

            print("\nBook found:")
            print("==============================")

            print_book_details(1, book)

            print("\n==============================")

        else:

            print(
                "\nBook not found."
            )

    # -----------------------------------------------------
    # SEARCH BY AUTHOR
    # -----------------------------------------------------

    else:

        author = get_valid_text(
            "Enter author: "
        )

        found_books = manager.search_by_author(
            author
        )

        if found_books:

            print(
                f"\nFound {len(found_books)} "
                f"book(s) by \"{author}\":"
            )

            print("==============================")

            for number, book in enumerate(
                found_books,
                start=1
            ):

                print_book_details(number, book)

            print("\n==============================")

        else:

            print(
                "\nNo books found by "
                "that author."
            )


# =========================================================
# SHOW LENT OUT BOOKS
# =========================================================


def show_lent_out_books(manager):

    lent_out_books = manager.get_lent_out_books()

    if not lent_out_books:

        print(
            "\nNo books are lent out."
        )

        return

    print("\n==============================")
    print("       LENT OUT BOOKS")
    print("==============================")

    for number, book in enumerate(
        lent_out_books,
        start=1
    ):

        print(f"\n{number}. {book.title}")

        print(f"   Author: {book.author}")
        print(f"   Lent to: {book.person}")
        print(f"   Lent on: {book.borrowed_date}")

    print("\n==============================")

    print(
        f"Total lent out: {len(lent_out_books)}"
    )


# =========================================================
# LEND BOOK
# =========================================================


def lend_book(manager):

    print("\n--- LEND BOOK ---")

    title = get_valid_text(
        "Enter title of the book to lend: "
    )

    book = manager.search_book(
        title
    )

    if not book:

        print(
            "\nBook not found."
        )

        return

    # Only printed books that I own can be lent out

    if not isinstance(book, PrintedBook):

        print(
            "\nOnly printed books can be lent out."
        )

        return

    if book.status == "Wish List":

        print(
            f'\n"{book.title}" is on your wish list, '
            f"so it is not in your library yet."
        )

        return

    if book.status == "Borrowed Out":

        print(
            f'\n"{book.title}" is already lent to '
            f"{book.person} since {book.borrowed_date}."
        )

        return

    person, borrowed_date = (
        get_borrow_details()
    )

    manager.lend_book(
        book,
        person,
        borrowed_date
    )

    print(
        f'\n"{book.title}" was lent to {person} '
        f"on {borrowed_date}."
    )


# =========================================================
# RETURN BOOK
# =========================================================


def return_book(manager):

    print("\n--- RETURN BOOK ---")

    lent_out_books = manager.get_lent_out_books()

    if not lent_out_books:

        print(
            "\nNo books are lent out."
        )

        return

    for number, book in enumerate(
        lent_out_books,
        start=1
    ):

        print(
            f"{number}. {book.title} - "
            f"lent to {book.person} "
            f"on {book.borrowed_date}"
        )

    print("0. Back")

    choice = choose_book_number(
        len(lent_out_books)
    )

    if choice == 0:
        return

    book = lent_out_books[choice - 1]

    person = book.person

    manager.return_book(book)

    print(
        f'\n"{book.title}" was returned by '
        f"{person} and is back in your library."
    )


@retry_on_invalid("Error: Please enter a number.")
def choose_book_number(count):

    choice = int(
        input("Choose book: ")
    )

    if 0 <= choice <= count:
        return choice

    print(
        f"Error: Please choose a number "
        f"from 0 to {count}."
    )

    return None


# =========================================================
# EDIT BOOK
# =========================================================


def edit_book(manager):

    print("\n--- EDIT BOOK ---")

    title = get_valid_text(
        "Enter title of the book to edit: "
    )

    book = manager.search_book(
        title
    )

    if not book:

        print(
            "\nBook not found."
        )

        return

    is_audio = isinstance(book, AudioBook)

    while True:

        print("\nCurrent book:")
        print(book)

        print("\n--- WHAT DO YOU WANT TO EDIT? ---")

        print("1. Title")
        print("2. Author")
        print("3. Year")
        print("4. Genre")

        if is_audio:
            print("5. Duration")
        else:
            print("5. Pages")

        print("6. Status")
        print("0. Done")

        choice = input(
            "Choose field: "
        ).strip()

        if choice == "0":
            break

        elif choice == "1":

            book.title = get_valid_text(
                "Enter new title: "
            )

        elif choice == "2":

            book.author = get_valid_text(
                "Enter new author: "
            )

        elif choice == "3":

            book.year = get_valid_year()

        elif choice == "4":

            book.genre = get_genre()

        elif choice == "5" and is_audio:

            book.hours, book.minutes = (
                get_audio_duration()
            )

        elif choice == "5":

            book.pages = get_valid_pages()

        elif choice == "6":

            edit_status(book)

        else:

            print(
                "Error: Please choose "
                "0, 1, 2, 3, 4, 5, or 6."
            )

    manager.save_books()

    print(
        f'\n"{book.title}" was updated successfully.'
    )


def edit_status(book):

    # Only printed books can be borrowed out

    if not isinstance(book, PrintedBook):

        book.status = get_status()

        return

    status = get_status(
        printed=True
    )

    if status == "Borrowed Out":

        person, borrowed_date = (
            get_borrow_details()
        )

        book.borrow_book(
            person,
            borrowed_date
        )

    else:

        book.return_book(
            status
        )


# =========================================================
# MAIN PROGRAM
# =========================================================


def main():

    manager = BookManager()

    while True:

        print("\n==============================")
        print("       PERSONAL LIBRARY")
        print("==============================")

        print("1. Search Book")
        print("2. Show All Books")
        print("3. Add Book")
        print("4. Edit Book")
        print("5. Show Lent Out Books")
        print("6. Lend Book")
        print("7. Return Book")
        print("0. Exit")

        choice = input(
            "Choose an option: "
        ).strip()

        # Search Book

        if choice == "1":

            search_books(manager)

        # Show All Books

        elif choice == "2":

            manager.show_books()

        # Add Book

        elif choice == "3":

            add_new_book(manager)

        # Edit Book

        elif choice == "4":

            edit_book(manager)

        # Show Lent Out Books

        elif choice == "5":

            show_lent_out_books(manager)

        # Lend Book

        elif choice == "6":

            lend_book(manager)

        # Return Book

        elif choice == "7":

            return_book(manager)

        # Exit

        elif choice == "0":

            print("\nGoodbye!")

            break

        # Invalid menu option

        else:

            print(
                "Error: Invalid option. "
                "Please choose a number from 0 to 7."
            )




if __name__ == "__main__":
    main()