import csv
from datetime import datetime
import os
from functools import wraps

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# --------------------------------------------------------------------------- #
# The Decorator is contained within the actual task-file instead
# of being imported to show it being used.
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

# Class LoanedBooks blueprint to easily work with the data from the CSV File.
class LoanedBooks:
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
        # Fornavn, Etternavn, Boktittel, Sjanger,
        # Lånedato, Låneperiode, Forlenget, Tilbakelevert
        try:
            return cls(
                data['Fornavn'], data['Etternavn'], data['Boktittel'],
                data['Sjanger'], data['Lånedato'], data['Tilbakelevert'],
                loan_period=data.get('Låneperiode', 14),
                extended=data.get('Forlenget', 0)
            ), None
        except ValueError as e:
            return None,f'Error on row: {data}, Error: {e}'

    @staticmethod
    def validate_name(name):
        if name.split().isalpha():
            return True

    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_int(nr_str):
        if nr_str.isdigit() or isinstance(nr_str, int):
            return True

    @staticmethod
    def validate_return(returned):
        if returned.lower() in ['ja', 'nei']:
            return True

    @staticmethod
    def validate_genre(genre):
        if genre.lower() in ['fiksjon', 'krim','sakprosa','fantasy']:
            return True


    def __str__(self):
        return f'{self.book_title} was loaned out to {self.first_name} {self.last_name} on date {self.loan_date}'

    def returned_on_time(self):
        if self.returned == 'Ja':
            return True

    def check_extension(self):
        return self.extended

    def get_title(self):
        return self.book_title

    def get_genre(self):
        return self.genre

    def get_loan_period(self):
        return self.loan_period + self.extended

    def get_full_name_loaner(self):
        return f'{self.first_name} {self.last_name}'


# --------------------------------------------------------------------------- #
# Function to create a list of objects (LoanedBooks) from the CSV file.
# It also creates a separate file called "errors_from_csv.txt"
@logging_current_task('"Reading file and creating list with objects"')
def create_class_list_from_csv(filename)-> list[LoanedBooks]:
    loaned_books_list_internal = []
    errors_from_csv = []
    error_file = 'errors_from_csv.txt'
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            bookloan, error = LoanedBooks.create_object_from_dict(row)
            if error:
                errors_from_csv.append(error)
            else:
                loaned_books_list_internal.append(bookloan)

    with open(error_file, 'w', encoding='utf-8') as error_writer:
        for error in errors_from_csv:
            error_writer.write(f'{error}\n')
    print(f'''Found [{len(errors_from_csv)}] rows with errors when creating objects with data from file [{filename}]
Row with data and error has been written to file [{error_file}]''')
    return loaned_books_list_internal

# --------------------------------------------------------------------------- #
# Oppgave 5A
@logging_current_task('5A')
def total_days_books_were_extended(loanedbooks_list):
    total_days = 0
    for book in loanedbooks_list:
        total_days += book.extended
    print(f'Total days all loaned out books were extended: {total_days}')


# --------------------------------------------------------------------------- #
# Oppgave 5B

@logging_current_task('5B')
def count_books_per_genra(loanedbooks_list):
    loaned_books_per_genra = {}
    for book in loanedbooks_list:
        if not book.returned_on_time():
            loaned_books_per_genra[book.genre] = loaned_books_per_genra.get(book.genre, 0) + 1
    print('Current amount of books loaned out per genre is: ')
    for genre, amount in loaned_books_per_genra.items():
        print(f'{genre}: {amount}')


# --------------------------------------------------------------------------- #
# Oppgave 5C

@logging_current_task('5C')
def get_average_loan_lenght(loanedbooks_list):
    total = 0
    for book in loanedbooks_list:
        total += book.get_loan_period()
    print(f'Average loan lenght: {total/len(loanedbooks_list):.2f} days')


# --------------------------------------------------------------------------- #
# Oppgave 5D

@logging_current_task('5D')
def count_books_not_returned_on_time(loanedbooks_list):
    currently_not_returned = []
    for book in loanedbooks_list:
        if not book.returned_on_time():
            currently_not_returned.append(f'Book: {book.book_title}, Loaner: {book.get_full_name_loaner()}')
    for i in currently_not_returned:
        print(i)
    return currently_not_returned


# --------------------------------------------------------------------------- #
# Oppgave 5E

@logging_current_task('5E')
def get_most_loaned_book(loanedbooks_list):
    total_loans_per_book = {}
    for book in loanedbooks_list:
        total_loans_per_book[book.book_title] = total_loans_per_book.get(book.book_title, 0) + 1
    sorted_books = sorted(total_loans_per_book.items(), key=lambda x: (-x[1], x[0].lower()))
    print(f'most loaned books:')
    for idx, book in enumerate(sorted_books):
        print(f'{idx+1}.\t"{book[0]}" | Amount: {book[1]}')


# --------------------------------------------------------------------------- #
# Main
def main():
    loaned_books_list = create_class_list_from_csv('bokutlån.csv')
    total_days_books_were_extended(loaned_books_list)
    count_books_per_genra(loaned_books_list)
    get_average_loan_lenght(loaned_books_list)
    not_returned_list = count_books_not_returned_on_time(loaned_books_list)
    get_most_loaned_book(loaned_books_list)

# --------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
