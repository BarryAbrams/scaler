def getChildByName(parent, name):
    foundItem = "null"

    for child in parent.GetChildren():
        if child.GetName() == name:
            foundItem = child
    if foundItem == "null":
        return False
    else:    
        return foundItem


class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Rect:
    def __init__(self,points):
        # order
        self.unorderedPoints = points

        smallestX = 10000
        largestX = -10000
        smallestY = 10000
        largestY = -10000

        for point in self.unorderedPoints:
            if point.x > largestX:
                largestX = point.x
            if point.x < smallestX:
                smallestX = point.x
            if point.z > largestY:
                largestY = point.z
            if point.z < smallestY:
                smallestY = point.z

        topLeftPoint = Vector(smallestX, 0, smallestY)
        topRightPoint = Vector(largestX, 0, smallestY)
        bottomRightPoint = Vector(largestX, 0, largestY)
        bottomLeftPoint = Vector(smallestX, 0, largestY)

        self.points = [topLeftPoint, topRightPoint, bottomRightPoint, bottomLeftPoint]

        self.width = largestX - smallestX
        self.height = largestY - smallestY
        self.center = Vector((largestX + smallestX) / 2, 0, (largestY + smallestY) / 2 )