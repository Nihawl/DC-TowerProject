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
            vecNorm = rs.VectorScale(vecNorm, 1.4)
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
                    ### Create firstCrv Curve ### 
                    firstCrv = rs.AddCurve((ptMTX[(i,j-1)],ptMTX[(i,j)],ptMTX[(i-1,j)],
                    ptMTX[(i-1,j-1)],ptMTX[(i,j-1)]),1)
                    ### Create secondCrv ###
                    #create construction surface to get grid of points
                    srf = rs.AddSrfPt((srfNorm01[(i,j-1)],srfNorm01[(i,j)],srfNorm01[(i-1,j)],
                    srfNorm01[(i-1,j-1)]))
                    #create grid of points, rebuild to get (3x3) grid
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from surface
                    pts = rs.SurfacePoints(srf)
                    rs.DeleteObject(srf)
                    #create curves
                    midpoint01 = MidPt(pts[1], pts[6])
                    midpoint02 = MidPt(pts[13], pts[10])
                    centroid = MidPt(pts[6], pts[9])
                    secondCrv = rs.AddCurve((pts[5], pts[9], midpoint02,pts[10],
                    pts[6],midpoint01, pts[5]),3)
                    #scale curve
                    secondCrv =rs.ScaleObject(secondCrv,centroid ,(1.2,1.2,1.2))
                    ### Create thirdCrv ###
                    #create construction surface
                    srf = rs.AddSrfPt((srfNorm02[(i,j-1)],srfNorm02[(i,j)],srfNorm02[(i-1,j)],
                    srfNorm02[(i-1,j-1)]))
                    #rebuild to get (3x3) grid
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from surface
                    pts = rs.SurfacePoints(srf)
                    rs.DeleteObject(srf)
                    #create curves
                    midpoint01 = MidPt(pts[1], pts[6])
                    midpoint02 = MidPt(pts[13], pts[10])
                    centroid = MidPt(pts[6], pts[9])
                    thirdCrv = rs.AddCurve((pts[5], pts[9], midpoint02,pts[10],
                    pts[6],midpoint01, pts[5]),3)
                    #scale curve
                    thirdCurve = rs.ScaleObject(thirdCrv, centroid,(0.7,0.7,0.7))
                    ### CREATE MODULE USING LOFT ###
                    #flip direction of curves
                    #rs.ReverseCurve(firstCrv)
                    #rs.ReverseCurve(secondCrv)
                    #rs.ReverseCurve(thirdCrv)
                    #loft curves to create surfaces
                    module = rs.AddLoftSrf((firstCrv,secondCrv,thirdCrv), None, None,1,0)
                    
                    #add color to module
                    #rs.ObjectColor(module, (255/INTU*i, 255-(255/INTU)*i,255/INTU*i))
                    
                    rs.DeleteObjects((firstCrv,secondCrv,thirdCurve))

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
        rs.HideObject(strSRF)
        #call function
        SurfacePoints(strSRF, intU, intV)
    rs.EnableRedraw(True)

main()