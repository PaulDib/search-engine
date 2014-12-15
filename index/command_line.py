from .getch import getch

class CommandLine:
    def __init__(self, autocomplete_actions = None):
        self._history = []
        if autocomplete_actions:
            self._autocomplete = autocomplete_actions
        else:
            self._autocomplete = []

    def readInput(self, prompt):
        char = ''
        buff = ""
        buff_ptr = 0
        hist_ptr = len(self._history)
        self._history = self._history + [buff]
        print(prompt, end="", flush = True)
        while True:
            char = getch()
            old_len = len(buff)
            if ord(char) == 13: # Enter key
                print("")
                if buff == '':
                    self._history = self._history[0:-1]
                else:
                    self._history[len(self._history) - 1] = buff
                return buff
            if char =='\x1b': # Escaped sequence
                nextChar = getch()
                if nextChar == '[':
                    arrowChar = getch()
                    if arrowChar == 'A': # Up
                        hist_ptr = hist_ptr - 1 if hist_ptr > 0 else 0
                        buff = self._history[hist_ptr] if len(self._history) > 0 else buff
                        buff_ptr = len(buff)
                    elif arrowChar == 'B': # Down
                        hist_ptr = hist_ptr + 1 if hist_ptr < len(self._history) else len(self._history) - 1
                        buff = self._history[hist_ptr] if len(self._history) > 0 and hist_ptr < len(self._history) else buff
                        buff_ptr = len(buff)
                    elif arrowChar == 'C': # Right
                        buff_ptr = buff_ptr + 1 if buff_ptr < len(buff) else len(buff)
                    elif arrowChar == 'D': # Left
                        buff_ptr = buff_ptr - 1 if buff_ptr > 0 else 0
            elif ord(char) == 9: # Tab key
                if buff_ptr > 0:
                    current_word = buff[0:buff_ptr].split()[-1]
                    autocomplete_targets = [x for x in self._autocomplete if x.startswith(current_word) and not x == current_word]
                    if len(autocomplete_targets) == 1:
                        buff = autocomplete_targets[0]
                        buff_ptr = len(buff)
            elif ord(char) == 127: # Backspace key
                buff = buff[0:buff_ptr-1] + buff[buff_ptr:]
                buff_ptr = buff_ptr - 1 if buff_ptr > 0 else 0
            elif ord(char) >= 32: # Printable char
                buff = buff[0:buff_ptr] + char + buff[buff_ptr:]
                buff_ptr = buff_ptr + 1
            if hist_ptr == len(self._history) - 1:
                self._history[hist_ptr] = buff
            print("\r" + prompt + " " * old_len, end = "", flush = True)
            print("\r" + prompt + buff, end = "" , flush = True)
            print("\r" + prompt + buff[0:buff_ptr], end="", flush = True)
