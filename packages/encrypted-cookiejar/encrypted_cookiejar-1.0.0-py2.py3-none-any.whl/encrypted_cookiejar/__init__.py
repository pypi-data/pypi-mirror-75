#!/usr/bin/env python

import hashlib
import base64
from http.cookiejar import Cookie, FileCookieJar
from cryptography.fernet import Fernet

__all__ = [
    'EncryptedCookieJar',
    'ParseException'
]

__version__ = '1.0.0'

class ParseException(Exception):
    """
        This is raised in case of error parsing file
    """
    pass


class EncryptedCookieJar(FileCookieJar):

    def __getitem__(self, name: str):
        for cookie in iter(self):
            if cookie.name == name:
                return cookie.value
        raise KeyError(name)

    def get(self, name):
        for cookie in iter(self):
            if cookie.name == name:
                return cookie.value
        return None

    def iterkeys(self):
        " Return an iterator of names of cookies from the jar "
        for cookie in iter(self):
            yield cookie.name

    def keys(self):
        " Return a list of names of cookies from the jar "
        return sorted(set(self.iterkeys()))

    def _fernet(self, password):
        " Derive Fernet key from password "
        h = hashlib.sha3_256()
        h.update(password.encode('utf-8'))
        key = base64.urlsafe_b64encode(h.digest())
        return Fernet(key)

    def load(self, filename=None, password=None):
        " Load cookies from a file "
        filename = filename or self.filename
        if filename is None:
            raise ValueError("Filename not supplied")
        with open(filename, 'rb') as f:
            data = f.read()
        if password is not None:
            data = self._fernet(password).decrypt(data)
        for line in data.decode('utf-8').split('\n'):
            try:
                if not line:
                    continue
                line = line.split("\t")
                domain, initial_dot, path, secure, expires, name, value = line
                c = Cookie(0, name, value, None, False,
                           domain,
                           initial_dot == "TRUE",
                           domain.startswith("."),
                           path, False,
                           secure == "TRUE",
                           expires or None,
                           expires is None,
                           None,
                           None,
                           {})
                self.set_cookie(c)
            except Exception:
                raise ParseException("Error parsing cookie jar")

    def save(self, filename=None, password=None):
        " Save cookies to a file "
        filename = filename or self.filename
        if filename is None:
            raise ValueError("Filename not supplied")
        lines = []
        for cookie in self:
            secure = "TRUE" if cookie.secure else "FALSE"
            initial_dot = "TRUE" if cookie.domain.startswith(".") else "FALSE"
            expires = str(cookie.expires) if cookie.expires is not None else ""
            lines.append("\t".join([cookie.domain, initial_dot, cookie.path,
                         secure, expires, cookie.name, cookie.value]))
        data = '\n'.join(lines).encode('utf-8')
        if password is not None:
            data = self._fernet(password).encrypt(data)
        with open(filename, "wb") as f:
            f.write(data)

    def __eq__(self, other):
        def k(cookie):
            return cookie.name + '|' + (cookie.domain or '') + '|' + (cookie.path or '')
        if not isinstance(other, self.__class__):
            return False
        d1 = dict((k(x), x) for x in self)
        d2 = dict((k(x), x) for x in other)
        if not d1.keys() == d2.keys():
            return False
        for cookie in self:
            other_cookie = d2.get(k(cookie))
            if other_cookie is None or cookie.__dict__ != other_cookie.__dict__:
                return False
        return True

    def __str__(self):
        return "; ".join(["=".join([x.name, x.value]) for x in self])

