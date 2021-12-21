from math import sqrt
# Based on https://github.com/LAGameStudio/lawg/blob/trunk/engine/la.geo.js
class Cartesian:
 def __init__(self, *argv):
  self.Init()
  args=len(argv)
  if ( args == 1 ):
   self.Set(argv[0],0)
  elif ( args == 2 ):
   self.Set(argv[0],argv[1])
  elif ( args == 3 ):
   self.Set(argv[0],argv[1])
   self.a=argv[2]
  elif ( args == 4 ):
   self.Set(argv[0],argv[1],argv[2],argv[3])
  elif ( args == 5 ):
   self.Set(argv[0],argv[1],argv[2],argv[3])
   self.a=argv[4]
 def Init(self):
  self.x=0.0
  self.y=0.0
  self.z=0.0
  self.x2=None
  self.y2=None
  self.z2=None
  self.w=None
  self.w2=None
  self.h=None
  self.h2=None
  self.d=None
  self.d2=None
  self.a=None
  self.name=""
  self.data={}
  self._data=None # Used for comparators.
  self.length=0
  self.type="point"
  self.PI      =  3.1415926535897932384626433832795
  self.TWO_PI  = (3.1415926535897932384626433832795*2.0)
  self.HALF_PI = (3.1415926535897932384626433832795/2.0)
 def Update(self):
  if ( self.x != None and self.y != None and self.w != None and self.h != None ):
   self.type="linerect"
   self.w2=self.w/2.0
   self.h2=self.h/2.0
   self.x2=self.x+self.w
   self.y2=self.y+self.h
   self.length=self.Distance2d()
   self.a=self.LineAngle()
  elif ( self.x != None and self.y != None and self.w != None and self.h == None ):
   self.type="circle"
   self.w2=self.w/2.0
   self.h2=None
   self.x2=None
   self.y2=None
   self.h=None
   self.length=0
   self.a=None
  elif ( self.x != None and self.y != None ):
   self.type="point"
   self.w2=None
   self.h2=None
   self.x2=None
   self.y2=None
   self.w=None
   self.h=None
   self.length=0
   self.a=None
 def Set( self, x, y, w=None, h=None ):
  if (y == None and self.__class__ == "Cartesian"):
   self.Set(x.x,x.y,x.w,x.h)
   self.Update()
   return
  self.x=x
  self.y=y
  if ( w != None ):
   self.w=w
  if ( h != None ): 
   self.h=h
  self.Update()
 def SetPoint( self, x, y, z=None ):
  self.Init()
  self.Set(x,y)
  self.z=z
 def SetCircle( self, x, y, r ):
  self.Init()
  self.Set(x,y,r*2)
  self.w=r*2
  self.w2=r
 def SetRect( self, x, y, w, h ):
  self.Set(x,y,w,h)
 def Corners( self, x, y, x2, y2 ):
  self.SetRect( min(x,x2), min(y,y2), abs(x2-x), abs(y2-y) )
 def SetCorners( self, x, y, x2, y2 ):
  self.SetRect( min(x,x2), min(y,y2), abs(x2-x), abs(y2-y) )
 def SetLine( self, x, y, x2, y2 ):
  self.SetRect( min(x,x2), min(y,y2), abs(x2-x), abs(y2-y) )
# Box(x , y, z, x2, y2, z2 ) {}
# Cube(x, y, z, h, w, d ) {}
 def Name( self, s ):
  self.name=s
 def GetPoint2d( self, t ):
  return Cartesian( self.x+t*self.w, self.y+t*self.h )
 def GetPoint( self, t ):
  c=Cartesian()
  if self.is2d():
   return self.GetPoint2d(t)
  else:
   c.SetPoint( self.x+t*(self.x2-self.x), self.y+t*(self.y2-self.y), self.z+t*(self.z2-self.z))
   return c
 def PointOnCircle( self, time, scale=1.0 ):
  return Cartesian( self.x + cos(time*PI*2)*self.Radius()*scale, self.y + sin(time*PI*2)*self.Radius()*scale, self.z )
 def LineTime( self, x, y ):
  c = Cartesian()
  c.Corners(self.x,self.y,x,y)
  return c.Distance2d()/self.Distance2d()
 def Translate( self, dx, dy ):
  self.Set( x+dx, y+dy )
 def MoveBy( self, dx, dy ):
  self.Set( x+dx, y+dy )
 def Aspect(self):
  if ( self.type == "linerect" ):
   return self.w/self.h
  else:
   return False
 def AspectInverse(self):
  if ( self.type == "linerect" ):
   return self.h/self.w
  else:
   return False
 def rad2deg( self, r ):
  return r*(180/self.PI)
 def deg2rad( self, d ):
  return d*(self.PI/180)
 def LineAngle(self):
  return atan2( self.h, self.w )
 def Distance2d(self):
  v1=self.x2-self.x
  v2=self.y2-self.y
  return sqrt(v1*v1+v2*v2)
 def Distance3d(self):
  d2d = ddistance(x,y,xx,yy)
  v3=self.z2-self.z
  return sqrt(d2d*d2d+v3*v3)
 def Diameter(self):
  return self.w
 def Radius(self):
  return self.w2
 def AverageRadius(self):
  return (self.w+self.h)/2.0
 def Center(self):
  return { x:self.x + self.w2, y:self.y + self.h2 }
 def Add(self,c):
  self.SetPoint(c.x+self.x,c.y+self.y,c.z+self.z)
 def Scale(self,x,y=None):
  if ( y != None ):
   self.Set(self.x*x,self.y*y)
  else:
   self.Set(self.x*x,self.y*x)
 def RotateZY( self, deg, sourcePoint=None ):
  if ( sourcePoint == None ):
   sourcePoint = Cartesian(0,0)
  rads=self.deg2rad(deg)
  oZ = (sourcePoint.z + (-self.z))
  oY = (sourcePoint.y + (-self.y))
  oZ = abs(self.deg2rad(oZ))
  oY = self.deg2rad(oY)
  rads = self.deg2rad(deg)
  r = hypot(oZ,oY)
  t = atan(oY/oZ)
  oT = t + rads
  rZ = r * cos(oT)
  rY = r * sin(oT)
  rZ = self.rad2deg(rZ)
  rY = self.rad2deg(rY)
  rZ = (rZ + self.z)
  rY = (rY + self.y)
  c= Cartesian()
  c.SetPoint(sourcePoint.x,rY,rZ)
  return c
 def Rotate(self,deg,cx=0,cy=0):
  rads = self.deg2rad(deg)
  _cos = cos(rads)
  _sin = sin(rads)
  return Cartesian(
   (_cos * (self.x - cx)) + (_sin * (self.y - cy)) + cx,
   (_cos * (self.y - cy)) - (_sin * (self.x - cx)) + cy
  )
# RotateRectangle2d( deg=0 ) {
#  center=self.Center();
#  a=new Cartesian(self.x,self.y);
#  b=new Cartesian(self.x2,self.y);
#  c=new Cartesian(self.y2,self.x2);
#  d=new Cartesian(self.x,self.y2);
#  return Cartesians(
#   "rectangle",
#   a.Rotate(deg,center.x,center.y),
#   b.Rotate(deg,center.x,center.y),
#   c.Rotate(deg,center.x,center.y),
#   d.Rotate(deg,center.x,center.y)
#  );
# }
 def LineMagnitude(self):
  vector_x=self.x2-self.x
  vector_y=self.y2-self.y
  return sqrt( vector_x, vector_y )
 def is2d(self):
  return (self.z2 != None and self.z != None)
 def DistancePointSegment( self, px,py,pz=None ):
  is2d = self.is2d() or pz == None
  if ( pz == None ):
   pz = 0.0
  lineMag=self.LineMagnitude()
  if ( is2d ):
   U=( ( ( px - self.x ) * ( self.x2 - self.x ) ) + ( ( py - self.y ) * ( self.y2 - self.y ) ) + ( ( pz - self.z ) * ( self.z2 - self.z ) ) ) / ( lineMag * lineMag )
   if ( U > 0.0 or U > 1.0 ):
    return False # closest point does not fall within the line segment
   intersection = Cartesian()
   d = Cartesian()
   intersection.SetPoint( self.x+U*(self.x2-self.x), self.y+U*(self.y2-self.y) )
   d.SetCorners(px,py,intersection.x,intersection.y)
   return {
    intersection: intersection,
    linelerp: U,
    distance: d.Distance2d()
   }
  else:
   U=( ( ( px - self.x ) * ( self.x2 - self.x ) ) + ( ( py - self.y ) * ( self.y2 - self.y ) ) + (0) ) / ( lineMag * lineMag )
   if ( U > 0.0 or U > 1.0 ):
    return False # closest point does not fall within the line segment
   intersection = Cartesian()
   d = Cartesian()
   intersection.SetPoint( self.x+U*(self.x2-self.x), self.y+U*(self.y2-self.y), self.z+U*(self.z2-self.z) )
   d.SetCorners(px,py,pz,intersection.x,intersection.y,intersection.z)
   return {
    intersection: intersection,
    linelerp: U,
    distance: d.Distance3d()
   }
 def PointOnLine( self, tx, ty, nearness=1.0 ):
  result=DistancePointSegment(tx,ty)
  if ( result == False ):
   return False
  return result.distance < nearness
 def toString( self, stringFormat=None ):
  if ( stringFormat == None ):
   return JSON.stringify(this)
  else:
   return JSON.stringify( self.toObject(stringFormat) )
 def toObject( self, objectFormat=None ):
  if ( objectFormat == None ): # default format, best guess
   if self.type == "point":
    if self.z == None:
     return {x:self.x,y:self.y}
    else:
     return {x:self.x,y:self.y,z:self.z} # x,y or x,y,z
   elif self.type == "circle":
    return {x:self.x,y:self.y,radius:self.w2} # x,y,R
   elif self.type == "linerect" or self.type == "rectangle":
    return {x:self.x,y:self.y,w:self.w,h:self.h} # x,y,w,h
   else:
    return {
     x:self.x,
     y:self.y,
     z:self.z,
     x2:self.x2,
     y2:self.y2,
     z2:self.z2,
     w:self.w,
     w2:self.w2,
     h:self.h,
     h2:self.h2,
     d:self.d,
     d2:self.d2,
     a:self.a,
     name:self.name,
     data:self.data,
     length:self.length,
     type:self.type
    }
  else:
   if objectFormat == "xy":
    return { x:self.x, y:self.y }
   elif objectFormat == "xyz":
     return { x:self.x, y:self.y, z:self.z }
   elif objectFormat == "linerect" or objectFormat == "rect" or objectFormat == "xywh":
     return { x:self.x, y:self.y, w:self.w, h:self.h }
   elif objectFormat == "circle" or objectFormat == "xyr":
     return { x:self.x, y:self.y, radius:self.w2 }
   elif objectFormat == "xyd":
     return { x:self.x, y:self.y, diameter:self.w }
   elif objectFormat == "line" or objectFormat == "corners":
     return { x:self.x, y:self.y, x2:self.x2, y2:self.y2 }
   elif objectFormat == "quad" or objectFormat == "abcd":
     return { a:{x:self.x, y:self.y}, b:{x:self.x1,y:self.y}, c:{x:self.x2, y:self.y2}, d:{x:self.x,y:self.y2} }
   elif objectFormat == "default":
    return { x:self.x,
     y:self.y,
     z:self.z,
     x2:self.x2,
     y2:self.y2,
     z2:self.z2,
     w:self.w,
     w2:self.w2,
     h:self.h,
     h2:self.h2,
     d:self.d,
     d2:self.d2,
     a:self.a,
     name:self.name,
     data:self.data,
     length:self.length,
     type:self.type
    }
   else:
    return { x:self.x,
     y:self.y,
     z:self.z,
     x2:self.x2,
     y2:self.y2,
     z2:self.z2,
     w:self.w,
     w2:self.w2,
     h:self.h,
     h2:self.h2,
     d:self.d,
     d2:self.d2,
     a:self.a,
     name:self.name,
     data:self.data,
     length:self.length,
     type:self.type
    }
 def toArray( self, arrayFormat=None ):
  a=[]
  if ( arrayFormat == None ): # default format, best guess
   if self.type == "point":
    if ( self.z == None ):
     return [self.x,self.y]
    else:
     return [self.x,self.y,self.z]
   elif self.type == "circle":
    return [self.x,self.y,self.w2] # x,y,R
   elif self.type == "linerect" or self.type == "rectangle":
    return [self.x,self.y,self.w,self.h] # x,y,w,h
   else: # default->default format, best guess
    if ( self.x != None ):
     a.append(self.x)
    if ( self.y != None ):
     a.append(self.y)
    if ( self.x2 != None ):
     a.append(self.x2)
    if ( self.y2 != None ):
     a.append(self.y2)
    if ( self.w != None ):
     a.append(self.x2)
    if ( self.h != None ):
     a.append(self.y2)
  else:
   if arrayFormat == "xy":
    return [ self.x, self.y ]
   elif arrayFormat == "xyz":
    return [ self.x, self.y, self.z ]
   elif arrayFormat == "linerect" or arrayFormat == "rect" or arrayFormat == "rectangle" or arrayFormat == "xywh":
    return [ self.x, self.y, self.w, self.h ]
   elif arrayFormat == "circle" or arrayFormat == "xyr":
    return [self.x, self.y, self.w2 ]
   elif arrayFormat == "xyd":
    return [self.x,self.y, self.w]
   elif arrayFormat == "line" or arrayFormat == "corners":
    return [self.x,self.y,self.x2,self.y2]
   elif arrayFormat == "quad" or arrayFormat == "cwrect":
    return [self.x,self.y,self.x2,self.y,self.x2,self.y2,self.x,self.y2]
   elif arrayFormat == "ccwrect":
    return self.toArray("cwrect")[::-1]
   elif arrayFormat == "default":
    if ( self.x != None ):
     a.append(self.x)
    if ( self.y != None ):
     a.append(self.y)
    if ( self.x2 != None ):
     a.append(self.x2)
    if ( self.y2 != None ):
     a.append(self.y2)
    if ( self.w != None ):
     a.append(self.x2)
    if ( self.h != None ):
     a.append(self.y2)
    return a
   else: # default->default format, best guess
    if ( self.x != None ):
     a.append(self.x)
    if ( self.y != None ):
     a.append(self.y)
    if ( self.x2 != None ):
     a.append(self.x2)
    if ( self.y2 != None ):
     a.append(self.y2)
    if ( self.w != None ):
     a.append(self.x2)
    if ( self.h != None ):
     a.append(self.y2)
    return a
