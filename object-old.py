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
        
        # cube = c4d.BaseObject(c4d.Ocube)
        # cube.SetName("Test Cube")
        # cube.InsertUnder(nullObject)

        sharpLead = c4d.BaseObject(c4d.Oboole)
        sharpLead.SetName("Sharp Lead")
        sharpLead.InsertUnder(nullObject)
        sharpLead[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT

        lead = c4d.BaseObject(c4d.Ocylinder)
        lead.SetName("Lead")
        lead.InsertUnder(sharpLead)

        textag = c4d.TextureTag()
        textag.SetMaterial(matlist[0])
        textag[c4d.TEXTURETAG_PROJECTION]=c4d.TEXTURETAG_PROJECTION_CYLINDRICAL
        sharpLead.InsertTag(textag)

        cone = c4d.BaseObject(c4d.Ocone)
        cone.SetName("Lead Cone")
        cone[c4d.PRIM_CONE_HSUB] = 1
        cone[c4d.PRIM_CONE_SEG] = 32
        cone.InsertUnder(sharpLead)

        removeLead = c4d.BaseObject(c4d.Oboole)
        removeLead.SetName("Remove Lead")
        removeLead.InsertUnder(nullObject)
        removeLead[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_SUBTRACT

        leadRecess = c4d.BaseObject(c4d.Ocylinder)
        leadRecess.SetName("Lead")
        leadRecess.InsertUnder(removeLead)

        wood = c4d.BaseObject(c4d.Oboole)
        wood.SetName("Wood")
        wood.InsertUnder(removeLead)
        wood[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT
		
		#match = re.match(opname, mname)



        cone = c4d.BaseObject(c4d.Ocone)
        cone.SetName("Cone")
        cone[c4d.PRIM_CONE_HSUB] = 1
        cone[c4d.PRIM_CONE_SEG] = 64
        cone.InsertUnder(wood)

        textag = c4d.TextureTag()
        textag.SetMaterial(matlist[1])
        textag[c4d.TEXTURETAG_PROJECTION]=c4d.TEXTURETAG_PROJECTION_SPHERICAL
        cone.InsertTag(textag)

        extrude = c4d.BaseObject(c4d.Oextrude)
        extrude.SetName("Extrude")
        extrude.InsertUnder(wood)


        textag = c4d.TextureTag()
        textag.SetMaterial(matlist[random.randint(2,4)])
        textag[c4d.TEXTURETAG_PROJECTION]=c4d.TEXTURETAG_PROJECTION_CUBIC
        extrude.InsertTag(textag)

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

    sharpLead = getChildByName(nullObject, "Sharp Lead")

    lead = getChildByName(sharpLead, "Lead")
    lead[c4d.PRIM_CYLINDER_RADIUS] = rect.width/2 * .25
    lead[c4d.PRIM_CYLINDER_HEIGHT] = totalHeight - .8
    c4d.BaseObject.SetRelRot(lead, [1.5707963268,0,1.5707963268])
    c4d.BaseObject.SetRelPos(lead, [0,1,0])

    cone = getChildByName(sharpLead, "Lead Cone")
    c4d.BaseObject.SetRelRot(cone, [1.5707963268,0,1.5707963268])
    cone[c4d.PRIM_CONE_HEIGHT] = totalHeight - 1
    cone[c4d.PRIM_CONE_TRAD] = rect.width/2 * .2
    cone[c4d.PRIM_CONE_TOPFILLET] = True
    cone[c4d.PRIM_CONE_TOPFILLET_RADIUS] = rect.width/2 * .2

    c4d.BaseObject.SetRelPos(cone, [0,0,-rect.width/2 * .2 * 5])

    removeLead = getChildByName(nullObject, "Remove Lead")
    leadRecess = getChildByName(removeLead, "Lead")
    leadRecess[c4d.PRIM_CYLINDER_RADIUS] = (rect.width/2 * .25) * 1.025
    leadRecess[c4d.PRIM_CYLINDER_HEIGHT] = totalHeight - 1
    c4d.BaseObject.SetRelRot(leadRecess, [1.5707963268,0,1.5707963268])

    wood = getChildByName(removeLead, "Wood")

    cone = getChildByName(wood, "Cone")
    c4d.BaseObject.SetRelRot(cone, [1.5707963268,0,1.5707963268])
    cone[c4d.PRIM_CONE_HEIGHT] = totalHeight - 1

    extrude = getChildByName(wood, "Extrude")
    extrude[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = totalHeight
    c4d.BaseObject.SetRelPos(extrude, [0,0,-totalHeight/2])

    lead = getChildByName(removeLead, "Lead")
    c4d.BaseObject.SetRelPos(lead, [0,1,0])

    spline = getChildByName(extrude, "Spline")
    spline[c4d.PRIM_NSIDE_RADIUS] = (rect.width/2) - 2
    spline[c4d.PRIM_NSIDE_RRADIUS] = rect.width/2 * .2
    spline[c4d.PRIM_NSIDE_ROUNDING] = False
    c4d.BaseObject.SetRelPos(extrude, [0,0,-totalHeight/2])

    # cube = getChildByName(nullObject, "Test Cube")
   
    # cube[c4d.PRIM_CUBE_LEN, c4d.VECTOR_X] = rect.width
    # cube[c4d.PRIM_CUBE_LEN, c4d.VECTOR_Y] = 10
    # cube[c4d.PRIM_CUBE_LEN, c4d.VECTOR_Z] = rect.height

    c4d.BaseObject.SetRelPos(nullObject, [rect.center.x, rect.center.y + (rect.width/2) - 2, rect.center.z])
