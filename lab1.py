import re
import sys
import unidecode as ud

def open_file(filename):
    """
    Opens file and returns its content.
    Parameters:
        filename (string) - name of a file    
    Returns:
        (string) file content
    Raises:
        TypeError: filename is not a string
    """
    if type(filename) != str:
        raise TypeError

    with open(filename, 'r') as f:
        content = f.read()
     
    return content

def clean_text(plaintext, keep_spaces=False):
    """
    Depending on user decision of keeping whitespace:
    clears whitespace from file content
    or keeps whitespace in file content.
    Parameters:
        plaintext (string) - file content 
	    keep_spaces (bool) - if whitespace are kept     
    Returns:
        prodessed plaintext (string)
    Raises:
         TypeError: filename is not a string
    """
    if type(plaintext) != str:
        raise TypeError

    if keep_spaces:
        pattern = r'[^a-zA-Zą-źĄ-Ź0-9 ]+'
    else:
        pattern = r'[^a-zA-Zą-źĄ-Ź0-9]+'

    return re.sub(pattern, '', plaintext)

def clean_num(plaintext):
    """
    Clears numbers from file content
    Parameters:
         plaintext (string) - file content     
    Returns:
         prodessed plaintext (string)
    Raises:
        TypeError: filename is not a string
    """
    if type(plaintext) != str:
        raise TypeError

    return re.sub(r'[0-9]+', '', plaintext)

def clean_acc(plaintext, lower=True):
    """
    Depending on user decision of keeping uppercase letters:
    changes uppercase letters to lowercase letters in file content  
    or keeps uppercase letters in file content.
    Clears diacritics from file content    
    Parameters:
         plaintext (string) - file content 
	     lower (bool) - if uppercase letters are kept      
    Returns:
         prodessed plaintext (string)
    Raises:
         TypeError: filename is not a string
    """
    if type(plaintext) != str:
        raise TypeError
 
    if lower:
        plaintext = plaintext.lower()

    return ud.unidecode(plaintext)

def col_text(plaintext):
    """
    Puts file content gruped by 5 characters into 7 collumns.      
    Parameters:
        plaintext (string) - file content    
    Returns:
        text in collums     
    Raises:
        TypeError: plaintext is not a string        
    """
    if type(plaintext) != str:
        raise TypeError
    
    line_num = 0
    lines = []
    while line_num*35 < len(plaintext):
        line = plaintext[35*line_num:35*(line_num+1)]
        cols = [(line[5*col_num:len(line)], line[5*col_num:5*(col_num+1)])[(col_num + 1)*5 < len(line)] for col_num in range(7)]
        lines.append(' '.join(cols))
        line_num += 1
    return '\n'.join(lines)

def write_to_file(plaintext, filename):
    """
    Get file names and chosen options form the user. 
    Prints current operation.
    Handles previous functions. 
    Handles errors. 
    Saves processed text to file.
    
    Parameters:
        plaintext (string) - file content
        filename (string) - name of a file
    
    Raises:
        TypeError: filename/plaintext is not a string
    """
    if type(plaintext) != str or type(filename) != str:
        raise TypeError

    with open(filename, 'w') as f:
        f.write(plaintext)

input_file = ''
output_file = ''
remove_numbers = False
lower = False
keep_spaces = False

i = 0
while i < len(sys.argv):
    if sys.argv[i] == '-f' and i + 1 < len(sys.argv):
        input_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
        output_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '--remove_numbers':
        remove_numbers = True
    if sys.argv[i] == '--lower':
        lower = True
    if sys.argv[i] == '--keep_spaces':
        keep_spaces = True
    i += 1

done = False
while not done:
    try:
        print(f'Otwieranie pliku {input_file}... ', end='')
        plaintext = open_file(input_file)
        print('gotowe')

        print('Usuwanie białych znaków... ', end='')
        plaintext = clean_text(plaintext, keep_spaces)
        print('gotowe')

        if remove_numbers:
            print('Usuwanie cyfr... ', end='')
            plaintext = clean_num(plaintext)
            print('gotowe')

        print('Usuwanie znaków diakrytycznych... ', end='')
        plaintext = clean_acc(plaintext, lower)
        print('gotowe')

        print('Przekształcanie na kolumny... ', end='')
        plaintext = col_text(plaintext)
        print('gotowe')

        print(f'Zapis wyniku do pliku {output_file}... ', end='')
        write_to_file(plaintext, output_file)
        print('gotowe')

        done = True
    except:
        print('Wystąpił błąd. Podaj opcje jeszcze raz. Wpisane "exit" powoduje wyjście z programu')
        input_file = input('Plik wejściowy: ')
        if 'exit' == input_file.lower():
            sys.exit()
        output_file = input('Plik wyjściowy: ')
        if 'exit' == output_file.lower():
            sys.exit()
        remove_numbers = input('Usuwanie liczb [y/n]: ')
        if 'exit' == remove_numbers.lower():
            sys.exit()
        lower = input('Małe litery [y/n]: ')
        if 'exit' == lower.lower():
            sys.exit()
        keep_spaces = input('Zachowanie spacji [y/n]: ')
        if 'exit' == keep_spaces.lower():
            sys.exit()

        remove_numbers = remove_numbers in 'yY'
        lower = lower in 'yY'
        keep_spaces = keep_spaces in 'yY'