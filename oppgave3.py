from functools import wraps
from datetime import datetime

# --------------------------------------------------------------------------- #
"""
A. Lag en funksjon som tar inn en streng 
og sjekker om det er en gyldig IPv4-adresse. 
En gyldig IPv4-adresse har fire deler atskilt med punktum (.), 
der hver del er et heltall mellom 0 og 255. Funksjonen skal returnere 
True hvis det er en gyldig adresse, og False ellers.
Eksempel:
    Input: "192.168.1.1" → Output: True
    Input: "256.100.50.0" → Output: False
    
B. Lag en funksjon som tar inn to datoer som strenger 
på formatet ‘dd/mm/yyyy’ og returnerer antall dager mellom dem. 
Hvis den første datoen er senere enn den andre, 
skal funksjonen fortsatt returnere antall dager (positivt tall)
Eksempel:
    Input: "21/11/2024", "01/01/2024" → Output: 325 dager
    
C. I dataprogrammering brukes fargekoder ofte for å representere farger i
brukergrensesnitt og grafikk. To vanlige måter å representere farger på er:
    1. HEX-kode:
    En fargekode som starter med # og består av seks tegn som representerer 
    de røde, grønne og blå komponentene i fargen (for eksempel #CD5C5C). 
    Hver komponent har to tegn (heksadesimalt), hvor:
        • CD representerer rødt (r),
        • 5C representerer grønt (g), og
        • 5C representerer blått (b).
    2. RGB-kode:
    En fargekode representert som tre heltall, én for hver fargekomponent 
    (rød, grønn, blå). For eksempel: rgb(205, 92, 92).
    
Oppgave:
    Lag en funksjon ‘rgb_to_hex’ som tar inn tre heltall 
    (for eksempel red=205, green=92, blue=92) og returnerer 
    tilsvarende HEX-kode som en streng (for eksempel ‘#CD5C5C’).
    Legg også til passende feilmelding om 
    red, blue eller green parametere har ugyldig verdi.
"""

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
            return result
        return wrapper
    return decorator


# --------------------------------------------------------------------------- #
# Task 3 A
@logging_current_task('3A')
def task_3a(ip_str: str)->bool:
    """
    Validates if the input string is a valid IPv4 address.

    Args:
        ip_str (str): The input string.
    Returns:
        bool: True if the string is a valid IPv4 address, False otherwise.
    """
    separated_ip = ip_str.split('.')
    if len(separated_ip) != 4:
        return False
    for i in separated_ip:
        if not i.isdigit() or not 0 <= int(i) <=255:
            return False
    return True


# --------------------------------------------------------------------------- #
# Task 3B
@logging_current_task('3B')
def task_3b(date_1: str, date_2: str) -> str | None:
    """
    Calculates the number of days between two dates.

    Args:
        date_1 (str): First date in format 'dd/mm/yyyy'.
        date_2 (str): Second date in format 'dd/mm/yyyy'.
    Returns:
        str: The difference in days if valid data (abs)
        None: If any date is invalid.
    """
    try:
        date1 = datetime.strptime(date_1, '%d/%m/%Y')
        date2 = datetime.strptime(date_2, '%d/%m/%Y')
    except ValueError as e:
        print(f"Invalid format for date(s). Expected: [dd/mm/yyyy].")
        return None

    return f'{abs(date1 - date2).days} dager'


# --------------------------------------------------------------------------- #
# Task 3C
@logging_current_task('3C')
def rgb_to_hex(r: int, g: int, b: int) -> str | None:
    """
    Converts RGB values to a HEX color code.

    Args:
        r (int): Red (0-255).
        g (int): Green (0-255).
        b (int): Blue (0-255)
    Returns:
        str | None: HEX str if correct, or None if input
        values are out of range.
    """

    # Validates integer, attempts to cast if not.
    if not all(isinstance(i, int) for i in (r,g,b)):
        try:
            r,g,b = (int(i) for i in (r,g,b))
        except ValueError:
            print('Values are not integers.')
            return None

    # Validates value between 0-255 None if not
    if not all(0 <= colour <= 255 for colour in (r, g, b)):
        print('RGB numbers must be between 0-255')
        return None

    return f'#{r:02X}{g:02X}{b:02X}'


# --------------------------------------------------------------------------- #
# Main function because I included some prints to make it the output
# cleaner to look at.
def main():
    """
    Executes tasks 3A through 3C and prints results.
    """
    # Task 3A: Validate IPv4 addresses
    print(task_3a('255.200.1.1'))  # Valid
    print(task_3a('258.200.1.1'))  # Invalid
    print()

    # Task 3B: Calculate days between dates
    print(task_3b('30/04/1997', '12/01/1997'))  # Valid dates
    print(task_3b('09/12-2024', '08/12/2024'))  # Invalid date format
    print()

    # Task 3C: Convert RGB to HEX
    print(rgb_to_hex(205, 92, 92))  # Valid RGB
    print(rgb_to_hex(256, 92, 92))  # Invalid RGB


# --------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()