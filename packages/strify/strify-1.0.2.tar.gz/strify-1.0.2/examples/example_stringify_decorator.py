from strify import stringifiable, stringify


def format_proper_name(string):
    return ' '.join((word[0].upper() + word[1:].lower() for word in string.split(' ')))


@stringifiable()
class Song:
    def __init__(self, artist, title, year, album):
        self._artist = artist
        self._title = title
        self._year = year
        self._album = album

    @property
    @stringify(format_proper_name)
    def artist(self):
        return self._artist

    @property
    @stringify(format_proper_name)
    def title(self):
        return self._title

    @property
    @stringify(marker_name='YEAR')
    def year(self):
        return self._year

    # it will not be formatted
    @property
    @stringify()
    def album(self):
        return self._album

    def __hash__(self):
        return hash(str(self._artist) + self._title)


if __name__ == '__main__':
    song = Song(
        artist='we butter the bread with butter',
        title='alptraum song',
        album='der tag an dem die welt unterging',
        year=2010
    )

    patterns = [
        '[artist] -- [title] ([YEAR])',
        '[title]: [artist], [YEAR]',
        '"[title]" by "[artist]" from "[album]"'
    ]

    for index, pattern in enumerate(patterns):
        representation = song.stringify(pattern)
        print(f'{index}. {representation}')
