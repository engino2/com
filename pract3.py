# NFA state
nfa = 1
flag = 0

# -------- STATE FUNCTIONS -------- #

def state1(c):
    global nfa, flag
    if c == 'a':
        nfa = 2
    elif c in ['b', 'c']:
        nfa = 1
    else:
        flag = 1

def state2(c):
    global nfa, flag
    if c == 'a':
        nfa = 3
    elif c in ['b', 'c']:
        nfa = 2
    else:
        flag = 1

def state3(c):
    global nfa, flag
    if c == 'a':
        nfa = 1
    elif c in ['b', 'c']:
        nfa = 3
    else:
        flag = 1

def state4(c):
    global nfa, flag
    if c == 'b':
        nfa = 5
    elif c in ['a', 'c']:
        nfa = 4
    else:
        flag = 1

def state5(c):
    global nfa, flag
    if c == 'b':
        nfa = 6
    elif c in ['a', 'c']:
        nfa = 5
    else:
        flag = 1

def state6(c):
    global nfa, flag
    if c == 'b':
        nfa = 4
    elif c in ['a', 'c']:
        nfa = 6
    else:
        flag = 1

def state7(c):
    global nfa, flag
    if c == 'c':
        nfa = 8
    elif c in ['a', 'b']:
        nfa = 7
    else:
        flag = 1

def state8(c):
    global nfa, flag
    if c == 'c':
        nfa = 9
    elif c in ['a', 'b']:
        nfa = 8
    else:
        flag = 1

def state9(c):
    global nfa, flag
    if c == 'c':
        nfa = 7
    elif c in ['a', 'b']:
        nfa = 9
    else:
        flag = 1


# -------- CHECK FUNCTIONS -------- #

def checkA(s):
    global nfa, flag
    nfa = 1  # RESET

    for ch in s:
        if nfa == 1:
            state1(ch)
        elif nfa == 2:
            state2(ch)
        elif nfa == 3:
            state3(ch)

    return nfa == 1


def checkB(s):
    global nfa, flag
    nfa = 4  # RESET

    for ch in s:
        if nfa == 4:
            state4(ch)
        elif nfa == 5:
            state5(ch)
        elif nfa == 6:
            state6(ch)

    return nfa == 4


def checkC(s):
    global nfa, flag
    nfa = 7  # RESET

    for ch in s:
        if nfa == 7:
            state7(ch)
        elif nfa == 8:
            state8(ch)
        elif nfa == 9:
            state9(ch)

    return nfa == 7


# -------- DRIVER CODE -------- #

s = "bbbca"

if checkA(s) or checkB(s) or checkC(s):
    print("ACCEPTED")
else:
    if flag == 0:
        print("NOT ACCEPTED")
    else:
        print("INPUT OUT OF DICTIONARY")
