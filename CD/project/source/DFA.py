""" # DFA 
- This file contains the DFA class which is used to create a DFA object. 
"""

class DFA:
    def __init__(self,states,accept,star):
        self.states = states
        self.accept = accept 
        self.star = star
        self.position = 0
        self.status = 'start'

    def run(self,input_char):
        if self.states == 'trap':
            return self.states
        
        next_states = self.states[self.position]
        for alphabet in next_states :
            if input_char in alphabet:
                self.position = next_states[alphabet]
                break
        else :
            self.status = 'trap'
            return self.status
        if self.position in self.accept:
            self.status = 'accept*' if self.position in self.star else 'accept'
        else :
            self.status = 'continue'
        return self.states

    def reset(self):
        self.position = 0
        self.status = 'start'

digit_input = tuple(str(i) for i in range( 10)) 
letter_input = tuple(chr(i) for i in range(ord('a'),ord('z')+1)) + tuple(chr(i) for i in range(ord('A'),ord('Z')+1))
white_space_input = ('\n', '\f', '\r', '\t', '\v', ' ')
symbol_input = tuple(';:,[](){}+-*=</&|')


num_states = [
    {digit_input : 1},
    {digit_input : 1 , white_space_input :2 , symbol_input: 2 , letter_input:3 },
    {},
    {}
]
numDFA = DFA(num_states,(2),(2))

id_states = [
    {letter_input : 1},
    {letter_input : 1 , digit_input : 1 , white_space_input : 2 , symbol_input: 2},
    {}
]
idDFA = DFA()
