"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class GlagoliticTransliter:
    """
    Транслитератор кирилицы в глаголицу.
    """

    table = {
        "\u0430": "\u2c30",
        "\u0431": "\u2c31",
        "\u0432": "\u2c32",
        "\u0433": "\u2c33",
        "\u0434": "\u2c34",
        "\u0435": "\u2c35",
        "\u0451": "\u2c56",
        "\u0436": "\u2c36",
        "\u0437": "\u2c38",
        "\u0438": "\u2c3a",
        "\u0439": "\uef63",
        "\u043a": "\u2c3d",
        "\u043b": "\u2c3e",
        "\u043c": "\u2c3f",
        "\u043d": "\u2c40",
        "\u043e": "\u2c41",
        "\u043f": "\u2c42",
        "\u0440": "\u2c43",
        "\u0441": "\u2c44",
        "\u0442": "\u2c45",
        "\u0443": "\u2c46",
        "\u0444": "\u2c47",
        "\u0445": "\u2c48",
        "\u0446": "\u2c4c",
        "\u0447": "\u2c4d",
        "\u0448": "\u2c4e",
        "\u0449": "\u2c4b",
        "\u044a": "\u2c4f",
        "\u044b": "\uef5f",
        "\u044c": "\u2c50",
        "\u044d": "\uef61",
        "\u044e": "\u2c53",
        "\u044f": "\u2c5d",
    }

    @classmethod
    def translit(cls, text: str) -> str:
        """
        Транслитерирует все кирилические буквы в переданном тексте
        в глаголические.
        
        Не кирилические буквы остаются на своих местах и не выбрасываются
        из текста.

        @param cyriclic_text: str - текст.
        @return текст с заменой всех кирилических букв.
        """
        translited_text = ""
        for letter in text:
            if letter in cls.table:
                translited_text = translited_text + cls.table[letter]
            elif letter.lower() in cls.table:
                translited_text = (
                    translited_text + cls.table[letter.lower()].upper()
                )
            else:
                translited_text = translited_text + letter
        return translited_text


__all__ = ["GlagoliticTransliter"]
