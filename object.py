import c4d, math, imp, random
from c4d import utils

def createObject(op, obj, polyID, rect, matlist):
    identifer = f"Object {polyID}"
    parent = op[c4d.ID_USERDATA, 9]
    foundItem = "null"

    for child in parent.GetChildren():
        if child.GetName() == identifer:
            foundItem = child

    if foundItem == "null":
        nullObject = c4d.BaseObject(c4d.Onull)
        nullObject.SetName(identifer)
        nullObject.InsertUnder(parent)
        
        sharpenedPencil = c4d.BaseObject(c4d.Oboole)
        sharpenedPencil.SetName("Sharpened Pencil")
        sharpenedPencil.InsertUnder(nullObject)
        sharpenedPencil[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT

        #sharpened pencil mask
        intersection = c4d.BaseObject(c4d.Onull)
        intersection.SetName("Intersection")
        intersection.InsertUnder(sharpenedPencil)

        combinedShapes = c4d.BaseObject(c4d.Oboole)
        combinedShapes.SetName("Combined Shapes")
        combinedShapes.InsertUnder(intersection)
        combinedShapes[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_UNION
        combinedShapes[c4d.BOOLEOBJECT_HIGHQUALITY] = False
        
        cylinder = c4d.BaseObject(c4d.Ocylinder)
        cylinder.SetName("Cylinder")
        cylinder.InsertUnder(combinedShapes)
        cylinder[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_ZP
        cylinder[c4d.PRIM_CYLINDER_HSUB] = 1

        cone = c4d.BaseObject(c4d.Ocone)
        cone.SetName("Cone")
        cone.InsertUnder(combinedShapes)
        cone[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_ZP
        cone[c4d.PRIM_CYLINDER_HSUB] = 1

        #pencil
        pencil = c4d.BaseObject(c4d.Onull)
        pencil.SetName("Pencil")
        pencil.InsertAfter(intersection)

        #main lead
        lead = c4d.BaseObject(c4d.Ocylinder)
        lead.SetName("Lead")
        lead.InsertUnder(pencil)
        lead[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_ZP
        lead[c4d.PRIM_CYLINDER_HSUB] = 1

        removeLead = c4d.BaseObject(c4d.Oboole)
        removeLead.SetName("Remove Lead")
        removeLead.InsertAfter(lead)
        removeLead[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_SUBTRACT

        extrude = c4d.BaseObject(c4d.Oextrude)
        extrude.SetName("Extrude")
        extrude.InsertUnder(removeLead)

        spline = c4d.BaseObject(c4d.Osplinenside)
        spline.SetName("Spline")
        spline.InsertUnder(extrude)

        leadHole = c4d.BaseObject(c4d.Ocylinder)
        leadHole.SetName("Lead Hole")
        leadHole.InsertAfter(extrude)
        leadHole[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_ZP
        leadHole[c4d.PRIM_CYLINDER_HSUB] = 1


    else:
        nullObject = foundItem
        #print("known")

    padding = 10
    totalHeight = rect.height - padding
    totalWidth = rect.width - padding


    totalHeight = 600
    totalWidth = 35
    pencilRadius = totalWidth / 2
    leadRadius = pencilRadius 

    sharpenedPencil = getChildByName(nullObject, "Sharpened Pencil")
    intersection = getChildByName(sharpenedPencil, "Intersection")
    combinedShapes = getChildByName(intersection, "Combined Shapes")
    cylinder = getChildByName(combinedShapes, "Cylinder")
    cone = getChildByName(combinedShapes, "Cone")
    pencil = getChildByName(sharpenedPencil, "Pencil")
    lead = getChildByName(pencil, "Lead")
    removeLead = getChildByName(pencil, "Remove Lead")
    extrude = getChildByName(removeLead, "Extrude")
    spline = getChildByName(extrude, "Spline")
    leadHole = getChildByName(removeLead, "Lead Hole")

    cylinderHeight = totalHeight/2
    cylinder[c4d.PRIM_CYLINDER_HEIGHT] = cylinderHeight
    cylinder[c4d.PRIM_CYLINDER_RADIUS] = totalWidth
    c4d.BaseObject.SetRelPos(cylinder, [0,0,-cylinderHeight/2])

    coneHeight = totalHeight/2
    cone[c4d.PRIM_CONE_HEIGHT] = coneHeight
    cone[c4d.PRIM_CONE_TRAD] = 5
    cone[c4d.PRIM_CONE_BRAD] = 100
    cone[c4d.PRIM_CONE_TOPFILLET] = True
    cone[c4d.PRIM_CONE_TOPFILLET_RADIUS] = 5
    cone[c4d.PRIM_CONE_TOPFILLET_HEIGHT] = 5
    cone[c4d.PRIM_CONE_SEG] = 32
    c4d.BaseObject.SetRelPos(cone, [0,0,coneHeight/2])

    lead[c4d.PRIM_CYLINDER_HEIGHT] = totalHeight + 2
    lead[c4d.PRIM_CYLINDER_RADIUS] = leadRadius

    extrude[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = totalHeight + 2
    c4d.BaseObject.SetRelPos(extrude, [0,0,(-totalHeight/2) - 1])

    spline[c4d.PRIM_NSIDE_RADIUS] = totalWidth
    spline[c4d.PRIM_NSIDE_RRADIUS] = 5
    spline[c4d.PRIM_NSIDE_ROUNDING] = True
    c4d.BaseObject.SetRelPos(spline, [0,0,0])

    leadHole[c4d.PRIM_CYLINDER_HEIGHT] = totalHeight + 2
    leadHole[c4d.PRIM_CYLINDER_RADIUS] = leadRadius + .005
    c4d.BaseObject.SetRelPos(leadHole, [0,0,-1])

        
