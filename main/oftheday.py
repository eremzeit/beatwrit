from datetime import date, timedelta

class WordOfTheDay():
    wordoftheday = None
    updated_date = None
    def __init__(self):
        self.d = date.today()
        randomval = self.d.day * 13 + self.d.month * 19
        
        """If cache doesn't exist or is stale"""
        if not WordOfTheDay.wordoftheday or not WordOfTheDay.updated_date == date.today():
            words = self._parse_words()
            print words
            word = self._generate_word(words, randomval)
            WordOfTheDay.wordoftheday = word
            WordOfTheDay.updated_date = self.d

    def get_word(self):
        return WordOfTheDay.wordoftheday[0]

    def get_part_of_speech(self):
        return WordOfTheDay.wordoftheday[1]

    def get_definitions(self):
        return WordOfTheDay.wordoftheday[2]

    def _generate_word(self, words, randomval):
        i = randomval % len(words)
        return words[i]
        
    def _parse_words(self) :
        words = """_amalgamate
        v
        To merge, to combine, to blend, to join.

        _alacrity
        n
        Eagerness; liveliness; enthusiasm.
        Promptness; speed. 

        _bereft
        adj
        (of a person) pained by the loss of someone
        deprived of, lacking, stripped of, robbed of 

        _caustic
        adj
        Capable of burning, corroding or destroying organic tissue
        (of language etc) sharp, bitter, cutting, biting, sarcastic

        _cacophony
        n
        A mix of discordant sounds; dissonance.


        _bungalow
        n
        A small house or cottage usually having a single story
        A thatched or tiled one-story house in India surrounded by a wide verandah

        _cuckold
        n
        A man married to an unfaithful wife, especially when he is unaware or unaccepting of the fact. 


        _fecund
        adj
        (formal) Highly fertile; able to produce offspring.
        (figuratively) Leading to new ideas or innovation. 


        _rapscallion 
        n
        A rascal, scamp, rogue, or scoundrel.
        (attributive) Roguish, disreputable.

        _reticulate
        v
        (transitive) To distribute or move via a network.
        (transitive) To divide into or form a network.
        (intransitive) To create a network.

        _scintilla
        n
        A small spark or flash.
        A small or trace amount.

        _faklempt
        adj
        overwhelmed, flustered, nervous
        excited, overjoyed, happy

        _Zeitgeist
        n
        The spirit of the age; the taste, outlook, and spirit characteristic of a period.

        _etiolate
        v
        To make pale through lack of light, especially of a plant.
        To make a person pale and sickly-looking.

        _gumption
        n
        Energy of mind and body, enthusiasm.
        Boldness of enterprise; initiative or aggressiveness, guts; spunk; initiative.

        _lubricious
        adj
        smooth and glassy; slippery
        lewd, wanton, salacious or lecherous

        _quiddity
        n
        The essence or inherent nature of a person or thing.
        An eccentricity; an odd feature
        """
        lines = words.splitlines()

        words = []

        state = 0
        word = None
        pos = None
        defs = []
        for line in lines:
            _line = line.strip()
            if _line == '':
                continue
            if _line[0] == '_':
                if state == 2:
                    words.append((word, pos, defs))
                    word = None
                    pos = None
                    defs = []
                word = _line[1:]
                state = 1
            elif state == 1:
                pos = _line
                state = 2
            elif state == 2:
                defs.append(_line)
        return words
            


