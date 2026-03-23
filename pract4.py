def is_correct(s):
    semicolon = 0
    bracket1 = 0
    bracket2 = 0
    flag = 0

    # Check first 3 characters → "for"
    if s[:3] != "for":
        print("Error in for keyword usage")
        return

    # Count symbols
    for ch in s:
        if ch == '(':
            bracket1 += 1
        elif ch == ')':
            bracket2 += 1
        elif ch == ';':
            semicolon += 1

    # Check semicolons
    if semicolon != 2:
        print("Semicolon Error")
        flag += 1

    # Check closing parenthesis at end
    elif s[-1] != ')':
        print("Closing parenthesis absent at end")
        flag += 1

    # Check opening parenthesis after 'for'
    elif len(s) > 4 and s[3] == ' ' and s[4] != '(':
        print("Opening parenthesis absent after for keyword")
        flag += 1

    # Check parentheses count
    elif bracket1 != 1 or bracket2 != 1 or bracket1 != bracket2:
        print("Parentheses Count Error")
        flag += 1

    # No error
    if flag == 0:
        print("No error")


# -------- Driver Code -------- #

str1 = "for (i = 10; i < 20; i++)"
str2 = "for i = 10; i < 20; i++)"

print("Checking str1:")
is_correct(str1)

print("\nChecking str2:")
is_correct(str2)
