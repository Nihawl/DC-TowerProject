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
                    
                    ###Create Front Points###
                    #create centre lines from midpoints
                    midpoint01 = MidPt(srfNorm01[(i,j-1)],srfNorm01[(i,j)])
                    midpoint02 = MidPt(srfNorm01[(i,j)],srfNorm01[(i-1,j)])
                    midpoint03 = MidPt(srfNorm01[(i-1,j)],srfNorm01[(i-1,j-1)])
                    midpoint04 = MidPt(srfNorm01[(i-1,j-1)],srfNorm01[(i,j-1)])
                    line01 = rs.AddLine(midpoint01,midpoint03)
                    line02 = rs.AddLine(midpoint02,midpoint04)
                    #create points at parameter t
                    t = 0.4
                    t01 = rs.CurveParameter(line01, t)
                    t02 = rs.CurveParameter(line02, t)
                    t03 = rs.CurveParameter(line01, 1-t)
                    t04 = rs.CurveParameter(line02, 1-t)
                    pt01 = rs.EvaluateCurve(line01,t01)
                    pt02 = rs.EvaluateCurve(line02,t02)
                    pt03 = rs.EvaluateCurve(line01,t03)
                    pt04 = rs.EvaluateCurve(line02,t04)
                    rs.AddPoint(pt01)
                    rs.AddPoint(pt02)
                    rs.AddPoint(pt03)
                    rs.AddPoint(pt04)
                    #rs.AddTextDot('pt01',pt01)
                    #rs.AddTextDot('pt02',pt02)
                    #rs.AddTextDot('pt03',pt03)
                    #rs.AddTextDot('pt04',pt04)
                    
                    ###Create Surfaces From Points###
                    srf01 = rs.AddSrfPt((ptMTX[(i,j-1)],pt04,ptMTX[(i-1,j-1)]))
                    srf02 = rs.AddSrfPt((ptMTX[(i,j)],pt01,ptMTX[(i,j-1)]))
                    srf03 = rs.AddSrfPt((ptMTX[(i-1,j)],pt02,ptMTX[(i,j)]))
                    srf04 = rs.AddSrfPt((ptMTX[(i-1,j-1)],pt03,ptMTX[(i-1,j)]))
                    




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