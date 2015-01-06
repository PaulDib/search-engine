'''
Provides a class that can read inputs from command line.
'''
from .getch import getch


class CommandLine:

    '''
    Provides a reading function for a REPL environment.
    '''

    def __init__(self, autocomplete_actions=None):
        self._history = []
        self._buff = ""
        self._buff_ptr = 0
        self._hist_ptr = len(self._history)
        self._old_len = 0
        if autocomplete_actions:
            self._autocomplete = autocomplete_actions
        else:
            self._autocomplete = []

    def read_input(self, prompt):
        '''
        Prompts a user for an input that should be validated with Enter key.
        Allows for autocompletion and history.
        '''
        char = ''
        self._init_buffer()
        print(prompt, end="", flush=True)
        while True:
            char = getch()
            self._old_len = len(self._buff)
            if ord(char) == 13:  # Enter key
                print("")
                self._add_buffer_to_history()
                return self._buff
            if char == '\x1b':  # Escaped sequence
                self._handle_escaped_sequence()
            elif ord(char) == 9:  # Tab key
                self._autocomplete_buffer()
            elif ord(char) == 127:  # Backspace key
                self._erase_previous_char()
            elif ord(char) >= 32:  # Printable char
                self._add_to_buffer(char)
            self._update_history()
            self._write_buffer(prompt)

    def _init_buffer(self):
        '''Initializes buffer to default values.'''
        self._buff = ""
        self._buff_ptr = 0
        self._hist_ptr = len(self._history)
        self._history = self._history + [self._buff]

    def _handle_escaped_sequence(self):
        '''
        Handles escaped sequence of character, like arrow keys.
        '''
        arrow_char = getch()
        if arrow_char == '[':
            arrow_char = getch()
        if arrow_char == 'A' or arrow_char == 'H':  # Up arrow
            self._show_previous_command()
        elif arrow_char == 'B' or arrow_char == 'P':  # Down arrow
            self._show_next_command()
        elif arrow_char == 'C' or arrow_char == 'M':  # Right arrow
            self._move_cursor_right()
        elif arrow_char == 'D' or arrow_char == 'K':  # Left arrow
            self._move_cursor_left()

    def _show_previous_command(self):
        '''
        Replaces current buffer with previous command in history.
        '''
        self._hist_ptr = self._hist_ptr - 1 if self._hist_ptr > 0 else 0
        if self._history:
            self._buff = self._history[self._hist_ptr]
        self._buff_ptr = len(self._buff)

    def _show_next_command(self):
        '''
        Replaces current buffer with next command in history.
        '''
        if self._hist_ptr < len(self._history):
            self._hist_ptr = self._hist_ptr + 1
        else:
            self._hist_ptr = len(self._history) - 1
        if self._history and self._hist_ptr < len(self._history):
            self._buff = self._history[self._hist_ptr]
        self._buff_ptr = len(self._buff)

    def _move_cursor_right(self):
        '''
        Move the writing cursor right.
        '''
        if self._buff_ptr < len(self._buff):
            self._buff_ptr = self._buff_ptr + 1
        else:
            self._buff_ptr = len(self._buff)

    def _move_cursor_left(self):
        '''
        Move the writing cursor left.
        '''
        if self._buff_ptr > 0:
            self._buff_ptr = self._buff_ptr - 1
        else:
            self._buff_ptr = 0

    def _autocomplete_buffer(self):
        '''
        Try to autocomplete the current buffer.
        '''
        if self._buff_ptr > 0:
            current_word = self._buff[0:self._buff_ptr].split()[-1]
            autocomplete_targets = [x for x in self._autocomplete
                                    if x.startswith(current_word)
                                    and not x == current_word]
            if len(autocomplete_targets) == 1:
                self._buff = autocomplete_targets[0]
                self._buff_ptr = len(self._buff)

    def _erase_previous_char(self):
        '''Erases the character right before the cursor.'''
        if self._buff_ptr > 0:
            self._buff = self._buff[
                0:self._buff_ptr - 1] + self._buff[self._buff_ptr:]
            self._buff_ptr = self._buff_ptr - 1

    def _add_to_buffer(self, char):
        '''Adds a char to the current buffer at the position of the cursor.'''
        self._buff = self._buff[0:self._buff_ptr] + \
            char + self._buff[self._buff_ptr:]
        self._buff_ptr = self._buff_ptr + 1

    def _add_buffer_to_history(self):
        '''Adds the buffer to history before it is returned to the client.'''
        if self._buff == '':
            self._history = self._history[0:-1]
        else:
            self._history[len(self._history) - 1] = self._buff

    def _update_history(self):
        '''
        Writes the current buffer in history everytime it changes.
        Allows the current buffer to be retrieved when browsing history.
        '''
        if self._hist_ptr == len(self._history) - 1:
            self._history[self._hist_ptr] = self._buff

    def _write_buffer(self, prompt):
        '''Writes the current buffer to the screen.'''
        print("\r" + prompt + " " * self._old_len, end="", flush=True)
        print("\r" + prompt + self._buff, end="", flush=True)
        print("\r" + prompt + self._buff[0:self._buff_ptr], end="", flush=True)
