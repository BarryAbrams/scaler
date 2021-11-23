import c4d, math, imp
from c4d import utils

def createObject(op, obj, polyID, rect):
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
        
        # cube = c4d.BaseObject(c4d.Ocube)
        # cube.SetName("Test Cube")
        # cube.InsertUnder(nullObject)

        bool = c4d.BaseObject(c4d.Oboole)
        bool.SetName("Bool")
        bool.InsertUnder(nullObject)
        bool[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT

        lead = c4d.BaseObject(c4d.Ocylinder)
        lead.SetName("Lead")
        lead.InsertUnder(nullObject)

        cone = c4d.BaseObject(c4d.Ocone)
        cone.SetName("Cone")
        cone.InsertUnder(bool)

        extrude = c4d.BaseObject(c4d.Oextrude)
        extrude.SetName("Extrude")
        extrude.InsertUnder(bool)

        spline = c4d.BaseObject(c4d.Osplinenside)
        spline.SetName("Spline")
        spline.InsertUnder(extrude)
        
    else:
        nullObject = foundItem
        #print("known")

    padding = 10
    totalHeight = rect.height - padding
        
    nullObject[c4d.NULLOBJECT_DISPLAY] = c4d.NULLOBJECT_DISPLAY_POINT
    nullObject[c4d.NULLOBJECT_RADIUS] = 5

    lead = getChildByName(nullObject, "Lead")
    lead[c4d.PRIM_CYLINDER_RADIUS] = rect.width/2 * .2
    lead[c4d.PRIM_CYLINDER_HEIGHT] = totalHeight
    c4d.BaseObject.SetRelRot(lead, [1.5707963268,0,1.5707963268])

    bool = getChildByName(nullObject, "Bool")

    cone = getChildByName(bool, "Cone")
    c4d.BaseObject.SetRelRot(cone, [1.5707963268,0,1.5707963268])
    cone[c4d.PRIM_CONE_HEIGHT] = totalHeight - 1

    extrude = getChildByName(bool, "Extrude")
    extrude[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = totalHeight
    c4d.BaseObject.SetRelPos(extrude, [0,0,-totalHeight/2])

    spline = getChildByName(extrude, "Spline")
    spline[c4d.PRIM_NSIDE_RADIUS] = rect.width/2
    spline[c4d.PRIM_NSIDE_RRADIUS] = rect.width/2 * .2
    spline[c4d.PRIM_NSIDE_ROUNDING] = True
    c4d.BaseObject.SetRelPos(extrude, [0,0,-totalHeight/2])

    # cube = getChildByName(nullObject, "Test Cube")
   
    # cube[c4d.PRIM_CUBE_LEN, c4d.VECTOR_X] = rect.width
    # cube[c4d.PRIM_CUBE_LEN, c4d.VECTOR_Y] = 10
    # cube[c4d.PRIM_CUBE_LEN, c4d.VECTOR_Z] = rect.height

    c4d.BaseObject.SetRelPos(nullObject, rect.center)
