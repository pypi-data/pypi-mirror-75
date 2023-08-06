from strify import stringifiable, StringifyInfo


def format_proper_name(string):
    return ' '.join((word[0].upper() + word[1:].lower() for word in string.split(' ')))


@stringifiable([
    StringifyInfo('artist', None, format_proper_name),
    StringifyInfo('title', 'title', format_proper_name),
    StringifyInfo('album', preprocessing_func=format_proper_name),
    StringifyInfo('year'),
    StringifyInfo('hash', '__hash__'),
])
class Song:
    def __init__(self, artist, title, year, album):
        self.artist = artist
        self.title = title
        self.year = year
        self.album = album

    def __hash__(self):
        return hash(str(self.artist) + self.title)


if __name__ == '__main__':

    song = Song(
        artist='we butter the bread with butter',
        title='alptraum song',
        album='der tag an dem die welt unterging',
        year=2010
    )

    patterns = [
        '[artist] -- [title] ([year])',
        '[title]: [artist], [year]',
        '"[title]" by "[artist]" from "[album]"',
    ]

    for index, pattern in enumerate(patterns):
        representation = song.stringify(pattern)
        print(f'{index}. {representation}')
