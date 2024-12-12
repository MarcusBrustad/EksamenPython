import csv
from datetime import datetime
import os
from functools import wraps

os.chdir(os.path.dirname(os.path.realpath(__file__)))
# --------------------------------------------------------------------------- #

"""
Description of Rows: 
1. Fornavn: Fornavnet til personen som lånte boken.
2. Etternavn: Etternavnet til personen som lånte boken.
3. Boktittel: Navnet på boken som ble lånt.
4. Sjanger: Sjanger på boken som ble lånt (Fiksjon, Krim, Sakprosa, Fantasy).
5. Lånedato: Datoen boken ble lånt ut (format: dd/mm/yyyy).
6. Låneperiode: Antall dager boken er lånt for (standard: 14 dager).
7. Forlenget: Hvor mange ekstra dager lånet ble forlenget 
(kan være 0 hvis ingen forlengelse).
8. Tilbakelevert: En indikasjon på om boken ble levert tilbake i tide 
eller ikke (Ja eller Nei). 

!!!
### Clarification of Column 8 (Tilbakelevert)
Column 8, "Tilbakelevert," is difficult to interpret in the tasks because
it can be understood in two ways:
    - The book has not been handed in yet.
    - The book was not returned on time (but may have been returned later).

This makes it harder to decide the correct logic for some tasks. The
description says the column means "not on time," but it does not clearly
rule out the possibility that the book has been returned late.

For example, in the printout, there is a book loaned in 2023 marked as
"Nei" for "Tilbakelevert." This could mean the book has not been returned,
but it could also mean it was returned after the due date.

**Default Interpretation:**
As a general rule, the column will be treated as showing whether the book
was returned on time, as described in the exam text. If there is any
uncertainty, I will follow this interpretation and avoid using the column
in tasks where a different interpretation could change the results.

**Resolution:**
For each task where the column is important and needs to be interpreted, I
will explain how I use it to make sure the logic matches the task
description and avoids any confusion in the data.
!!!

Tasks: 
A. Finn den totale mengden med forlengelser:
Skriv et program som summerer opp antall dager lånene ble forlenget 
og skriv ut svaret.

B. Antall bøker i hver sjanger:
Lag en funksjon som beregner hvor mange bøker som er lånt ut per sjanger 
(f.eks. Fantasy: 3, Krim: 5, osv.) og skriv ut svaret.

C. Gjennomsnittlig låneperiode:
Beregn den gjennomsnittlige låneperioden i antall hele dager for alle bøker 
som er lånt ut, inkludert forlengelsene og skriv ut svaret.

D. Bøker ikke levert tilbake i tide:
Lag en funksjon som lister opp alle bøkene som ikke ble levert tilbake. 
Returner en liste med navnene på bøkene 
og hvem som lånte dem og skriv ut svaret.

E. Toppliste over lånte bøker:
Skriv en funksjon som finner hvilke bøker som har blitt lånt flest ganger. 
Funksjonen skal returnere en oversikt over boktitlene og antallet ganger 
de har blitt lånt ut. Hvis flere bøker har blitt lånt ut like mange ganger, 
skal de sorteres alfabetisk. Skriv ut svaret.
"""

# --------------------------------------------------------------------------- #
# The Decorator is contained within the actual task-file instead
# of being imported to show it being used for this task, and how.
# Decorator to log what task is currently running.
def logging_current_task(task_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'Now running task: {task_id}')
            result = func(*args, **kwargs)
            print()
            return result
        return wrapper
    return decorator


# Generator to read CSV file.
def read_csv_in_chunks(filename):
    """
    Yields rows from a CSV file as dictionaries.
    """
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            yield row


# Class LoanedBooks blueprint to easily work with the data from the CSV File.
class LoanedBooks:
    """
    Represents a loaned book with details about the loan.
    """

    valid_genres = {'fiksjon', 'krim', 'sakprosa', 'fantasy'}
    valid_returned_values = {'ja', 'nei'}

    def __init__(self, first_name, last_name, book_title, genre,
                 loan_date, returned, loan_period=14, extended=0):
        if not self.validate_date(loan_date):
            raise ValueError('Invalid date format for "Lånedato"')
        if not self.validate_int(loan_period):
            raise ValueError('"Låneperiode" must be an integer')
        if not self.validate_int(extended):
            raise ValueError('"Forlenget" must be an integer')
        if not self.validate_return(returned):
            raise ValueError('"Returned" must be in list: ["Ja","Nei"]')
        if not self.validate_genre(genre):
            raise ValueError('"Genre" must be in list: '
                             '["fiksjon", "krim", "sakprosa", "fantasy"]')

        self.first_name = first_name
        self.last_name = last_name
        self.book_title = book_title
        self.genre = genre
        self.loan_date = datetime.strptime(loan_date, '%d/%m/%Y')
        self.loan_period = int(loan_period)
        self.extended = int(extended)
        self.returned = returned

    @classmethod
    def create_object_from_dict(cls, data):
        """
        Creates a LoanedBooks object from a dictionary.

        # Fornavn, Etternavn, Boktittel, Sjanger,
        # Lånedato, Låneperiode, Forlenget, Tilbakelevert
        """
        try:
            return cls(
                data['Fornavn'], data['Etternavn'], data['Boktittel'],
                data['Sjanger'], data['Lånedato'], data['Tilbakelevert'],
                loan_period=data.get('Låneperiode', 14),
                extended=data.get('Forlenget', 0)
            ), None
        except ValueError as e:
            return None,f'Error on row: {data} | Error: {e}'

    @classmethod
    def validate_return(cls, returned):
        """
        Validates if the return status is valid.
        """
        return returned.lower() in cls.valid_returned_values

    @classmethod
    def validate_genre(cls, genre):
        """
        Validates if the genre is valid.
        """
        return genre.lower() in cls.valid_genres

    @staticmethod
    def validate_name(name):
        """
        Validates if the name contains only letters.
        """
        return name.isalpha()

    @staticmethod
    def validate_date(date_str):
        """
        Validates if a date is in 'dd/mm/yyyy' format.
        """
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_int(value):
        """
        Validates if a value is an integer.
        """
        if isinstance(value, int):
            return True
        try:
            value = int(value)
            return value >= 0
        except ValueError:
            return False


    def __str__(self):
        return (f'{self.book_title} was loaned out to '
                f'{self.first_name} {self.last_name} '
                f'on date {self.loan_date}')

    def returned_on_time(self):
        """
        Checks if the book was returned on time.
        """
        if self.returned.lower() == 'ja':
            return True
        return False

    def check_extension(self):
        """
        Returns the number of days the loan was extended.
        """
        return self.extended

    def get_title(self):
        """
        Returns the title of the book.
        """
        return self.book_title

    def get_genre(self):
        """
        Returns the genre of the book.
        """
        return self.genre

    def get_loan_period(self):
        """
        Returns the total loan period, including extensions.
        """
        return self.loan_period + self.extended

    def get_full_name_loaner(self):
        """
        Returns the full name of the loaner.
        """
        return f'{self.first_name} {self.last_name}'


# --------------------------------------------------------------------------- #
# Function to create a list of objects (LoanedBooks) from the CSV file.
# It also creates a separate file called "errors_from_csv.txt"
@logging_current_task('"Reading file and creating list with objects"')
def create_class_list_from_csv(filename)-> list[LoanedBooks]:
    """
    Creates a list of LoanedBooks from a CSV file and logs errors.
    """
    bookloans_list = []
    errors_from_csv = []
    error_file = 'errors_from_csv.txt'

    for row in read_csv_in_chunks(filename):
        bookloan, error = LoanedBooks.create_object_from_dict(row)
        if error:
            errors_from_csv.append(error)
        else:
            bookloans_list.append(bookloan)

    print(f'{len(bookloans_list)} entries were handled correctly')

    if errors_from_csv:
        with open(error_file, 'w', encoding='utf-8') as error_writer:
            for error in errors_from_csv:
                error_writer.write(f'{error}\n')
        print(f'Found {len(errors_from_csv)} Errors. Details in {error_file}')
    return bookloans_list

# --------------------------------------------------------------------------- #
# Oppgave 5A
@logging_current_task('5A')
def total_days_books_were_extended(loanedbooks_list):
    """
    Calculates total days all loans were extended.
    """
    total_days = 0
    for book in loanedbooks_list:
        total_days += book.extended
    print(f'Total days all loaned out books were extended: {total_days}')


# --------------------------------------------------------------------------- #
# Oppgave 5B

"""
'
B. Antall bøker i hver sjanger:
Lag en funksjon som beregner hvor mange bøker som er lånt ut per sjanger 
(f.eks. Fantasy: 3, Krim: 5, osv.) og skriv ut svaret.
'
In this task, column 8 ("Tilbakelevert") is interpreted as meaning the book
is currently not handed back. This allows the program to check which books
are not present at the library at the current time.

This interpretation better matches the example output provided in the exam.
"""
@logging_current_task('5B')
def count_books_per_genre(loanedbooks_list):
    """
    Counts books loaned out per genre.
    """
    loaned_books_per_genra = {}
    for book in loanedbooks_list:
        if not book.returned_on_time():
            loaned_books_per_genra[book.genre] = loaned_books_per_genra.get(
                book.genre, 0) + 1
    print('Current amount of books loaned out per genre is: ')
    for genre, amount in loaned_books_per_genra.items():
        print(f'{genre}: {amount}')


# --------------------------------------------------------------------------- #
# Oppgave 5C

@logging_current_task('5C')
def get_average_loan_length(loanedbooks_list):
    """
    Calculates the average loan length of all books from the CSV file.
    """
    total = 0
    for book in loanedbooks_list:
        total += book.get_loan_period()
    print(f'Average loan lenght: {total/len(loanedbooks_list):.2f} days')


# --------------------------------------------------------------------------- #
# Oppgave 5D

"""
D. Bøker ikke levert tilbake i tide:
Lag en funksjon som lister opp alle bøkene som ikke ble levert tilbake. 
Returner en liste med navnene på bøkene og hvem som lånte dem 
og skriv ut svaret.

In this task, column 8 ("Tilbakelevert") is interpreted as meaning the book
is currently not handed back. This lets the program focus on books that are
still not present in the library.

This approach aligns with the task description and example output by
identifying overdue books and borrowers.
"""
@logging_current_task('5D')
def count_books_not_returned_on_time(loanedbooks_list):
    """
    Lists books not returned on time with their loaners.
    """
    currently_not_returned = []
    for book in loanedbooks_list:
        if not book.returned_on_time():
            currently_not_returned.append(
                f'Book: {book.book_title},'
                f' Loaner: {book.get_full_name_loaner()}')
    for i in currently_not_returned:
        print(i)
    return currently_not_returned


# --------------------------------------------------------------------------- #
# Oppgave 5E

@logging_current_task('5E')
def get_most_loaned_book(loanedbooks_list):
    """
    Lists the most loaned books in descending order by number if there are
    more than 1 with the same amount it does it alphabeticly asc order.

    """
    total_loans_per_book = {}
    for book in loanedbooks_list:
        total_loans_per_book[book.book_title] = (total_loans_per_book.get
                                                 (book.book_title, 0) + 1)
    sorted_books = sorted(
        total_loans_per_book.items(), key=lambda x: (-x[1], x[0].lower())
    )
    print(f'most loaned books:')
    for idx, book in enumerate(sorted_books):
        print(f'{idx+1}.\t"{book[0]}" | Amount: {book[1]}')


# --------------------------------------------------------------------------- #
# Main
def main():
    """
    Executes all tasks for processing and analyzing loaned books.
    """

    loaned_books_list = create_class_list_from_csv('bokutlån.csv')
    if not loaned_books_list:
        print('No bookloans with valid data found. Exiting')
        return

    total_days_books_were_extended(loaned_books_list)
    count_books_per_genre(loaned_books_list)
    get_average_loan_length(loaned_books_list)
    not_returned_list = count_books_not_returned_on_time(loaned_books_list)
    get_most_loaned_book(loaned_books_list)

# --------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
