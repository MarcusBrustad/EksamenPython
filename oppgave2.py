from datetime import datetime
from functools import wraps

# --------------------------------------------------------------------------- #
"""
Oppgave 2.
A. Skriv et program som leser inn en dato i formatet: 
    "dd/mm/yyyy" fra brukeren.
Programmet skal deretter sjekke om datoen er gyldig. 
Hvis datoen er ugyldig, skalprogrammet skrive en passende feilmelding.
B. Ta utgangspunkt i en liste der tekst og tall er plassert 
parvis med navn og alder slik:
    ["Cecilie", 28, "Bjørn", 30, "Tor", 24, "Anna", 25]
Skriv et program som splitter denne listen i to separert lister, 
en liste for navn og en liste for alder.
C. Ta utgangspunkt i listene fra oppgave B og lag en dictionary der 
tekstverdier fra listen med navn blir nøkler og 
tallverdiene fra listen med alder blir verdier. Skriv ut innholdet
av denne dictionary på formatet:
«Cecilie er 25 år»
«Bjørn er 30 år»
D. Skriv et program som:
1. Sorterer denne dictionary etter alder hvor den eldste skal være først. 
Skriv ut resultatet.
2. Sorterer denne dictionary etter alder hvor den eldste skal være først. 
Skriv ut resultatet.
E. Ta utgangspunktet i dictionary som er sortert på navn i oppgave 2D 
og lag en ny liste med disse verdiene slik at listen får samme format 
som den i oppgave 2B, men sortert på navn.
    ['Anna', 25, 'Bjørn', 30, 'Cecilie', 28, 'Tor', 24]
"""

# --------------------------------------------------------------------------- #
# Utility used for this task and subtasks

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


# --------------------------------------------------------------------------- #
# Task 2A

@logging_current_task('2A')
def task_2a() -> bool:
    """
    Validates a date input using the "datetime.strptime" function.
    """
    print('Please type in a date in the format "dd/mm/yyyy"')
    date_str = input("date: ")
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        print(f"{date_str} is a valid date.")
        return True
    except ValueError:
        print(f'Unvalid data for date given. '
              f'Expected format for date: [dd/mm/yyyy]')
        return False


# --------------------------------------------------------------------------- #
# Task 2B

@logging_current_task('2B')
def task_2b() -> tuple[list, list]:
    """
    Splits a list of alternating names and ages into two separate lists.

    Example:
        Input: ["Cecilie", 28, "Bjørn", 30]
        Output: (["Cecilie", "Bjørn"], [28, 30])
    Returns:
        name_list (list[str]): Names.
        age_list (list[int]): Ages.
    """

    name_age_list = ["Cecilie", 28, "Bjørn", 30, "Tor", 24, "Anna", 25]

    names_list: list[str] = [name for name in name_age_list
                             if isinstance(name, str)]
    ages_list: list[int] = [age for age in name_age_list
                            if isinstance(age, int)]

    print(f"The new lists are: '{names_list}' and '{ages_list}'")
    return names_list, ages_list


# --------------------------------------------------------------------------- #
# Task 2C

@logging_current_task('2C')
def task_2c(name_list: list[str], age_list: list[int]) -> dict:
    """
    Maps names to ages in a dictionary.

    Args:
        name_list (list[str]): Names.
        age_list (list[int]): Ages.
    Returns:
        dict: Name-age mapping.
    """
    name_age_dict = {name: age for name, age in zip(name_list, age_list)}

    for key, value in name_age_dict.items():
        print(f"{key} er {value} år")
    return name_age_dict


# --------------------------------------------------------------------------- #
# Task 2D
"""
'D. Skriv et program som:
1. Sorterer denne dictionary etter alder hvor den eldste skal være først. 
Skriv ut resultatet.
2. Sorterer denne dictionary etter alder hvor den eldste skal være først. 
Skriv ut resultatet.
E. Ta utgangspunktet i dictionary som er sortert på navn i oppgave 2D 
og lag en ny liste med disse verdiene slik at listen får samme format 
som den i oppgave 2B, men sortert på navn.
    ['Anna', 25, 'Bjørn', 30, 'Cecilie', 28, 'Tor', 24]'


!!! Reading this I interpret this as being a mistake in task D 
and thus locking me from completing task E. 
I will be sorting by "age" in D.1 and by "name" in D.2, 
allowing me to use this data for the followup part in task E !!! 
"""
@logging_current_task('2D')
def task_2d(name_age_dict: dict[str, int])-> (
        tuple)[dict[str, int],dict[str, int]]:
    """
    Sorts a dictionary of names and ages by age and name.

    This function sorts the input dictionary twice:
    1. By age in descending order.
    2. By name in ascending order.

    The sorted dictionaries are printed in a readable format and returned.
    Args:
        name_age_dict (dict[str, int]): Dictionary where keys are names
        and values are ages.

    Returns:
        tuple[dict[str, int], dict[str, int]]: A tuple containing:
            - The dictionary sorted by age in descending order.
            - The dictionary sorted by name in ascending order.
    """
    # D.1
    sorted_by_age = dict(
        sorted(name_age_dict.items(), key=lambda item: item[1], reverse=True)
    )
    # D.2
    sorted_by_name = dict(
        sorted(name_age_dict.items(), key=lambda item: item[0], reverse=False)
    )
    # print results
    print(f"Here is the name and ages of everyone sorted by "
          f"their age in descending order.")
    for key, value in sorted_by_age.items():
        print(f"{key} er {value} år")
    print()

    print("Here is the names and ages of everyone sorted by "
          "their name in ascending order.")
    for key, value in sorted_by_name.items():
        print(f"{key} er {value} år")

    return sorted_by_age, sorted_by_name


# --------------------------------------------------------------------------- #
# Task 2E
@logging_current_task
def task_2e(name_age_dict: dict) -> list:
    """
    Flattens a dictionary into a list sorted by name.

    Args:
        name_age_dict (dict): Dictionary of names and ages.
    """
    name_age_sorted_list = [
        name_or_age for key, value in name_age_dict.items()
        for name_or_age in (key, value)]

    print('Reconstructed list from task 2B, sorted by names:')
    print(name_age_sorted_list)


# --------------------------------------------------------------------------- #
# Main
def main() -> None:
    """
    It executes tasks A trough E in order.
    It also logs what task is being ran for the output.
    """
    task_2a()
    names, ages = task_2b()
    name_age_dictionary = task_2c(names, ages)
    age_sorted_dict, name_sorted_dict = task_2d(name_age_dictionary)
    task_2e(name_sorted_dict)


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()