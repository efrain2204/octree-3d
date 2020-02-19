import vtk
colors = vtk.vtkNamedColors()

class Point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def printp(self): 
        print("(",self.x,",",self.y,",",self.z,")") 

    def imprimir(self,ren):
        #sphere
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(self.x, self.y, self.z)
        sphereSource.SetRadius(5)
        # Make the surface smooth.
        sphereSource.SetPhiResolution(100)
        sphereSource.SetThetaResolution(100)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphereSource.GetOutputPort())

        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper)
        actor2.GetProperty().SetColor(colors.GetColor3d('White'))
        ren.AddActor(actor2)
        
class Prism:
    def __init__(self,x,y,z,w,h,l):
        self.x=x
        self.y=y
        self.z=z
        self.w=w
        self.h=h
        self.l=l
    def contains(self,point):
        if point.x<self.x+self.w and point.x>self.x-self.w and point.y<self.y+self.h and point.y>self.y-self.h and point.z<self.z+self.l and point.z>self.z-self.l:
            return True
        return False
    def intersects(self,rang):
        return not(rang.x-rang.w>self.x+self.w or rang.x+rang.w<self.x-self.w or rang.y-rang.h>self.y+self.h or rang.y+rang.h<self.y-self.h or rang.z-rang.l>self.z+self.l or rang.z+rang.l<self.z-self.l)
class OctTree:
    def __init__(self,boundary,n,ren):
        self.boundary=boundary
        self.capacity=n
        self.points=[]
        self.divided=False
        #random color 
        r = 1
        g = 1
        b = 1
        #cube
        cube = vtk.vtkCubeSource()
        cube.SetXLength(self.boundary.w*2)
        cube.SetYLength(self.boundary.h*2)
        cube.SetZLength(self.boundary.l*2)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(r, g, b)
        actor.GetProperty().SetOpacity(0.2)
        actor.SetPosition(self.boundary.x, self.boundary.y, self.boundary.z)
        actor.RotateX(0)
        actor.RotateY(0)
        actor.RotateZ(0)
        ren.AddActor(actor)

        
    def subdivide(self,ren):
        self.sonAXC=OctTree(Prism(self.boundary.x+self.boundary.w/2,self.boundary.y+self.boundary.h/2,self.boundary.z+self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonAXD=OctTree(Prism(self.boundary.x+self.boundary.w/2,self.boundary.y+self.boundary.h/2,self.boundary.z-self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonAYC=OctTree(Prism(self.boundary.x+self.boundary.w/2,self.boundary.y-self.boundary.h/2,self.boundary.z+self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonAYD=OctTree(Prism(self.boundary.x+self.boundary.w/2,self.boundary.y-self.boundary.h/2,self.boundary.z-self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonBXC=OctTree(Prism(self.boundary.x-self.boundary.w/2,self.boundary.y+self.boundary.h/2,self.boundary.z+self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonBXD=OctTree(Prism(self.boundary.x-self.boundary.w/2,self.boundary.y+self.boundary.h/2,self.boundary.z-self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonBYC=OctTree(Prism(self.boundary.x-self.boundary.w/2,self.boundary.y-self.boundary.h/2,self.boundary.z+self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.sonBYD=OctTree(Prism(self.boundary.x-self.boundary.w/2,self.boundary.y-self.boundary.h/2,self.boundary.z-self.boundary.l/2,self.boundary.w/2,self.boundary.h/2,self.boundary.l/2),self.capacity,ren)
        self.divided=True
    def insert(self,point,ren):
        if not self.boundary.contains(point):
            return False
        if len(self.points)<self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide(ren)
            self.sonAXC.insert(point,ren)
            self.sonAXD.insert(point,ren)
            self.sonAYC.insert(point,ren)
            self.sonAYD.insert(point,ren)
            self.sonBXC.insert(point,ren)
            self.sonBXD.insert(point,ren)
            self.sonBYC.insert(point,ren)
            self.sonBYD.insert(point,ren)
    def query(self,rang,found):
        if self.boundary.intersects(rang):
            for i in self.points:
                if rang.contains(i):
                    found.append(i)
            if self.divided:
                self.sonAXC.query(rang,found)
                self.sonAXD.query(rang,found)
                self.sonAYC.query(rang,found)
                self.sonAYD.query(rang,found)
                self.sonBXC.query(rang,found)
                self.sonBXD.query(rang,found)
                self.sonBYC.query(rang,found)
                self.sonBYD.query(rang,found)
        else:
            return
    def mostrar(self,n,ren):
        for i in self.points:
            print(n)
            i.imprimir(ren)
        if self.divided:
            self.sonAXC.mostrar(n+1,ren)
            self.sonAXD.mostrar(n+1,ren)
            self.sonAYC.mostrar(n+1,ren)
            self.sonAYD.mostrar(n+1,ren)
            self.sonBXC.mostrar(n+1,ren)
            self.sonBXD.mostrar(n+1,ren)
            self.sonBYC.mostrar(n+1,ren)
            self.sonBYD.mostrar(n+1,ren)
