# Overview

The library allows you to get a string representation of a class at **RUNTIME**, without overloading ```__repr__```, ```__str__```
or defining your own specific ```get_repr() -> str``` (or even several for different cases).  
The library provides a *lightweight* API using which you can _in a minute_ add a pattern processing function
```stringify(pattern: str) -> str``` to any class.  

This tool is more **intended to help developers** that want to **allow users specify their own
data representation patterns**.

# Motivation  
You're a developer. Let's assume that ```song_downloader``` is a library you wrote using ```strify```. ```song_downloader.search_in_web()``` searchs for a song 
on the Internet and returns an instance of ```Song``` class that allows to download the song using
```Song.download_mp3()```  

```python
>>> from song_downloader import search_in_web
>>> song = search_in_web(title='Loosing My Mind', artist='Falling In Reverse')
>>> print(song)
Song(Loosing My Mind, Falling In Reverse, 2018)
>>> song.download_mp3('[artist] — [title] ([year])')
```

The code will download the mp3 and save it as "Falling In Reverse — Loosing My Mind (2018).mp3".

You may ask: "**why should I use ```strify```** if I could do that like \*the code below\*?"
```python
>>> from song_downloader import search_in_web
>>> song = search_in_web(title='Loosing My Mind', artist='Falling In Reverse')
>>> print(song)
Song(Loosing My Mind, Falling In Reverse, 2018)
>>> song.download_mp3(f'{song.artist} — {song.title} ({song.year})')
```

You definitely can. But there is *no flexibility* for the end user that can't change sources;
usually, he/she just is not assumed to do that, it's not a good practice.

```strify```'s approach is to **ask a user to enter whatever pattern he/she wants** and supply it to
the program in any way (args, json, data base etc.) 
and just use the value in the script. That's the power: **it's not necessary to define a pattern in the source code**.

Now we can change the example and save it as ```download_mp3.py```:
```python
from song_downloader import search_in_web
args = parse_args()
song = search_in_web(title=args['title'], artist=args['artist'])
song.download_mp3(args['mp3_name_pattern'])
```

Then run it like this:
```
python3 download_mp3.py --title='loosing my mind' --artist='falling in reverse' --mp3-name-pattern='[artist] — [title] ([year])'
```
And check what's happened:
```shell script
user@computer:~/$ ls -1
...
download_mp3.py
Falling In Reverse — Loosing My Mind (2018).mp3
...
user@computer:~/$
```

# Usage Guide
Let's continue with our Song class:
```python
from random import randrange

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
    
    def get_year(self):
        year = randrange(1960, 2020)
        return year
```
**Notice**: ```Song.get_year()``` is a mock. In a real code it has to connect to the net and
find all the data there using ```self.title``` and ```self.artist```.

### Diving in
First of all, you need to take a look at the terminology:
* **stringification** — process of building class instance representation (according to a **pattern**)   
* **pattern** — a string with **markers**. After **stringification** all the markers 
will be replaced with **marker values** (or ```final_marker_value```, see **preprocessing function**)
* **marker** — ```f'[{marker_name}]'```
* **marker attribute** — name of a class instance attribute which value is used during **stringification**.  
* **marker value**: the way ```strify``` gets **marker value** looks like this:
```python
import inspect
def get_marker_value(class_instance, marker_attribute):
    marker_value = getattr(class_instance, marker_attribute)
    if inspect.ismethod(marker_value):
        marker_value = marker_value()
    return str(marker_value)
```
* **preprocessing function**:
```python
def preprocessing_function(marker_value: str) -> str:
    final_marker_value = whatever_magic_you_want(marker_value)
    return final_marker_value
```


#### Way #1: use ```stringifiable``` and ```StringifyInfo```

```stringifiable``` gets list of ```StringifyInfo``` and adds ```stringify(pattern: str) -> str```
method to the class it decorates.  
One ```StringifyInfo``` in the list describes one **marker**.
  
Signature:  
```StringifyInfo(marker_name, marker_attribute=None, preprocessing_function=None)```  
If ```marker_attribute``` isn't passed to the constructor (i.e. is ```None```) then
it's assumed to be the same as passed ```marker_name```.

```python
from strify import stringifiable, StringifyInfo

from random import randrange

# transforms 'tHis striNg' into 'This String'
def format_proper_name(string):
    return ' '.join(word[0].upper() + word[1:].lower() for word in string.split(' '))

@stringifiable([
    StringifyInfo('title', None, format_proper_name),
    StringifyInfo('artist', 'artist', format_proper_name),
    StringifyInfo('year', 'get_year'),
])
class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
    
    def get_year(self):
        year = randrange(1960, 2020)
        return year
```

Now, the following is possible:
```python
>>> song = Song('loosing my mind', 'falling in reverse')
>>> song.stringify('[artist] — [title] ([year])')
Falling In Reverse — Loosing My Mind (2018)
>>> song.stringify('[title]: [artist], [year]')
Loosing My Mind: Falling In Reverse, 2018
```

#### Way #2: use ```stringifiable``` and ```stringify```

Signature:  
```stringify(preprocessing_func=None, marker_name=None)```  
If ```marker_name``` equals ```None``` (i.e. not passed) then it's assumed
that ```marker_name == func.__name__```  

```python
from strify import stringifiable, stringify

from random import randrange

# transforms 'tHis striNg' into 'This String'
def format_proper_name(string):
    return ' '.join(word[0].upper() + word[1:].lower() for word in string.split(' '))

@stringifiable()
class Song:
    def __init__(self, title, artist):
        self._title = title
        self._artist = artist
    
    @stringify(format_proper_name)
    def artist(self):
        return self._artist

    @stringify(format_proper_name)
    def title(self):
        return self._title

    @stringify(marker_name='year')
    def get_year(self):
        year = randrange(1960, 2020)
        return year
```

**Notice**: it would be more usual to make properties.
In this case, ```stringify``` **must** be the first decorator that's applied to the function.
```python
@property
@stringify(format_proper_name)
def title(self):
    return self._title
```

Now you can test the code we ran at the end of **Way #1** and ensure that we achieved the same interface and results:
```python
>>> song = Song('loosing my mind', 'falling in reverse')
>>> song.stringify('[artist] — [title] ([year])')
Falling In Reverse — Loosing My Mind (2018)
>>> song.stringify('[title]: [artist], [year]')
Loosing My Mind: Falling In Reverse, 2018
```