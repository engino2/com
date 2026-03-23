import copy

# 🔥 IMPORTANT: Import inside function to avoid circular import
def get_single_symbol_regex(symbol):
    from nfa import NFA
    nfa = NFA()
    nfa.add_state(1, True)
    nfa.add_transition(0, symbol, {1})
    return nfa


def shift(nfa, inc):
    nfa.states = {s + inc for s in nfa.states}
    nfa.accept_states = {s + inc for s in nfa.accept_states}

    new_tf = {}
    for (state, sym), targets in nfa.transition_function.items():
        new_tf[(state + inc, sym)] = {t + inc for t in targets}
    nfa.transition_function = new_tf


def merge(a, b):
    a.accept_states = b.accept_states
    a.states |= b.states
    a.transition_function.update(b.transition_function)
    a.alphabet |= b.alphabet


def get_concat(a, b):
    shift(b, max(a.states))
    merge(a, b)
    return a


def get_union(a, b):
    from nfa import NFA

    nfa = NFA()

    a.accept_states = set()
    b.accept_states = set()

    shift(a, 1)
    merge(nfa, a)

    shift(b, max(nfa.states) + 1)
    merge(nfa, b)

    nfa.add_transition(0, "", {1, min(b.states)})

    new_accept = max(nfa.states) + 1
    nfa.add_state(new_accept, True)

    nfa.add_transition(max(a.states), "", {new_accept})
    nfa.add_transition(max(b.states), "", {new_accept})

    return nfa


def get_kleene_star_nfa(nfa):
    from nfa import NFA

    nfa.accept_states = set()  # ✅ FIX

    shift(nfa, 1)
    nfa.add_state(0)

    last = max(nfa.states)
    new_accept = last + 1
    nfa.add_state(new_accept, True)

    nfa.add_transition(last, "", {new_accept})
    nfa.add_transition(0, "", {1, new_accept})
    nfa.add_transition(last, "", {0})

    return nfa


def get_one_or_more_of_nfa(nfa):
    return get_concat(copy.deepcopy(nfa), get_kleene_star_nfa(nfa))


def get_zero_or_one_of_nfa(nfa):
    return get_union(get_single_symbol_regex(""), nfa)


def get_regex_nfa(regex):
    # UNION
    if "|" in regex:
        i = regex.find("|")
        return get_union(
            get_regex_nfa(regex[:i]),
            get_regex_nfa(regex[i+1:])
        )

    # CONCAT (.)
    if "." in regex:
        i = regex.find(".")
        return get_concat(
            get_regex_nfa(regex[:i]),
            get_regex_nfa(regex[i+1:])
        )

    # STAR
    if "*" in regex:
        i = regex.find("*")
        return get_kleene_star_nfa(
            get_regex_nfa(regex[:i])
        )

    # BASE CASE
    if len(regex) == 1:
        return get_single_symbol_regex(regex)

    # IMPLICIT CONCAT
    return get_concat(
        get_regex_nfa(regex[0]),
        get_regex_nfa(regex[1:])
    )
