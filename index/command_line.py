from .getch import getch

class CommandLine:
    '''
    Provides a reading function for a REPL environment.
    '''
    def __init__(self, autocomplete_actions = None):
        self._history = []
        if autocomplete_actions:
            self._autocomplete = autocomplete_actions
        else:
            self._autocomplete = []

    def readInput(self, prompt):
        '''
        Prompts a user for an input that should be validated with Enter key.
        Allows for autocompletion and history.
        '''
        char = ''
        self._initBuffer()
        print(prompt, end="", flush = True)
        while True:
            char = getch()
            self._old_len = len(self._buff)
            if ord(char) == 13: # Enter key
                print("")
                self._addBufferToHistory()
                return self._buff
            if char =='\x1b': # Escaped sequence
                self._handleEscapedSequence()
            elif ord(char) == 9: # Tab key
                self._autocompleteBuffer()
            elif ord(char) == 127: # Backspace key
                self._erasePreviousChar()
            elif ord(char) >= 32: # Printable char
                self._addToBuffer(char)
            self._updateHistory()
            self._writeBuffer(prompt)

    def _initBuffer(self):
        self._buff = ""
        self._buff_ptr = 0
        self._hist_ptr = len(self._history)
        self._history = self._history + [self._buff]

    def _handleEscapedSequence(self):
        arrowChar = getch()
        if arrowChar == '[':
            arrowChar = getch()
        if arrowChar == 'A' or arrowChar == 'H': # Up arrow
            self._showPreviousCommand()
        elif arrowChar == 'B' or arrowChar == 'P': # Down arrow
            self._showNextCommand()
        elif arrowChar == 'C' or arrowChar == 'M': # Right arrow
            self._moveCursorRight()
        elif arrowChar == 'D' or arrowChar == 'K': # Left arrow
            self._moveCursorLeft()

    def _showPreviousCommand(self):
        self._hist_ptr = self._hist_ptr - 1 if self._hist_ptr > 0 else 0
        if self._history:
            self._buff = self._history[self._hist_ptr]
        self._buff_ptr = len(self._buff)

    def _showNextCommand(self):
        if self._hist_ptr < len(self._history):
            self._hist_ptr = self._hist_ptr + 1
        else:
            self._hist_ptr = len(self._history) - 1
        if self._history and self._hist_ptr < len(self._history):
            self._buff = self._history[self._hist_ptr]
        self._buff_ptr = len(self._buff)

    def _moveCursorRight(self):
        if self._buff_ptr < len(self._buff):
            self._buff_ptr = self._buff_ptr + 1
        else:
            self._buff_ptr = len(self._buff)

    def _moveCursorLeft(self):
        if self._buff_ptr > 0:
            self._buff_ptr = self._buff_ptr - 1
        else:
            self._buff_ptr = 0

    def _autocompleteBuffer(self):
        if self._buff_ptr > 0:
            current_word = self._buff[0:self._buff_ptr].split()[-1]
            autocomplete_targets = [x for x in self._autocomplete if x.startswith(current_word) and not x == current_word]
            if len(autocomplete_targets) == 1:
                self._buff = autocomplete_targets[0]
                self._buff_ptr = len(self._buff)

    def _erasePreviousChar(self):
        if self._buff_ptr > 0:
            self._buff = self._buff[0:self._buff_ptr-1] + self._buff[self._buff_ptr:]
            self._buff_ptr = self._buff_ptr - 1

    def _addToBuffer(self, char):
        self._buff = self._buff[0:self._buff_ptr] + char + self._buff[self._buff_ptr:]
        self._buff_ptr = self._buff_ptr + 1

    def _addBufferToHistory(self):
        if self._buff == '':
            self._history = self._history[0:-1]
        else:
            self._history[len(self._history) - 1] = self._buff

    def _updateHistory(self):
        if self._hist_ptr == len(self._history) - 1:
            self._history[self._hist_ptr] = self._buff

    def _writeBuffer(self, prompt):
        print("\r" + prompt + " " * self._old_len, end = "", flush = True)
        print("\r" + prompt + self._buff, end = "" , flush = True)
        print("\r" + prompt + self._buff[0:self._buff_ptr], end="", flush = True)
