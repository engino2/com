from collections import defaultdict
from disjoint_set import DisjointSet
import os


class DFA(object):

    def __init__(self, states_or_filename, terminals=None, start_state=None,
                 transitions=None, final_states=None):

        # Initialize all attributes with defaults first
        self.states       = []
        self.terminals    = []
        self.start_state  = None
        self.final_states = []
        self.transitions  = {}

        # If loading from file
        if terminals is None:
            self._get_graph_from_file(states_or_filename)
        # If manual values provided
        else:
            assert isinstance(states_or_filename, (list, tuple))
            self.states = list(states_or_filename)

            assert isinstance(terminals, (list, tuple))
            self.terminals = list(terminals)

            assert isinstance(start_state, str)
            self.start_state = start_state

            assert isinstance(transitions, dict)
            self.transitions = transitions

            assert isinstance(final_states, (list, tuple))
            self.final_states = list(final_states)

    def _get_graph_from_file(self, filename):
        """
        Load DFA from file:
        Line 1: states (space separated)
        Line 2: terminals (space separated)
        Line 3: start state
        Line 4: final states (space separated)
        Line 5+: transitions (current_state terminal next_state)
        """
        if not os.path.exists(filename):
            print(f"ERROR: File '{filename}' not found.")
            print(f"Looking in: {os.getcwd()}")
            print("Make sure 'graph' file is in the same folder as dfa.py")
            return

        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) < 5:
                print("ERROR: graph file must have at least 5 lines.")
                print("Format:\n  Line1: states\n  Line2: terminals\n  Line3: start state\n  Line4: final states\n  Line5+: transitions")
                return

            self.states       = lines[0].split()
            self.terminals    = lines[1].split()
            self.start_state  = lines[2]
            self.final_states = lines[3].split()

            self.transitions = {}
            for i, line in enumerate(lines[4:], start=5):
                parts = line.split()
                if len(parts) == 3:
                    current_state, terminal, next_state = parts
                    self.transitions[(current_state, terminal)] = next_state
                else:
                    print(f"WARNING: Skipping malformed line {i}: '{line}'")

            print("Graph loaded successfully!")
            print(f"  States       : {self.states}")
            print(f"  Terminals    : {self.terminals}")
            print(f"  Start State  : {self.start_state}")
            print(f"  Final States : {self.final_states}")
            print(f"  Transitions  : {self.transitions}\n")

        except Exception as e:
            print(f"ERROR while reading file: {e}")

    def _remove_unreachable_states(self):
        """
        Removes states unreachable from the start state using DFS.
        """
        g = defaultdict(list)
        for k, v in self.transitions.items():
            g[k[0]].append(v)

        stack = [self.start_state]
        reachable_states = set()

        while stack:
            state = stack.pop()
            if state not in reachable_states:
                stack += g[state]
                reachable_states.add(state)

        self.states       = [s for s in self.states if s in reachable_states]
        self.final_states = [s for s in self.final_states if s in reachable_states]
        self.transitions  = {k: v for k, v in self.transitions.items()
                             if k[0] in reachable_states}

    def minimize(self):
        """
        Minimizes the DFA using the table-filling algorithm.
        """
        self._remove_unreachable_states()

        def order_tuple(a, b):
            return (a, b) if a < b else (b, a)

        sorted_states = sorted(self.states)
        table = {}

        # Initialize table: mark pairs (final, non-final) as distinguishable
        for i, item in enumerate(sorted_states):
            for item2 in sorted_states[i + 1:]:
                table[(item, item2)] = (item in self.final_states) != (item2 in self.final_states)

        # Table filling method
        flag = True
        while flag:
            flag = False
            for i, item in enumerate(sorted_states):
                for item2 in sorted_states[i + 1:]:
                    if table[(item, item2)]:
                        continue
                    for w in self.terminals:
                        t1 = self.transitions.get((item, w), None)
                        t2 = self.transitions.get((item2, w), None)
                        if t1 is not None and t2 is not None and t1 != t2:
                            marked = table[order_tuple(t1, t2)]
                            flag = flag or marked
                            table[(item, item2)] = marked
                            if marked:
                                break

        # Merge indistinguishable states using DisjointSet
        d = DisjointSet(self.states)
        for k, v in table.items():
            if not v:
                d.union(k[0], k[1])

        self.states      = [str(x) for x in range(1, 1 + len(d.get()))]
        self.start_state = str(d.find_set(self.start_state))

        new_final_states = []
        for s in d.get():
            for item in s:
                if item in self.final_states:
                    new_final_states.append(str(d.find_set(item)))
                    break

        self.transitions  = {
            (str(d.find_set(k[0])), k[1]): str(d.find_set(v))
            for k, v in self.transitions.items()
        }
        self.final_states = new_final_states

    def show(self):
        """
        Returns transitions grouped by (from_state, to_state) -> [terminals]
        """
        if not self.transitions:
            print("WARNING: No transitions found. Check your graph file.")
            return {}
        temp = defaultdict(list)
        for k, v in self.transitions.items():
            temp[(k[0], v)].append(k[1])
        return temp

    def __str__(self):
        return '{} states. {} final states. start state - {}'.format(
            len(self.states), len(self.final_states), self.start_state
        )


# ---- Main ----
if __name__ == "__main__":
    # graph file must be in same folder as dfa.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, 'graph.txt')

    dfa = DFA(filename)

    if not dfa.transitions:
        print("ERROR: DFA could not be loaded. Exiting.")
    else:
        print("=== BEFORE MINIMIZATION ===")
        x = dict(dfa.show())
        for key, value in x.items():
            print(key, ':', value)
        print(dfa, "\n")

        dfa.minimize()

        print("=== AFTER MINIMIZATION ===")
        x = dict(dfa.show())
        for key, value in x.items():
            print(key, ':', value)
        print(dfa)
