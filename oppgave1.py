from functools import wraps
# --------------------------------------------------------------------------- #
"""
A. Lag et program som ber brukeren om å skrive inn et positivt heltall (int) 
og finner summen av alle tall fra 1 til dette tallet 
(inkluder også tallet i summen). 
Summen skal beregnes ved hjelp av en for-løkke.

B. Skriv et program som ber brukeren skrive inn to setninger. 
    Programmet skal deretter sammenligne lengden på de to setningene 
    og skrive ut hvilken som er lengst og 
    antall karakterer det er i denne setningen.
    
C. Lag et program som ber brukeren skrive inn et tall 
og genererer multiplikasjonstabellen for dette tallet (fra 1 til 10). 
Eksempel:
    Input: 3
    Output:
    3 * 1
    3 * 2
    3 * 3
    Osv..
    
D. Lag et program som bytter plass på to elementer i en gitt liste. 
Programmet skal ta utgangspunkt i følgende liste:
    fruits = ["eple", "banan", "appelsin", "drue", "kiwi"]
    
    1. Be brukeren om å skrive inn to indekser (input) som angir 
    hvilke elementer i listen som skal bytte plass
    2. Bytt plass på elementene som ligger på de angitte indeksene
    3. Skriv ut den oppdaterte listen
        • Hvis en eller begge indeksene er ugyldige (ikke i listen), 
        skal programmet gi en passende feilmelding.
"""

# --------------------------------------------------------------------------- #
# Utility here:

# Decorator to log what task I'm working on.
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


# --------------------------------------------------------------------------- #
# Tasks 1A

@logging_current_task('1A')
def tasks_1a():
    """
    Sums all numbers from 1 to a user-provided positive integer.

    Prompts the user for a positive integer.
    Ensures the input is valid (positive integer greater than 1).
    It is locked from using negative numbers, as per the task description.

    Calculates the sum using a for loop and prints the result.
    """
    print('Summarising numbers from 1 to given number')
    try:
        sum_input = int(input('Wanted nr: '))
        if sum_input < 1:
            print('The number must bea positive integer: [number > 0]')
            return
        # Calculating sum with a for loop
        total_sum = 0
        for i in range(1, sum_input + 1):
            total_sum += i
        print(f'The sum of numbers from 1 to {sum_input} is {total_sum}')
    except ValueError:
        print('Invalid input. Not a valid positive integer.')


# A, looped but not for-loop
def sum_numbers_with_builtin():
    """
    This is the same as "tasks1_a" but done with builtin
    """
    sum_input = int(input('Write a positive integer: '))
    return sum(range(1, sum_input + 1))


# --------------------------------------------------------------------------- #
# Tasks 1B

# Class to work with the senteces for Task B
class Sentences:
    """
    A class to represent and compare sentences.

    Attributes:
        sentence (str): The sentence content.
        name (str): The name or identifier for the sentence.

    Methods:
        get_sentence_length():
            Returns the length of the sentence.
        compare_sentence_length(other):
            Compares the length of this sentence with another sentence and
            returns a message indicating which is longer or if they are equal.
    """
    def __init__(self, sentence, name):
        self.sentence = sentence
        self.name = name


    def __str__(self):
        return f"{self.name}: {self.sentence}"

    def get_sentence_length(self):
        return len(self.sentence)

    def compare_sentence_length(self, other):
        own_lenght = self.get_sentence_length()
        other_length = other.get_sentence_length()
        if own_lenght > other_length:
            return (f"{self.name} is the longest sentence "
                    f"and is made up of {own_lenght} characters")
        elif own_lenght < other_length:
            return (f"{other.name} is the longest sentence "
                    f"and is made up of {other_length} characters")
        else:
            return (f"{self.name} is the same as {other.name} "
                    f"and they are made up of {own_lenght} characters")


@logging_current_task('1B')
def tasks_1b():
    """
    Compares the length of two user-provided sentences.

    Prompts the user to input two sentences.
    Uses the Sentences class to compare their lengths.
    Prints which sentence is longer or if they are of equal length.
    """
    print('Compare the length of two sentences:')
    string_one = Sentences(input('Enter the first sentence: '),
                           'Sentence 1')
    string_two = Sentences(input('Sentence 2 for comparison: '),
                           'Sentence 2')
    print(string_one.compare_sentence_length(string_two))


# --------------------------------------------------------------------------- #
# Tasks 1C

@logging_current_task('1C')
def tasks_1c():
    """
    Generates a multiplication table for a user-provided number.

    The output format strictly follows the example given in the assignment:
        Input: 3
        Output:
        3 * 1
        3 * 2
        3 * 3
        ...
    Note: Hence, multiplication results are not included in the output.
    """
    try:
        number = int(input('Enter number for it\'s multiplication table: '))
        if number < 1:
            print('The number must be a positive integer.')
            return
        for i in range(1,11):
            print(f'{number} * {i}')
    except ValueError:
        print('Invalid input. Not a valid positive integer.')


# --------------------------------------------------------------------------- #
# Tasks 1D

@logging_current_task('1D')
def tasks_1d():
    """
    Swaps two elements in a predefined list of fruits based on
    user-provided indexes.

    Prompts the user to input two valid indexes.
    Validates the indexes to ensure they are within the list's range
    and not the same.
    Swaps the elements at the specified indexes and prints the updated list.
    Prints an error message if the indexes are invalid.
    """
    fruits = ['eple', 'banan', 'appelsin', 'drue', 'kiwi']
    print(f'The current list of fruits: {fruits}')
    print(f'Enter two indexes to swap [0 to {len(fruits) - 1}].')

    try:
        nr1 = int(input('Index 1: '))
        nr2 = int(input('Index 2: '))
        if nr1 == nr2:
            print('Can\'t swap the same indexes.')
            return
        fruits[nr1], fruits[nr2] = fruits[nr2], fruits[nr1]
        print(f'The updated list after swapping: {fruits}')

    except IndexError:
        print('One or more indexes are invalid.')
    except ValueError:
        print('Invalid input. Not an integer.')


# --------------------------------------------------------------------------- #
# Main function to run all my functions

def main():
    """
    It executes tasks A trough D in order.
    It also logs what task is being ran for the output.
    """
    tasks_1a()
    tasks_1b()
    tasks_1c()
    tasks_1d()


# --------------------------------------------------------------------------- #
if __name__ == '__main__':
    # Here the main program is being "executed"
    main()
