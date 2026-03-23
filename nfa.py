import time
from nfa_utils import get_regex_nfa

class NFA:
    def __init__(self):
        self.alphabet = set()
        self.states = {0}
        self.transition_function = {}
        self.accept_states = set()
        self.in_states = {0}

    def add_state(self, state, accepts=False):
        self.states.add(state)
        if accepts:
            self.accept_states.add(state)

    def add_transition(self, from_state, symbol, to_states):
        self.transition_function[(from_state, symbol)] = to_states
        if symbol != "":
            self.alphabet.add(symbol)

    def is_accepting(self):
        return len(self.in_states & self.accept_states) > 0

    def __str__(self):
        return f"""
NFA:
Alphabet: {self.alphabet}
States: {self.states}
Transition Function: {self.transition_function}
Accept States: {self.accept_states}
Current States: {self.in_states}
Accepting: {"Yes" if self.is_accepting() else "No"}
"""


# -------- MAIN -------- #
if __name__ == "__main__":
    regex = input("Enter regex: ").lower()

    print("\nBuilding NFA...")
    start = time.time()

    nfa = get_regex_nfa(regex)

    end = time.time()

    print(f"\nBuilt in {(end - start)*1000:.2f} ms\n")
    print(nfa)
