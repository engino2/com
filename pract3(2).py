dfa = 0  # Start state

def start(c):
    global dfa
    if c == 'a':
        dfa = 1
    elif c == 'b':
        dfa = 3
    else:
        dfa = -1

def state1(c):
    global dfa
    if c == 'a':
        dfa = 2
    elif c == 'b':
        dfa = 4
    else:
        dfa = -1

def state2(c):
    global dfa
    if c == 'a':
        dfa = 1
    elif c == 'b':
        dfa = 3
    else:
        dfa = -1

def state3(c):
    global dfa
    if c == 'b':
        dfa = 3
    elif c == 'a':
        dfa = 4
    else:
        dfa = -1

def state4(c):
    global dfa
    dfa = -1  # Dead state


def is_accepted(s):
    global dfa
    dfa = 0  # Reset

    for ch in s:
        if dfa == 0:
            start(ch)
        elif dfa == 1:
            state1(ch)
        elif dfa == 2:
            state2(ch)
        elif dfa == 3:
            state3(ch)
        elif dfa == 4:
            state4(ch)
        else:
            return False

    return dfa == 3


# Driver code
s = input("Enter string: ")

# Check alphabet
if any(ch not in ['a', 'b'] for ch in s):
    print("INPUT OUT OF ALPHABET")
else:
    if is_accepted(s):
        print("ACCEPTED")
    else:
        print("NOT ACCEPTED")
