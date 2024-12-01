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
                    #Set "t" value
                    t = 0.02*i
                    ##Back points
                    backPts = []
                    backCentroid = MidPt(ptMTX[(i,j-1)],ptMTX[(i-1,j)])
                    midPt01 = MidPt(ptMTX[(i,j-1)],ptMTX[(i,j)])
                    midPt02 = MidPt(ptMTX[(i,j)],ptMTX[(i-1,j)])
                    midPt03 = MidPt(ptMTX[(i-1,j)],ptMTX[(i-1,j-1)])
                    midPt04 = MidPt(ptMTX[(i-1,j-1)],ptMTX[(i,j-1)])
                    backLn01 = rs.AddLine(midPt01,backCentroid)
                    backLn02 = rs.AddLine(midPt02,backCentroid)
                    backLn03 = rs.AddLine(midPt03,backCentroid)
                    backLn04 = rs.AddLine(midPt04,backCentroid)
                    backPt01 = rs.EvaluateCurve(backLn01,(rs.CurveParameter(backLn01,t*0.5)))
                    backPt02 = rs.EvaluateCurve(backLn02,(rs.CurveParameter(backLn02,t*0.5)))
                    backPt03 = rs.EvaluateCurve(backLn03,(rs.CurveParameter(backLn04,t*0.5)))
                    backPt04 = rs.EvaluateCurve(backLn04,(rs.CurveParameter(backLn04,t*0.5)))
                    
                    ##Front points
                    frontPts = []
                    frontCentroid = MidPt(srfNorm01[(i,j-1)],srfNorm01[(i-1,j)])
                    frontLn01 = rs.AddLine(srfNorm01[(i,j-1)],frontCentroid)
                    frontLn02 = rs.AddLine(srfNorm01[(i,j)],frontCentroid)
                    frontLn03 = rs.AddLine(srfNorm01[(i-1,j)],frontCentroid)
                    frontLn04 = rs.AddLine(srfNorm01[(i-1,j-1)],frontCentroid)
                    frontPt01 = rs.EvaluateCurve(frontLn01,(rs.CurveParameter(frontLn01,t*2)))
                    frontPt02 = rs.EvaluateCurve(frontLn02,(rs.CurveParameter(frontLn02,t*2)))
                    frontPt03 = rs.EvaluateCurve(frontLn03,(rs.CurveParameter(frontLn03,t*2)))
                    frontPt04 = rs.EvaluateCurve(frontLn04,(rs.CurveParameter(frontLn04,t*2)))
                    
                    ## Create Surfaces
                    srf01 = rs.AddSrfPt((midPt01,backPt01,frontPt01,ptMTX[(i,j-1)]))
                    #srf02 = rs.AddSrfPt((ptMTX[(i,j-1)],midPt04,backPt04,frontPt01))
                    srf02 = rs.AddSrfPt((midPt04,ptMTX[(i,j-1)],frontPt01,backPt04))
                    srf03 = rs.AddSrfPt((ptMTX[(i-1,j-1)],midPt04,backPt04,frontPt04))
                    srf04 = rs.AddSrfPt((ptMTX[(i-1,j-1)],midPt04,backPt04,frontPt04))
                    #srf05 = rs.AddSrfPt((ptMTX[(i-1,j-1)],midPt03,backPt03,frontPt04))
                    srf05 = rs.AddSrfPt((midPt03,ptMTX[(i-1,j-1)],frontPt04,backPt03))
                    srf06 = rs.AddSrfPt((ptMTX[(i-1,j)],midPt03,backPt03,frontPt03))
                    #srf07 = rs.AddSrfPt((ptMTX[(i-1,j)],midPt02,backPt02,frontPt03))
                    srf07 = rs.AddSrfPt((midPt02,ptMTX[(i-1,j)],frontPt03,backPt02))
                    srf08 = rs.AddSrfPt((ptMTX[(i,j)],midPt02,backPt02,frontPt02))
                    #srf09 = rs.AddSrfPt((ptMTX[(i,j)],midPt01,backPt01,frontPt02))
                    srf09 = rs.AddSrfPt((midPt01,ptMTX[(i,j)],frontPt02,backPt01))
                    
                    #Delete Objects
                    rs.DeleteObjects((backLn01,backLn02,backLn03,backLn04,frontLn01,
                    frontLn02,frontLn03,frontLn04))
                    
                    





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