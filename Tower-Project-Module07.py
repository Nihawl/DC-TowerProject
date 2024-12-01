#3D SURFACE MATRIX
#import modules
import rhinoscriptsyntax as rs
import random as rnd

def SurfacePoints(STRSRF, INTU, INTV):
    #create empty dictionary
    ptMTX = {}
    srfNorm01 = {}
    srfNorm02 = {}
    
    #find surface domain
    Udomain = rs.SurfaceDomain(STRSRF,0)
    Vdomain = rs.SurfaceDomain(STRSRF,1)
    
    #find step size
    UStep = (Udomain[1] - Udomain[0])/ INTU
    VStep = (Vdomain[1] - Vdomain[0])/ INTV
    
    #find exponential step value
    expStep = DivideExponentially((Udomain[1]-Udomain[0]), INTU)
    
    #PLOT POINTS ON SURFACE
    for i in range(INTU+1):
        for j in range(INTV+1):
            #define u and v in terms of i and j
            #u = Udomain[0] + UStep*i
            u = expStep[i]
            v = Vdomain[0] + VStep*j
            
            #evaluate surface
            point = rs.EvaluateSurface(STRSRF, u,v)
            #print point
            ptMTX[(i,j)] = point
            
            #find surface normals
            vecNorm = rs.SurfaceNormal(STRSRF, (u,v))
            print vecNorm
            #unitize vector for scaling
            vecNorm = rs.VectorUnitize(vecNorm)
            #make scale a factor of distance from plane
            plane = rs.WorldXYPlane()
            distance = rs.DistanceToPlane(plane, point)
            vecNorm = rs.VectorScale(vecNorm, 1)
            #add to srfNorm01
            srfNorm01[(i,j)] = rs.PointAdd(vecNorm,point)
            #unitize and scale vector
            vecNorm= rs.VectorUnitize(vecNorm)
            vecNorm = rs.VectorScale(vecNorm, 1)
            #add to srfNorm02
            srfNorm02[(i,j)] = rs.PointAdd(vecNorm,point)
            
    #call function to generate geometry
    GenerateGeometry(ptMTX, srfNorm02, srfNorm01, INTU, INTV)

def   GenerateGeometry(ptMTX, srfNorm02, srfNorm01, INTU, INTV):
    #LOOP TO GENERATE GEOMETRY
        for i in range(INTU + 1):
            for j in range(INTV + 1):
                if i > 0 and  j > 0 :
                    #set parameter 
                    tBack = 0.75 - (i*0.01)
                    ### CREATE BACK CURVE ###
                    #create back points
                    #create lines
                    crv01 = rs.AddCurve((ptMTX[(i-1,j-1)],ptMTX[(i,j-1)],ptMTX[(i,j)]),1)
                    crv02 = rs.AddCurve((ptMTX[(i-1,j-1)],ptMTX[(i-1,j)],ptMTX[(i,j)]),1)
                    t01 = rs.CurveParameter(crv01, tBack)
                    t02 = rs.CurveParameter(crv02, tBack)
                    pt01 = rs.EvaluateCurve(crv01,t01)
                    pt02 = rs.EvaluateCurve(crv02,t02)
                    #create curve
                    backCrv = rs.AddCurve((ptMTX[(i,j-1)],ptMTX[(i-1,j-1)],ptMTX[(i-1,j)]),1)
                    
                    ### CREATE FRONT CURVE ###
                    #create front points
                    tFront = (tBack - 0.1) - (i*0.01)
                    crv03 = rs.AddCurve((srfNorm01[(i-1,j-1)],srfNorm01[(i,j)]))
                    t03 = rs.CurveParameter(crv03, tFront)
                    pt03 = rs.EvaluateCurve(crv03,t03)
                    frontCrv = rs.AddCurve((pt01,pt03,pt02),2)
                    #loft
                    module = rs.AddLoftSrf((backCrv,frontCrv),None, None,1,0)
                    
                    #delete 
                    rs.DeleteObjects((crv03,frontCrv,backCrv,crv01,crv02))




def MidPt(PT01, PT02):
    
    point = None
    point = [(PT01[0] + PT02[0])/2,(PT01[1] + PT02[1])/2,(PT01[2] + PT02[2])/2]
    return point

def DivideExponentially(maxLength, Divisions):
    #set-up lists
    point = []
    yVal = []
    
    #create point where x is .72 of Vdomain and y and z are 0 (point[0])
    pt = ([(maxLength*.72), 0, 0])
    #rs.AddPoint(pt)
    point.append(pt)
    
    #create point where x and y are .12 of model curve length and z is 0 (point[1])
    pt = ([(maxLength*.12), (maxLength*.12), 0])
    #rs.AddPoint(pt)
    point.append(pt)
    
    #create point where y is model curve length and x and z are 0 (point[2])
    pt = ([0, maxLength, 0])
    #rs.AddPoint(pt)
    point.append(pt)
    
    #draw a curve between the three points (GRAPHcrvGUID)
    GRAPHcrvGUID = rs.AddCurve(point)
    
    #divide (GRAPHcrvGUID)
    GRAPHpoints = rs.DivideCurve(GRAPHcrvGUID, Divisions, False, True)
    
    #delete curve
    rs.DeleteObject(GRAPHcrvGUID)
    
    #collect y values in a list
    for i in range(len(GRAPHpoints)):
        yVal.append(GRAPHpoints[i][1])
        
    return yVal
                  
def main():
    #collect data
    #strSRF = rs.GetObject('select surface', rs.filter.surface)
    strSRFs = rs.GetObjects('select surfaces', rs.filter.surface)
    intU = rs.GetInteger('how many U intervals?', 8)
    intV = rs.GetInteger('how many V intervals?', 2)
    #    rs.HideObject(strSRF)
    #    #call function
    #    rs.EnableRedraw(False)
    #    SurfacePoints(strSRF, intU, intV)
    #    rs.EnableRedraw(True)
    
    #call function with multiple surfaces
    rs.EnableRedraw(False)
    for strSRF in strSRFs:
        #rs.HideObject(strSRF)
        #call function
        SurfacePoints(strSRF, intU, intV)
    rs.EnableRedraw(True)

main()