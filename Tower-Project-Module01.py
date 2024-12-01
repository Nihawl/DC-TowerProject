#TOWER ASSIGNMENT
#import modules
import rhinoscriptsyntax as rs
import random as rnd

#Divide Surface to Cubes and add text dots
#Define each modular unit geometry 

def SurfacePoints(STRSRF, INTU, INTV):
    #create empty dictionary
    ptMTX = {}
    srfNorm = {}
    
    #find domain of surface
    Udomain = rs.SurfaceDomain(STRSRF, 0)
    Vdomain = rs.SurfaceDomain(STRSRF, 1)   
    
    #calculate step value
    UStep = (Udomain[1] - Udomain[0]) / INTU
    VStep = (Vdomain[1] - Vdomain[0]) / INTV
    
    #Calculate exponential step
    exp_Step = DivideExponentially((Udomain[1] - Udomain[0]), INTU)
    
    #Plot points on surface
    for i in range(INTU + 1):
        for j in range(INTV + 1):
            #define u and v in terms of i and j
            #u = Udomain[0] + UStep * i
            u = exp_Step[i] 
            v = Vdomain[0] + VStep * j
            
            #evaluate surface
            point = rs.EvaluateSurface(STRSRF, u, v)
            ptMTX[(i,j)] = point
            
            #find surface normal at parameters
            vecNorm = rs.SurfaceNormal(STRSRF, (u,v))
            #scale vector
            vecNorm = rs.VectorUnitize(vecNorm)
            vecNorm = rs.VectorScale(vecNorm, 2)
            vecNorm = rs.PointAdd(vecNorm, point)
            srfNorm[(i,j)] = vecNorm
            
    #Add text dots
    #for i in range(INTU+1):
        #for j in range(INTV+1):
            #rs.AddTextDot((i,j),ptMTX[(i,j)])
            #rs.AddTextDot((i,j),srfNorm[(i,j)])
    #call function to create geometry
    GenerateGeometry_Pattern1(ptMTX, srfNorm, INTU, INTV)

#CREATE PATTERN 01 FUNCTION
#def GenerateGeometry_Pattern1(ptMTX, srfNorm, INTU, INTV):
#    for i in range(INTU + 1):
#        for j in range(INTV + 1):
#            if i > 0 and j > 0:
#            #create back curve
#                midpt_Back = MidPt(srfNorm[(i-1,j-1)], srfNorm[(i-1,j)])
#                crv_Back = rs.AddCurve((ptMTX[(i-1,j-1)],midpt_Back, ptMTX[(i-1,j)]),3)
#            #create front curve
#                midpt_Front = MidPt(srfNorm[(i,j-1)], srfNorm[(i,j)])
#                crv_Front = rs.AddCurve((ptMTX[(i-1,j-1)],midpt_Front, ptMTX[(i,j-1)]),3)
#                #Loft
#                module = rs.AddLoftSrf((crv_Back,crv_Front),None, None, 2)
#                module = rs.FlipSurface(module, True)

#CREATE PATTERN 02 FUNCTION
def GenerateGeometry_Pattern1(ptMTX, srfNorm, INTU, INTV):
    for i in range(INTU + 1):
        for j in range(INTV + 1):
            if i > 0 and j > 0:
                #Create front point grid
                #create point 01
                crv_01 = rs.AddCurve((srfNorm[(i-1, j)],srfNorm[(i, j-1)]),1)
                pt_01 = rs.EvaluateCurve(crv_01, 2)
                pt_01 = rs.AddPoint(pt_01)
                #create point 02
                crv_02 = rs.AddCurve((srfNorm[(i-1, j-1)],srfNorm[(i, j)]),1)
                pt_02 = rs.EvaluateCurve(crv_02, 2)
                pt_02 = rs.AddPoint(pt_02)
                #create point 03
                mid_end = MidPt(srfNorm[(i-1,j-1)], srfNorm[(i-1,j)])
                mid_start = MidPt(srfNorm[(i,j-1)], srfNorm[(i,j)])
                crv_03 = rs.AddCurve((mid_start, mid_end),1)
                pt_03 = rs.EvaluateCurve(crv_03, 2)
                pt_03 = rs.AddPoint(pt_03)
                
                #Create Surfaces
                srf_01 = rs.AddSrfPt((ptMTX[(i-1,j-1)],pt_02,pt_01,ptMTX[(i-1,j)]))
                
                #srf_02 = rs.AddSrfPt((ptMTX[(i-1,j-1)],pt_02,pt_03,ptMTX[(i,j-1)]))
                srf_02 = rs.AddSrfPt((ptMTX[(i,j-1)],pt_03,pt_02,ptMTX[(i-1,j-1)]))
                
                #srf_03 = rs.AddSrfPt((ptMTX[(i,j-1)],pt_03,ptMTX[(i,j)]))
                srf_03 = rs.AddSrfPt((ptMTX[(i,j)],pt_03,ptMTX[(i,j-1)]))
                
                #srf_04 = rs.AddSrfPt((ptMTX[(i,j)],pt_03,pt_01,ptMTX[(i-1,j)]))
                srf_04 = rs.AddSrfPt((ptMTX[(i-1,j)],pt_01,pt_03,ptMTX[(i,j)]))
                
                #Delete curves
                rs.DeleteObjects((crv_01,crv_02,crv_03))
                rs.DeleteObjects((pt_01, pt_02,pt_03))


#GET MIDPOINT FUNCTION
def MidPt(PT01, PT02):
        point = None
        #calculate midpoint position
        point = [(PT01[0] + PT02[0]) / 2,(PT01[1] + PT02[1]) / 2,
        (PT01[2] + PT02[2]) / 2]
        return point

#DIVIDE EXPONENTIALLY FUNCTION
def DivideExponentially(maxLength, Divisions):
    ##input curve
    #crv = rs.GetObject('Select Curve', rs.filter.curve)
    ##get length
    #maxLength = rs.CurveLength(crv)
    #
    ##input number of divisions
    #Divisions = rs.GetInteger('Enter number of divisions',8)
    
    #set up lists
    point = []
    yVal = []
    
    #create point where x is .72 of Vdomain and y and z are 0 (point[0])
    pt = ([(maxLength*.72),0,0])
    rs.AddPoint(pt)
    point.append(pt)
    
    #create point where x and y are .12 of model curve length and z is 0 (point[1])
    pt = ([(maxLength*.12),(maxLength*.12),0])
    rs.AddPoint(pt)
    point.append(pt)
    
    #create point where y is model curve length and x and z are 0 (point[2])
    pt = ([0,maxLength,0])
    rs.AddPoint(pt)
    point.append(pt)
    
    #draw a curve between the three points
    GRAPHcrvGUID = rs.AddCurve(point)
    #divide curve
    crvPoints = rs.DivideCurve(GRAPHcrvGUID, Divisions, True, True)
    
    #collect y-values
    for i in range(len(crvPoints)):
        yVal.append(crvPoints[i][1])
        
    return yVal
#
def main():
    #input values
    strSRF = rs.GetObject('Select Surface')
    intU = rs.GetInteger('Input u-interval',8)
    intV = rs.GetInteger('Input v-interval',8)
    rs.HideObject(strSRF)
    rs.EnableRedraw(False)
    SurfacePoints(strSRF, intU, intV)
    rs.EnableRedraw(True)

main()    

