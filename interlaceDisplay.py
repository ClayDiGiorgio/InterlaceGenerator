from interlace import *

#
# Graphics functions
#

def addNubs(coords, path, nubLen=0.5):
    startDisp = [l*nubLen for l in follow(flip(path[0]), (0,0))]
    endDisp   = [l*nubLen for l in follow(path[-1],      (0,0))]
    
    start = (coords[0] [0] + startDisp[0], coords[0] [1] + startDisp[1])
    end   = (coords[-1][0] + endDisp[0],   coords[-1][1] + endDisp[1]  )
    
    coords.insert(0,start)
    coords.append(end)
    
    return coords


import math
# returns [minX, minY, maxX, maxY]
def getBounds(coords):
    bounds = [0,0,0,0]

    for c in coords:
        if c[0] < bounds[0]:
            bounds[0] = math.ceil(c[0])
        if c[1] < bounds[1]:
            bounds[1] = math.ceil(c[1])
        if c[0] > bounds[2]:
            bounds[2] = math.ceil(c[0])
        if c[1] > bounds[3]:
            bounds[3] = math.ceil(c[1])
        
    return bounds
 

import random
def semiKruskalFill(coordsAlreadyFilled, bounds):
    endpoints = set((x,y) for x in range(bounds[0], bounds[2]+1) for y in range(bounds[1], bounds[3]+1))
    endpoints = endpoints - set(c for c in coordsAlreadyFilled)
    endpointsList = [e for e in endpoints]
    
    adjacentEndpoints = set()
    for i in range(len(endpointsList)):
        foundAdj = False
        e1 = endpointsList[i]
        
        # make sure that isolated points still have adjacencies
        if not foundAdj:
            # find the nearest endpoints to e1 that share a coordinate value
            # (ie they're both on the same horizontal or vertical line)
            count = 0
            for j in range(1, max(bounds[2] - bounds[0], bounds[3] - bounds[1])):
                e2 = (e1[0]-j, e1[1])
                if e2 in endpoints:
                    adjacentEndpoints.add((e1,e2))
                    count += 1
                e2 = (e1[0]+j, e1[1])
                if e2 in endpoints:
                    adjacentEndpoints.add((e1,e2))
                    count += 1
                e2 = (e1[0], e1[1]-j)
                if e2 in endpoints:
                    adjacentEndpoints.add((e1,e2))
                    count += 1
                e2 = (e1[0], e1[1]+j)
                if e2 in endpoints:
                    adjacentEndpoints.add((e1,e2))
                    count += 1
                    
                if count >= 2:
                    break
                
                    
     
    # pick and remove a random element of adjacentEndpoints
    # if both elements of that are not in endpoints, then skip
    # if end2 is the end line 2,
        # flip line2
    # if end1 is the start of line 1,
        # flip line1
    # append line1 to line 2
    # remove end1 and end2's entries in the lines dictionary
        # because they're no longer endpoints
    # update the entries for the new line's endpoints
     
    lines = {e: [e] for e in endpoints}
     
    while len(adjacentEndpoints) != 0:
        wall = random.sample(adjacentEndpoints, 1)[0]
        adjacentEndpoints.remove(wall)
        
        while wall[0] not in endpoints or wall[1] not in endpoints:
            if len(adjacentEndpoints)==0:
                wall = None
                break
            wall = random.sample(adjacentEndpoints, 1)[0]
            adjacentEndpoints.remove(wall)
            
        if len(adjacentEndpoints)==0 and wall == None:
            break
        
        e1 = wall[0]
        e2 = wall[1]
        line1 = lines[e1]
        line2 = lines[e2]
        if len(line1) > 1:
            lines.pop(e1)
            endpoints.remove(e1)
        if len(line2) > 1:
            endpoints.remove(wall[1])
            lines.pop(e2)
        
        if e1 == line1[0]:
            line1 = line1[::-1]
        if e2 == line2[-1]:
            line2 = line2[::-1]
        
        line1.extend(line2)
        
        lines[line1[0]]  = line1
        lines[line1[-1]] = line1
        
        
    return [lines[e] for e in lines]


import graphics as gr
def __drawAbsolutePath(coords, window, scale, unscaledLineWidth, absoluteLineBorderWidth, highlightEndpoints, color="white", path="", drawLabels=False):
    rectSize = scale * unscaledLineWidth/2
    lineSize = scale * unscaledLineWidth - absoluteLineBorderWidth
    
    # draw the connection borders
    for i in range(1, len(coords)):
        c1 = coords[i-1]
        c2 = coords[i]
        
        l = gr.Line(gr.Point(*c1), gr.Point(*c2))
        l.setWidth(lineSize+absoluteLineBorderWidth*2)
        l.setFill("black")
        l.draw(window)
        
    for i in range(0, len(coords)):    
        # Draw the rectangle
        center = coords[i]
        r = gr.Rectangle(gr.Point(center[0]-rectSize, center[1]-rectSize), 
                         gr.Point(center[0]+rectSize, center[1]+rectSize))
        r.setFill(color)
        if highlightEndpoints:
            if i == 0:
                r.setFill("yellow")
            if i == len(coords)-1:
                r.setFill("blue")
        r.draw(window)
        
        if i == 0:
            continue
        
        # draw the connection
        c1 = coords[i-1]
        c2 = coords[i]
        l = gr.Line(gr.Point(*c1), gr.Point(*c2))
        l.setWidth(lineSize)
        l.setFill(color)
        l.draw(window)

     
    if len(coords) <= 2:
        return
    if path == "":
        return
    
    # redraw connections for path directions marked "the following node and its connections
    # will go over top anything else" by being capitalized to enforce this rule
    for i in range(len(coords)-2):
        if path[i] not in {"R", "L", "U", "D"}:
            continue
        
        center = coords[i+1]
        
        prev = coords[i]
        disp = [max(-1, min(p-c, 1)) for c, p in zip(center, prev)]
        prev = tuple(c+(d*scale/2) for c, d in zip(center, disp))
        
        l = gr.Line(gr.Point(*center), gr.Point(*prev))
        l.setWidth(lineSize+absoluteLineBorderWidth*2)
        l.setFill("black")
        l.draw(window)
        
        if i+2 < len(coords):
            nxt = coords[i+2]
            disp = [max(-1, min(p-c, 1)) for c, p in zip(center, nxt)]
            nxt = tuple(c+(d*scale/2) for c, d in zip(center, disp))
            
            l = gr.Line(gr.Point(*center), gr.Point(*nxt))
            l.setWidth(lineSize+absoluteLineBorderWidth*2)
            l.setFill("black")
            l.draw(window)
            
        
    for i in range(len(path)-2):
        if path[i] not in {"R", "L", "U", "D"}:
            continue
        
        center = coords[i+1]
        
        r = gr.Rectangle(gr.Point(center[0]-rectSize+absoluteLineBorderWidth, center[1]-rectSize+absoluteLineBorderWidth), 
                        gr.Point(center[0]+rectSize-absoluteLineBorderWidth, center[1]+rectSize-absoluteLineBorderWidth))
        r.setFill(color)
        r.setOutline(color)
        r.draw(window)
    
        prev = coords[i]
        disp = [max(-1, min(p-c, 1)) for c, p in zip(center, prev)]
        prev = tuple(c+(d*scale/2) for c, d in zip(center, disp))
        
        l = gr.Line(gr.Point(*center), gr.Point(*prev))
        l.setWidth(lineSize)
        l.setFill(color)
        l.draw(window)
        
        if i+2 < len(coords):
            nxt = coords[i+2]
            disp = [max(-1, min(p-c, 1)) for c, p in zip(center, nxt)]
            nxt = tuple(c+(d*scale/2) for c, d in zip(center, disp))
            
            l = gr.Line(gr.Point(*center), gr.Point(*nxt))
            l.setWidth(lineSize)
            l.setFill(color)
            l.draw(window)
            
    # draw the labels
    if drawLabels:
        for i in range(1, len(path)):
            center = coords[i]
            if path[i-1] in {"R", "L", "U", "D"} or path[i] in {"R", "L", "U", "D"}:
                center = (center[0], center[1] - rectSize/2.0)
            else:
                center = (center[0], center[1] + rectSize/2.0)
                
            label = gr.Text(gr.Point(*center), str(i-1)+"_"+(path[i] if i < len(path) else "?"))
            label.draw(window)
            

def drawPath(path, scale=100, unscaledBorderWidth=1, highlightEndpoints=False, unscaledLineWidth=0.8, absoluteLineBorderWidth=1, drawNubs=True, drawLabels=False):
    if path == "":
        return
    
    try:
        if drawNubs:
            coords = addNubs(pathToCoords(path), path)
            path   = " " + path + " " #adding "nubs" to the path
        else:
            coords = pathToCoords(path)
        bounds = getBounds(coords)
        
        minX = bounds[0] - unscaledBorderWidth/2.0
        minY = bounds[1] - unscaledBorderWidth/2.0
        
        width  = (bounds[2] - bounds[0]) + unscaledBorderWidth
        height = (bounds[3] - bounds[1]) + unscaledBorderWidth
        
        window = gr.GraphWin("interlace", width*scale, height*scale)
        
        
        backgroundLines = semiKruskalFill(coords, bounds)
        for lineCoords in backgroundLines:
            drawCoords = [((c[0]-minX) * scale, (c[1]-minY) * scale) for c in lineCoords]
            __drawAbsolutePath(drawCoords, window, scale, unscaledLineWidth, absoluteLineBorderWidth, False, color="grey")
        
        
        # adjust coords (scale and translate)
        drawCoords = [((c[0]-minX) * scale, (c[1]-minY) * scale) for c in coords]
        __drawAbsolutePath(drawCoords, window, scale, unscaledLineWidth, absoluteLineBorderWidth, highlightEndpoints, path=path, drawLabels=drawLabels)
        
        
        window.getMouse()
        window.close()
    finally:
        pass
    

def pathDrawer(gridSize=20, scale=100, unscaledBorderWidth=1, highlightEndpoints=False, unscaledLineWidth=0.8, absoluteLineBorderWidth=1, unscaledPointRadius=0.1, preloadPath=""):
    try:
        width  = 20 + unscaledBorderWidth*2
        height = 20 + unscaledBorderWidth*2
        
        window = gr.GraphWin("interlace", width*scale, height*scale)
        
        for r in range(width):
            for c in range(height):
                x = (c+unscaledBorderWidth)*scale
                y = (r+unscaledBorderWidth)*scale
                
                circle = gr.Circle(gr.Point(x, y), unscaledPointRadius*scale)
                circle.setFill("black")
                circle.draw(window)

        firstLoc = None
        lastLoc = None
        path = ""
        coords = []
        
        if preloadPath != "":
            path = preloadPath
            coords = pathToCoords(path)
            firstLoc = (10, 10)
            
            loc = coords[-1]
            loc = (loc[0], -loc[1])
            lastLoc = loc
            
            adjCoords = [((c[0]+unscaledBorderWidth+firstLoc[0]) * scale, (-(c[1]+1)+unscaledBorderWidth+firstLoc[1]) * scale) for c in coords]
            __drawAbsolutePath(adjCoords, window, scale, unscaledLineWidth, absoluteLineBorderWidth, highlightEndpoints, path=path)
            
        
        while True:
            loc = window.getMouse()
            loc = [loc.getX()+scale/2, (-loc.getY())+scale/2]
            loc = [loc[0] - unscaledBorderWidth*scale, loc[1] - unscaledBorderWidth*scale]
            loc = (int(loc[0]/scale), int(loc[1]/scale))
            
            
            if firstLoc == None:
                firstLoc = (loc[0], -loc[1])
            
            loc = (loc[0]-firstLoc[0], -(-loc[1]-firstLoc[1]))
            
            adjLoc = loc
            if adjLoc in coords:
                idx = coords.index(adjLoc)
                
                if idx > 0:
                    p = [l for l in path]
                    p[idx-1] = p[idx-1].upper()
                    
                    path = ''.join(p)
            elif lastLoc != None:
                path += coordsToDirection(lastLoc, loc)
            
                lastLoc = loc
                coords = pathToCoords(path)
            else:
                lastLoc = loc
                coords = [(0,0)]
            
            adjCoords = [((c[0]+unscaledBorderWidth+firstLoc[0]) * scale, (-(c[1]+1)+unscaledBorderWidth+firstLoc[1]) * scale) for c in coords]
            __drawAbsolutePath(adjCoords, window, scale, unscaledLineWidth, absoluteLineBorderWidth, highlightEndpoints, path=path)
    finally:
        return path
    
