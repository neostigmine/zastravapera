import re
from datetime import datetime, timedelta
from pprint import pprint
from typing import Tuple

import gspread
from discord import Embed

from const import get_const
from util import normalise


class Word:
    def __init__(self,
                 word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', prep: str = '',
                 conj: str = '', remark: str = '', derived_from_language: str = '', derived_from_word: str = ''):
        self.word = word
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.prep = prep
        self.conj = conj
        self.remark = remark
        self.derived_from_language = derived_from_language
        self.derived_from_word = derived_from_word

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'**{self.word}**' if not special else f'__**{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.adj:
            definitions.append(f'형: {self.adj}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adv:
            definitions.append(f'부: {self.adv}')
        if self.prep:
            definitions.append(f'관: {self.prep}')
        if self.conj:
            definitions.append(f'접: {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


class ThravelemehWord:
    def __init__(self,
                 word: str, noun: str = '', verb: str = '', adj: str = '', adv: str = '', conj: str = '',
                 remark: str = '', cont: str = '', origin: str = ''):
        self.word = word
        self.noun = noun
        self.verb = verb
        self.adj = adj
        self.adv = adv
        self.conj = conj
        self.remark = remark
        self.cont = cont
        self.origin = origin

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'[{self.cont}] **{self.word}**' if not special else f'__[{self.cont}] **{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'[명] {self.noun}')
        if self.verb:
            definitions.append(f'[동] {self.verb}')
        if self.adj:
            definitions.append(f'[형] {self.adj}')
        if self.adv:
            definitions.append(f'[부] {self.adv}')
        if self.conj:
            definitions.append(f'[접] {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


class Database:
    @staticmethod
    def is_duplicate(query: str, row: list) -> bool:
        return normalise(query) == normalise(row[0]) \
                   or any(normalise(query) in re.split(r'[,;] ', normalise(row[i])) for i in range(1, len(row)))

    def __init__(self):
        self.credential = gspread.service_account(filename='res/google_credentials.json')
        self.sheet = self.credential.open_by_key(get_const('zasokese_database')).sheet1

        self.last_reload = datetime.now()
        self.sheet_values = None
        self.reload()

    def reload(self):
        self.sheet_values = self.sheet.get_all_values()
        self.last_reload = datetime.now()
        return self

    def search_rows(self, query: str) -> Tuple[list, set, bool]:
        reloaded = False
        if self.last_reload + timedelta(weeks=1) < datetime.now():
            self.reload()
            reloaded = True
        duplicates = set()
        rows = list()
        for j, row in enumerate(self.sheet_values):
            for i, column in enumerate(row[:-2]):
                if normalise(query) in normalise(column):
                    rows.append(Word(*row))
                    break
            if self.is_duplicate(query, row):
                duplicates.add(len(rows) - 1)
        return rows, duplicates, reloaded


class ThravelemehDatabase:
    @staticmethod
    def is_duplicate(query: str, row: list) -> bool:
        return normalise(query) == normalise(row[0]) \
                   or any(normalise(query) in re.split(r'[,;] ', normalise(row[i])) for i in range(1, len(row)))

    def __init__(self):
        self.credential = gspread.service_account(filename='res/google_credentials.json')
        self.sheet = self.credential.open_by_key(get_const('thravelemeh_database')).sheet1

        self.last_reload = datetime.now()
        self.sheet_values = None
        self.reload()

    def reload(self):
        self.sheet_values = self.sheet.get_all_values()
        self.last_reload = datetime.now()
        return self

    def search_rows(self, query: str) -> Tuple[list, set, bool]:
        reloaded = False
        if self.last_reload + timedelta(hours=1) < datetime.now():
            self.reload()
            reloaded = True
        duplicates = set()
        rows = list()
        for j, row in enumerate(self.sheet_values):
            for i, column in enumerate(row[:-2]):
                if normalise(query) in normalise(column):
                    rows.append(ThravelemehWord(*row))
                    break
            if self.is_duplicate(query, row):
                duplicates.add(len(rows) - 1)
        return rows, duplicates, reloaded


if __name__ == '__main__':
    database = ThravelemehDatabase()
    pprint(database.search_rows('daaf'))
