"""
Support single string subscripts allowing specification of
full path through a dict/list structure
"""
import re
from contextlib import contextmanager

name_pat = r"(?P<name>[_A-Za-z][_A-Za-z0-9]*)"
subs_pat = r"\[(?P<index>-?\d*)\]"
first_pat = re.compile(rf"{name_pat}|{subs_pat}")
rest_pat = re.compile(rf"\.{name_pat}|{subs_pat}")


class DottedDict:
    """
    String subscripts are interpreted as keys to be used at successive
    layers of subscripting through the dictionaries and lists of a
    JSON-like record.

    Given a DottedDict with the following structure:

        dd = DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})

    the value returned by the expression

        dd['first.second[2].third']

    should be the string 'bingo'.
    """

    def __init__(self, d):  # start with a mapping
        """Initialise the internal dictionary."""
        self._d = d

    def __getitem__(self, key):
        """
        Return the element obtained by splitting the
        string key into strings and integers starting
        at the root of the dict (so the first element
        of the key must be a name).
        """
        o = self._d
        for k in self._fragments(key):
            try:
                o = o[k]
            except ValueError:
                raise KeyError(
                    'Non-integer value for list subscript at end of "{}"'.format(
                        key[: self.pos]
                    )
                )
            except IndexError:
                raise KeyError(
                    'Invalid list index at end of "{}"'.format(key[: self.pos])
                )
            except KeyError:
                raise KeyError(
                    'Unrecognised field name at end of "{}"'.format(key[: self.pos])
                )
        return o

    def __setitem__(self, key, value):
        """
        Set the element indicated by the key string
        to the given value.
        At present (and possibly for ever) we are
        unconcerned about the current value of the key.
        Currently handles only dicts.
        """
        v = self._d
        fs = self._fragments(key)
        k = next(fs)
        for nk in fs:
            v = v[k]
            k = nk
        v[k] = value

    def _fragments(self, key):
        """
        Split the key into its components, yielding
        a string for attribute references and an
        integer for bracketed references.
        """
        self.pos, end = 0, len(key)
        pat = first_pat
        while self.pos < end:
            mo = pat.match(key, self.pos)
            if mo is None:
                raise KeyError(
                    'Cannot find name or list subscript at start of "{}'.format(
                        key[self.pos :]
                    )
                )
            s, i = mo.groups()
            self.pos = mo.end()
            if s:
                yield s
            else:
                yield int(i)
            pat = rest_pat
