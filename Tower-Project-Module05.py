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
                    ### Create Back Curve ### 
                    backCrv = rs.AddCurve((ptMTX[(i,j-1)],ptMTX[(i,j)],ptMTX[(i-1,j)],
                    ptMTX[(i-1,j-1)],ptMTX[(i,j-1)]),1)
                    
                    ###Create Back Points###
                    #create centre lines from midpoints
                    lines = []
                    midPts = []
                    midpoint01 = MidPt(ptMTX[(i,j-1)],ptMTX[(i,j)])
                    midpoint02 = MidPt(ptMTX[(i,j)],ptMTX[(i-1,j)])
                    midpoint03 = MidPt(ptMTX[(i-1,j)],ptMTX[(i-1,j-1)])
                    midpoint04 = MidPt(ptMTX[(i-1,j-1)],ptMTX[(i,j-1)])
                    lines.append(rs.AddLine(midpoint01,midpoint02))
                    lines.append(rs.AddLine(midpoint02,midpoint03))
                    lines.append(rs.AddLine(midpoint03,midpoint04))
                    lines.append(rs.AddLine(midpoint04,midpoint01))
                    centroidBack= MidPt(ptMTX[(i,j-1)],ptMTX[(i-1,j)])
                    rs.AddPoint(centroidBack)
                    #find points for each line at parameter t 
                    for line in lines:
                        t = 0.2
                        t01 = rs.CurveParameter(line, t)
                        t02 = rs.CurveParameter(line, 1-t)
                        midPts.append(rs.AddPoint(rs.EvaluateCurve(line, t01)))
                        midPts.append(rs.AddPoint(rs.EvaluateCurve(line, t02)))
                        print midPts
                    #find mid point on normSrf01
                    centroidFront = MidPt(srfNorm01[(i,j-1)],srfNorm01[(i-1,j)])
                    #Create Surfaces
                    srf01 = rs.AddSrfPt((srfNorm01[(i,j)], midPts[1],centroidFront))
                    srf02 = rs.AddSrfPt((centroidFront, midPts[0],srfNorm01[(i,j)],))
                    srf03 = rs.AddSrfPt((centroidFront, midPts[2],srfNorm01[(i-1,j)]))
                    srf04 = rs.AddSrfPt((srfNorm01[(i-1,j)], midPts[3],centroidFront))
                    srf05 = rs.AddSrfPt((centroidFront, midPts[4],srfNorm01[(i-1,j-1)]))
                    srf06 = rs.AddSrfPt((srfNorm01[(i-1,j-1)], midPts[5],centroidFront))
                    srf07 = rs.AddSrfPt((centroidFront, midPts[6],srfNorm01[(i,j-1)]))
                    srf08 = rs.AddSrfPt((srfNorm01[(i,j-1)], midPts[7],centroidFront))






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