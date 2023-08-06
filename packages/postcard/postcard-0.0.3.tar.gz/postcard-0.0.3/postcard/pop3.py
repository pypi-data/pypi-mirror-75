# -*- coding: utf-8 -*-
# @author: leesoar

"""POP3 client"""

import base64
import poplib
from email.parser import Parser

from postcard import setting


__all__ = ["Pop3"]


class Pop3(object):
    def __init__(self):
        self.user = None
        self.pwd = None
        self._client = None
        self.pop_addr = self.get_addr_map()["163"]
        self.parser = Parser()

    def login(self, user, pwd, pop_addr=None, now=True):
        """Login current mailbox"""
        self.user = user
        self.pwd = pwd
        self.pop_addr = pop_addr or self.pop_addr

        if now:
            self._client = poplib.POP3(self.pop_addr)
            self._client.user(self.user)
            self._client.pass_(self.pwd)
        return self._client

    def close(self):
        self._client.quit()

    @staticmethod
    def get_addr_map():
        return setting.MAIL_ADDR

    def get_client(self):
        """Get pop3 client"""
        return self._client

    def how_many(self) -> int:
        """Return mailbox's email count"""
        return self._client.stat()[0]

    def retrieve(self, index_: int = None) -> dict:
        """Retrieve mail at index"""
        index_ = index_ or self.how_many()
        line_array = self._client.retr(index_)[1]
        delimiter = line_array.index(b"")
        content = base64.b64decode(b"".join(line_array[delimiter:])).decode()

        def __convert(x: bytes) -> list:
            k, v = x.decode().split(":", 1)
            return [k.lower().strip(), v.lower().strip().lstrip("[").rstrip("]")]

        mail_info = dict(map(__convert, filter(lambda x: b":" in x and b"\t" not in x, line_array)))
        mail_info.update(content=content)
        return mail_info

    def delete(self, index_: int = None):
        """Delete mail at index"""
        index_ = index_ or self.how_many()
        self._client.dele(index_)

    def process(self, user=None, pwd=None, pop_addr=None):
        """process decorator

        Args:
            user: mailbox account
            pwd: mailbox password
            pop_addr: current mailbox's pop3 addr
        Usage:
            pop = Pop3()

            @pop.process(user="xxx", pwd="xxx")
            def get_content():
                content = pop.retrieve()["content"]
                log.debug(content)
        """
        user = user or self.user
        pwd = pwd or self.pwd
        pop_addr = pop_addr or self.pop_addr

        assert None not in [user, pwd, pop_addr], \
            "You should give your info."

        def decorator(func):
            def wrapper(*args, **kwargs):
                self.login(user, pwd, pop_addr, not self._client)
                ret = func(*args, **kwargs)
                self.close()
                return ret
            return wrapper
        return decorator
