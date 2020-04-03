from interlaceDisplay import pathDrawer
from interlaceDisplay import drawPath
from interlaceDisplay import drawWord

from interlace import wordToPath

if __name__ == "__main__":
    # *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    #
    #  Example of creating and viewing a custom interlace
    #
    # *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    
    # an example of the tool used to help make the above paths
    # click on an existing node to bring it to the top
    #
    # when you're done drawing, close the window
    yourPath = pathDrawer(scale=50)
    
    print(yourPath)
    drawPath(yourPath, scale=50, highlightEndpoints=True)
    
    
    # example of adding to an existing path
    yourPath = pathDrawer(scale=50, preloadPath=yourPath)
    print(yourPath)
    
    # *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    #
    #  Example of converting English to an Interlace display
    #
    # *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    
    # all must start with l and end with u (by my definition for this case)
    # this is just one example alphabet
    alphabet = {'a': 'LUuuLDdrrulllu',
                'b': 'Llllddrrulddrruuuu',
                'c': 'luUuUurdlldrrdlldrrru',
                'd': 'llLldruuurdllu',
                'e': 'lLlLlldruurddruurddruu',
                'f': 'lLllldrRrruuuuldddddluuu',
                'g': 'ldDddrUulldrrruu',
                'h': 'lLlldruullddDdrrruuuurdddlllllu',
                'i': 'lLldruulldddrrruuuu',
                'j': 'LlLldrRruuldddluuu',
                'k': 'LlLlLldruurddruurddruuullllllddddrrrrrrru',
                'l': 'Lldruulldddrrrru',
                'm': 'llLldruuurrddddrru',
                'n': 'LlLldruulldddrrruuuulllldddddrrrrruuuu',
                'o': 'lLllldrRrruuldddluuu',
                'p': 'llldruullddDddrullurrrrrru',
                'q': 'lLlllldruuUurdddddrruuuullllu',
                'r': 'LlLldrruuldddrruuu',
                's': 'LllDddruuuullddrrruu',
                't': 'lllddrruuu',
                'u': 'llldruUuUuldrrdlldrrruuu',
                'v': 'lLlLldrRrruuldddluuulddddrrrrruu',
                'w': 'lLlLldDddrrrruuUuuldDddlUuuuldDddllurrrrrrulllllluu',
                'x': 'lLlldruuurddddruuulllu',
                'y': 'lldruulLlldruurddddrrrru',
                'z': 'luuulddrrulllu',
                ' ': 'lllllluuuuuu',
                '.': 'llllldruuuuu',
                ',': 'lllllldruuuu'}
    
    drawPath(wordToPath("hi", alphabet), highlightEndpoints=True)
    
