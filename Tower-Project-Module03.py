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
                    ptMTX[(i-1,j-1)],ptMTX[(i,j-1)]),2)
                    
                    #create construction surface to get grid of points for NormSurface01
                    srf01 = rs.AddSrfPt((srfNorm01[(i,j-1)],srfNorm01[(i,j)],srfNorm01[(i-1,j)],
                    srfNorm01[(i-1,j-1)]))
                    #create grid of points, rebuild to get (3x3) grid
                    rs.RebuildSurface(srf01, (3,3), (4,4))
                    #extract points from surface
                    pts01 = rs.SurfacePoints(srf01)
                    rs.DeleteObject(srf01)
                    
                    #create construction surface to get grid of points for NormSurface02
                    srf02 = rs.AddSrfPt((srfNorm02[(i,j-1)],srfNorm02[(i,j)],srfNorm02[(i-1,j)],
                    srfNorm02[(i-1,j-1)]))
                    #create grid of points, rebuild to get (3x3) grid
                    rs.RebuildSurface(srf02, (3,3), (4,4))
                    #extract points from surface
                    pts02 = rs.SurfacePoints(srf02)
                    rs.DeleteObject(srf02)
                    
                    #generate random numbers
                    quadNum = rnd.randint(1,4)
                    #create curves according to random number
                    if quadNum == 1:
                        #secondCrv
                        pt01 = MidPt(pts01[5],pts01[1])
                        pt02 = MidPt(pts01[9],pts01[13])
                        pt03 = MidPt(pts01[10],pts01[11])
                        secondCrv = rs.AddCurve((pt01,pt02,pt03,pt01),2)
                        centroid = rs.CurveAreaCentroid(secondCrv)[0]
                        secondCrv = rs.ScaleObject(secondCrv,centroid,(2,2,2))
                        #thirdCrv
                        pt04 = MidPt(pts02[5],pts02[1])
                        pt05 = MidPt(pts02[9],pts02[13])
                        pt06 = MidPt(pts02[10],pts02[11])
                        thirdCrv = rs.AddCurve((pt04,pt05,pt06,pt04),2)
                        centroid = rs.CurveAreaCentroid(thirdCrv)[0]
                        thirdCrv = rs.ScaleObject(thirdCrv, centroid, (1.2,1.2,1.2))
                    if quadNum == 2:
                        #secondCrv
                        pt01 = MidPt(pts01[5],pts01[1])
                        pt02 = MidPt(pts01[9],pts01[13])
                        pt03 = MidPt(pts01[6],pts01[7])
                        secondCrv = rs.AddCurve((pt01,pt02,pt03,pt01),2)
                        centroid = rs.CurveAreaCentroid(secondCrv)[0]
                        secondCrv = rs.ScaleObject(secondCrv,centroid,(2,2,2))
                        #thirdCrv
                        pt04 = MidPt(pts02[5],pts02[1])
                        pt05 = MidPt(pts02[9],pts02[13])
                        pt06 = MidPt(pts02[6],pts02[7])
                        thirdCrv = rs.AddCurve((pt04,pt05,pt06,pt04),2)
                        centroid = rs.CurveAreaCentroid(thirdCrv)[0]
                        thirdCrv = rs.ScaleObject(thirdCrv, centroid, (1.2,1.2,1.2))
                    if quadNum == 3:
                        #secondCrv
                        pt01 = MidPt(pts01[5],pts01[1])
                        pt02 = MidPt(pts01[9],pts01[13])
                        pt03 = MidPt(pts01[6],pts01[11])
                        secondCrv = rs.AddCurve((pt01,pt02,pt03,pt01),2)
                        centroid = rs.CurveAreaCentroid(secondCrv)[0]
                        secondCrv = rs.ScaleObject(secondCrv,centroid,(2,2,2))
                        #thirdCrv
                        pt04 = MidPt(pts02[5],pts02[1])
                        pt05 = MidPt(pts02[9],pts02[13])
                        pt06 = MidPt(pts02[6],pts02[11])
                        thirdCrv = rs.AddCurve((pt04,pt05,pt06,pt04),2)
                        centroid = rs.CurveAreaCentroid(thirdCrv)[0]
                        thirdCrv = rs.ScaleObject(thirdCrv, centroid, (1.2,1.2,1.2))
                    if quadNum == 4:
                        #secondCrv
                        pt01 = MidPt(pts01[9],pts01[13])
                        pt02 = MidPt(pts01[10],pts01[15])
                        pt03 = MidPt(pts01[6],pts01[3])
                        secondCrv = rs.AddCurve((pt01,pt02,pt03,pt01),2)
                        centroid = rs.CurveAreaCentroid(secondCrv)[0]
                        secondCrv = rs.ScaleObject(secondCrv,centroid,(2,2,2))
                        #thirdCrv
                        pt04 = MidPt(pts02[9],pts02[13])
                        pt05 = MidPt(pts02[10],pts02[15])
                        pt06 = MidPt(pts02[6],pts02[3])
                        thirdCrv = rs.AddCurve((pt04,pt05,pt06,pt04),2)
                        centroid = rs.CurveAreaCentroid(thirdCrv)[0]
                        thirdCrv = rs.ScaleObject(thirdCrv, centroid, (1.2,1.2,1.2))
                        
                    ### CREATE MODULE USING LOFT ###
                    #flip direction of curves
                    rs.ReverseCurve(firstCrv)
                    rs.ReverseCurve(secondCrv)
                    rs.ReverseCurve(thirdCrv)
                    #loft curves to create surfaces
                    module = rs.AddLoftSrf((firstCrv,secondCrv,thirdCrv), None, None,1,0)
                    #delete curves
                    rs.DeleteObjects((firstCrv, secondCrv, thirdCrv))
                    #add color to module
                    #rs.ObjectColor(module, (255/INTU*i, 255-(255/INTU)*i,255/INTU*i))

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