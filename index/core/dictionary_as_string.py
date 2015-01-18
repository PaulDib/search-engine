import re

class DictionaryAsString(object):
    key_sep = "."
    val_sep = "-"
    item_format = key_sep + "{0}" + val_sep + "{1}"

    def __init__(self):
        self._data = ""
        self._length = 0

    def __len__(self):
        return self._length

    def __setitem__(self, key, value):
        if self._get_item_position(key) == -1:
            self._data += DictionaryAsString.item_format.format(key, value)
            self._length += 1
        else:
            old_val = self[key]
            old_item = DictionaryAsString.item_format.format(key, old_val)
            new_item = DictionaryAsString.item_format.format(key, value)
            self._data = self._data.replace(old_item, new_item)

    def __getitem__(self, key):
        position = self._get_item_position(key)
        if position == -1:
            print(self._data)
            raise KeyError(key)
        buff = ""
        idx = position + len(key) + len(DictionaryAsString.key_sep) + len(DictionaryAsString.val_sep)
        while idx < len(self._data) and self._data[idx] != ".":
            buff += self._data[idx]
            idx += 1
        return int(buff)

    def __contains__(self, key):
        return self._get_item_position(key) != -1

    def __iter__(self):
        splitted = self._data \
            .replace(DictionaryAsString.val_sep, DictionaryAsString.key_sep) \
            .split(DictionaryAsString.key_sep)
        keys = [splitted[2*x+1] for x in range(0, int(len(splitted)/2))]
        return iter(keys)

    def values(self):
        splitted = self._data \
            .replace(DictionaryAsString.val_sep, DictionaryAsString.key_sep) \
            .split(DictionaryAsString.key_sep)
        values = [int(splitted[2*x]) for x in range(1, int(len(splitted)/2))]
        return iter(values)

    def _get_item_position(self, key):
        try:
            return self._data.index(DictionaryAsString.item_format.format(key, ""))
        except ValueError:
            return -1
            