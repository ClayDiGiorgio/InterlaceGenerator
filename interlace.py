import re

def doNothing():
    return True


# assumes path matches [r|l|u|d|R|L|U|D]*
def flip(path):
    assert(type(path) == str)
    
    flip = {"r" : "l",
            "d" : "u",
            "l" : "r",
            "u" : "d",
            "R" : "L",
            "D" : "U",
            "L" : "R",
            "U" : "D"}
        
    return "".join([flip[letter] for letter in path])


# assumes path matches [r|l|u|d|R|L|U|D]*
def rotate90(path):
    assert(type(path) == str)
    
    rotate = {"r" : "d",
              "d" : "l",
              "l" : "u",
              "u" : "r",
              "R" : "D",
              "D" : "L",
              "L" : "U",
              "U" : "R"}
    return "".join([rotate[letter] for letter in path])



# assumes direction matches [r|l|u|d|R|L|U|D]
# location must be a two-integer tuple, eg (0,0)
def follow(direction, location):
    assert(type(direction) == str)
    
    assert(type(location) == tuple)
    assert(len(location) == 2)
    assert(type(location[0]) == int and type(location[1]) == int)
    
    # capital letters are followed the same way as
    # lowercase letters
    direction = direction.lower()
    
    if(direction == "r"):
        return (location[0]+1, location[1])
    if(direction == "l"):
        return (location[0]-1, location[1])
    if(direction == "u"):
        return (location[0], location[1]+1)
    if(direction == "d"):
        return (location[0], location[1]-1)
    
    return location


# overlap is illegal if the path lies on top of itself in parallel
# or if the path changes direction while overlapping (corner overlap) 
#
# eg: "rl"                 => parallel overlap (turnback)
# eg: "ruld" (loop) + "r"  => parallel overlap
# eg: "rurdld"             => corner overlap
#
# this is fine though:
# "ruldd"                  => orthogonal overlap
#
# assumes path matches [r|l|u|d|R|L|U|D]*
def hasIllegalOverlap(path, checkStart=False, checkEnd=False):
    assert(type(path) == str)
    assert(type(checkStart) == bool)
    assert(type(checkEnd) == bool)
    
    # uppercase and lowercase directions behave the same
    # as far as illegal overlap is concerned
    path = path.lower()
    
    # check for turnbacks
    if re.search("rl", path) or re.search("ud", path) or \
       re.search("lr", path) or re.search("du", path):
        return True
    
    
    # set of all coords directly adjacent on the path
    coordPairs = set((0,0))
    # set of all coords visited by the path
    allCoords = set()
    
    prevCoord = (0,0)
    currCoord = (0,0)
    
    coords = pathToCoords(path)
    
    for i in range(0, len(path)-1):
        prevCoord = currCoord
        currCoord = coords[i]
        
        # check for parallel overlap
        if (prevCoord, currCoord) in coordPairs:
            return True
        if (currCoord, prevCoord) in coordPairs:
            return True
        
        # check for corner overlap
        
        # The first cell can never be a turn/corner, plus
        # checking if it is will cause an out of bounds
        # exception. Skip it
        if(i > 0): 
            # Index i is a corner iff path[i] != path[i-1]
            if(currCoord in allCoords and path[i] != path[i-1]): 
                return True # changed direction while overlapping
        
        coordPairs.add((prevCoord, currCoord))
        
        if not( (checkEnd and i == len(path)-1) or (checkStart and i == 0) ):
            allCoords.add(currCoord)
    
    # if the parameters specify that the end / begining of the path
    # having overlap is illegal, check them
    
    if checkEnd:
        if currCoord in allCoords:
            return True
    if checkStart:
        if (0,0) in allCoords:
            return True
    
    # no illegal overlap found!
    return False
 

# connect two paths with a straight line of length i
# rotates path2 until this is possible
def join(path1, path2, i):
    assert(type(path1) == str)
    assert(type(path2) == str)
    assert(type(i) == int)
    
    # rotate path2 until its start matches path1's end
    for i in range(4):
        if path1[-1].lower() == path2[0].lower():
            break
        path2 = rotate90(path2)
    
    # if it was rotated four times and it still doesn't line up,
    # it will never line up and something's wrong
    if path1[-1].lower() != path2[0].lower():
        return False
    
    # simple join
    joinDir = path1[-1]
    return path1 + joinDir*i + path2
    

# Internal function, support for joinMany
# since it's an internal function, I assume it will be called correctly
def __joinMany_Backtracking(paths, offsets, currentJoin, i, jCap=100, checkEnd=False, checkStart=False):
    #
    # base case
    #
    
    if i == len(paths)-1:
        # support for checkEnd and checkStart
        # if these are both false, this while loop will never trigger
        j = -1
        while hasIllegalOverlap(currentJoin, checkStart=checkStart, checkEnd=checkEnd) and j < jCap:
            j += 1
            currentJoin += currentJoin[-1]
        
        if j >= jCap:
            return False
        return currentJoin
    
    #
    # non-basecase
    #
    
    recursed = False
    j = -1
    
    while not recursed:
        j += 1
        newJoin = join(currentJoin, paths[i+1], j)
        
        while hasIllegalOverlap(newJoin, checkStart=checkStart) and j < jCap:
            j += 1
            newJoin = join(currentJoin, paths[i+1], j)
            
        offsets[i] = j
        if j >= jCap:
            return False
        
        recursedJoin = __joinMany_Backtracking(paths, offsets, newJoin, i+1, jCap=jCap, checkEnd=checkEnd, checkStart=checkStart)
        recursed = (type(recursedJoin) == str)

    return recursedJoin


# assumes paths is a list of strings that all match [r|l|u|d|R|L|U|D]*
# given a list of paths, joins them with strictly straight lines (after
# rotating them such that this is possible) such that the final resulting
# path has no illegal overlap
def joinMany(paths):
    assert(type(paths) == list)
    
    # trivial cases
    if len(paths) == 0:
        return ""
    if len(paths) == 1:
        return paths[0]

    # kick off the backtracking!
    offsets = [0]*len(paths)
    currentJoin = paths[0]
    i = 0
    return __joinMany_Backtracking(paths, offsets, currentJoin, i)


# converts a string `word` to a path using `alphabet`
# returns False if the conversion is impossible with the given alphabet
# otherwise, returns a list of paths of length `len(word)`
#
# intended to convert natural language to interlace paths, and can work with
# more than one word if alphabet has a mapping for spaces and such
def wordToPathList(word, alphabet):
    assert(type(word) == str)
    assert(type(alphabet) == dict)
    
    word = word.lower()
    for letter in word:
        if letter not in alphabet:
            return False
    
    paths = list()
    for letter in word:
        paths.append(alphabet[letter])
        
    return paths


# works just like wordToPath, but joins the resulting paths using the backtracking method
# returns False if the conversion or join is impossible with the given alphabet
def wordToPath(word, alphabet):
    assert(type(word) == str)
    assert(type(alphabet) == dict)
    
    pathlist = wordToPathList(word, alphabet)
    if pathlist == False:
        return False
    
    return joinMany(pathlist)
    

# essentially the inverse of follow()
# returns "-" if the coordinates aren't perfectly vertical or horizontal
# of eachother
# else returns a path of a single direction, long enough to connect
# the two coordinates
def coordsToDirection(c1, c2):
    # ensure that c1 and c2 are in fact 2D integer coordinates
    assert(type(c1) == tuple)
    assert(len(c1) == 2)
    assert(type(c1[0]) == int and type(c1[1]) == int)
    
    assert(type(c2) == tuple)
    assert(len(c2) == 2)
    assert(type(c2[0]) == int and type(c2[1]) == int)
    
    
    if c1 == None or c2 == None:
        return ""
    if c1[0] < c2[0]:
        return "r"*(c2[0]-c1[0])
    if c1[0] > c2[0]:
        return "l"*(c1[0]-c2[0])
    if c1[1] < c2[1]:
        return "u"*(c2[1]-c1[1])
    if c1[1] > c2[1]:
        return "d"*(c1[1]-c2[1])
    else:
        return "-"


# coords must be a list of valid coordinates
# returns the path defined by the list of coordinates
def coordsToPath(coords):
    assert(type(coords) == list)
    for c in coords:
        assert(type(c) == tuple)
        assert(len(c) == 2)
        assert(type(c[0]) == int and type(c[1]) == int)
    
    
    path = ""
    
    for i in range(1, len(coords)):
        c1 = coords[i-1]
        c2 = coords[i]
        path += coordsToDirection(c1, c2)
        
    return path

# assumes path matches [r|l|u|d|R|L|U|D]*
def pathToCoords(path):
    assert(type(path) == str)
    
    path = path.lower()
    coords = list()
    
    curr = (0,0)
    coords.append(curr)
    for d in path:
        curr = follow(d, curr)
        coords.append(curr)
    return coords
    
