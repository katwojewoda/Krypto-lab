import sys

class UserA(object):
    def __init__(self, p, g, a = None):
        self.p = p
        self.g = g
        a = int(secret_a)
        self.a = a
        self.g_to_a = None
        self.g_to_b = None
        self.g_to_ab = None
class UserB(object):
    def __init__(self, p, g, b = None):
        self.p = p
        self.g = g
        b = int(secret_b)
        self.b = b
        self.g_to_a = None
        self.g_to_b = None
        self.g_to_ab = None        
def open_file_pg(filename):
    if type(filename) != str:
        raise TypeError

    with open(filename, 'r') as f:
        content = f.read().split(',')
            
    return content

def open_file(filename):
    if type(filename) != str:
        raise TypeError

    with open(filename, 'r') as f:
        content = f.read()
     
    return content

def potega_m(a, b, p):
    if p == 1:
        return 0
    result = 1
    a = a % p
    while b > 0:
        if b & 1:
            result = (result * a) % p
        b = b >> 1
        a = (a * a) % p
    return result

def pdh(alice, bob):
    public_data = {}

    public_data['p'] = alice.p
    public_data['g'] = alice.g

    # obliczanie
    alice.g_to_a = potega_m(alice.g, alice.a, alice.p)
    bob.g_to_a = potega_m(bob.g, bob.b, bob.p)

    # wysłanie
    alice.g_to_b = bob.g_to_a
    bob.g_to_b = alice.g_to_a

    public_data['alice_g_to_a'] = alice.g_to_a
    public_data['bob_g_to_a'] = bob.g_to_a

    # obliczanie
    alice.g_to_ab = potega_m(alice.g_to_b, alice.a, alice.p)
    bob.g_to_ab = potega_m(bob.g_to_b, bob.b, alice.p)

    return public_data

def apdh(public_data):
    # wyciągamy dane dostępne publicznie
    p = public_data['p']
    g = public_data['g']
    g_to_a = public_data['alice_g_to_a']
    g_to_b = public_data['bob_g_to_a']

    a = None
    b = None
    for k in range(p - 1):
        power = potega_m(g, k, p)
        if power == g_to_a:
            a = k
        if power == g_to_b:
            b = k

    return potega_m(g, a*b, p)

input_file_a = None
input_file_b = None
input_file_pg = None
input_file_loaded_a = False
input_file_loaded_b = False
input_file_loaded_pg = False
while not input_file_loaded_a:
    try:
        print(f'Otwieranie pliku {input_file_a}... ', end='')
        secret_a = open_file(input_file_a)
        print('gotowe')
        input_file_loaded_a = True
    except:
        if input_file_a is not None and '.' not in input_file_a:
            input_file_a += '.txt'
            continue
        print('Podaj nazwę pliku zawierającego tajną liczbę a (exit aby wyjść)')
        input_file_a = input()
        if 'exit' == input_file_a.lower():
            sys.exit()
            
while not input_file_loaded_b:
    try:
        print(f'Otwieranie pliku {input_file_b}... ', end='')
        secret_b = open_file(input_file_b)
        print('gotowe')
        input_file_loaded_b = True
    except:
        if input_file_b is not None and '.' not in input_file_b:
            input_file_b += '.txt'
            continue
        print('Podaj nazwę pliku zawierającego tajną liczbę b (exit aby wyjść)')
        input_file_b = input()
        if 'exit' == input_file_b.lower():
            sys.exit()    
            
while not input_file_loaded_pg:
    try:
        print(f'Otwieranie pliku {input_file_pg}... ', end='')
        key_pg = open_file_pg(input_file_pg)
        print('gotowe')
        input_file_loaded_pg = True
    except:
        if input_file_pg is not None and '.' not in input_file_pg:
            input_file_pg += '.txt'
            continue
        print('Podaj nazwę pliku zawierającego p i g (exit aby wyjść)')
        input_file_pg = input()
        if 'exit' == input_file_pg.lower():
            sys.exit()          

p = int(key_pg[0])
g = int(key_pg[1])

alice = UserA(p, g)
bob = UserB(p, g)

dh = pdh(alice, bob)
            
print(f'Klucz Alicji: {alice.g_to_ab}')
print(f'Klucz Boba: {bob.g_to_ab}')
print(f'Publicze dane: {dh}')

key = apdh(dh)

print(f'Złamany klucz: {key}')