import c4d, math, imp
from c4d import utils
#Welcome to the world of Python
scalerUtils = imp.load_source("mymodule", "/Users/barry/Desktop/scaler/scalerUtils.py")
object = imp.load_source("mymodule", "/Users/barry/Desktop/scaler/object.py")

def main(op, doc):

    obj = op.GetDown().GetClone()
    obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
    obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2

    for i in range(op[c4d.ID_USERDATA,1]):
        split(doc, op, obj, i)
        
    for polyID, poly in enumerate(obj.GetAllPolygons()):
        pointA = obj.GetPoint(poly.a)
        pointB = obj.GetPoint(poly.b)
        pointC = obj.GetPoint(poly.c)
        pointD = obj.GetPoint(poly.d)
        
        points = [pointA, pointB, pointC, pointD]
        rect = scalerUtils.Rect(points)

        object.createObject(op, obj, polyID, rect)

    return obj

def split(doc, op, obj, iteration):
    polyes = obj.GetAllPolygons()
    for polyID, poly in enumerate(polyes):
        pointCount = obj.GetPointCount()
        polyCount = obj.GetPolygonCount()
        polys = obj.GetAllPolygons()
        points = obj.GetAllPoints()

        A = polys[polyID].a
        B = polys[polyID].b
        C = polys[polyID].c
        D = polys[polyID].d

        E = pointCount
        F = pointCount + 1
        E2 = pointCount + 2
        F2 = pointCount + 3

        noise = utils.noise
        freq = op[c4d.ID_USERDATA,2]
        duration = op[c4d.ID_USERDATA,6].Get()
        scale = freq * duration
        time = doc.GetTime().Get()/duration
        time1, time2 = utils.SinCos(time*2*math.pi)
        off = iteration * pointCount * op[c4d.ID_USERDATA,7]
        mapping = op[c4d.ID_USERDATA,3]

        slide = noise.Noise(c4d.Vector(time1,time2,0)*scale, off)
        #slide = op[c4d.ID_USERDATA, 4].GetPoint(slide).y * mapping + slide

        size = op[c4d.ID_USERDATA, 5]*2**(op[c4d.ID_USERDATA, 1]/2)

        #horizontal
        if iteration <= 3:
            obj.ResizeObject(pointCount + 4, polyCount + 1)

            length = (points[A] - points[D]).GetLength()
            minL = size/2**(iteration/2+1)

            off = minL/length
            if length <= 2*minL: slide = .5
            else: slide = utils.RangeMap(slide, 0,1, off, 1-off, True)

            Epos = points[A] + (points[D] - points[A])*slide
            Fpos = points[B] + (points[C] - points[B])*slide
            obj.SetPolygon(polyID, c4d.CPolygon(A,B,F,E))
            obj.SetPolygon(polyCount+0, c4d.CPolygon(E2,F2,C,D))



        #vertical
        else:
            obj.ResizeObject(pointCount + 4, polyCount + 1)

            length = (points[A] - points[B]).GetLength()
            minL = size/3**((iteration-1)/2+1)

            off = minL/length
            if length <= 2*minL: slide = .5
            else: slide = utils.RangeMap(slide, 0,1, off, 1-off, True)

            obj.ResizeObject(pointCount+4, polyCount+1)
            Epos = points[A] + (points[B] - points[A])*slide
            Fpos = points[D] + (points[C] - points[D])*slide

            #obj.SetPolygon(polyID, c4d.CPolygon(A,B,C,D))
            #obj.SetPolygon(polyCount+0, c4d.CPolygon(E,F,E2,F2))
            obj.SetPolygon(polyID, c4d.CPolygon(A,E,F,D))
            obj.SetPolygon(polyCount+0, c4d.CPolygon(E2, B,C,F2))


        obj.SetPoint(E, Epos)
        obj.SetPoint(F, Fpos)
        obj.SetPoint(E2, Epos)
        obj.SetPoint(F2, Fpos)