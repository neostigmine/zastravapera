from database import Word


class SesameWord(Word):
    def __init__(self, word: str, pronunciation: str, origin: str, object_: str, action: str, property_: str, etc: str,
                 *notes: str):
        super().__init__(word)
        self.pronunciation = pronunciation
        self.origin = origin
        self.object = object_
        self.action = action
        self.property = property_
        self.etc = etc
        self.notes = notes

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}**' if not special else f'__**{self.word}** (일치)__'

    def get_field_value(self) -> str:
        definitions = list()
        if self.object:
            definitions.append(f'[객체] {self.object}')
        if self.action:
            definitions.append(f'[동작] {self.action}')
        if self.property:
            definitions.append(f'[속성] {self.property}')
        if self.etc:
            definitions.append(f'[기타] {self.etc}')
        return '\n'.join(definitions)
