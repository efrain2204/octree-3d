from log import *
from random import choice
colors = vtk.vtkNamedColors()

#mouse
class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self,parent=None):
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)
        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()
    def leftButtonPressEvent(self,obj,event):
        clickPos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        # get the new
        self.NewPickedActor = picker.GetActor()
        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)
            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(1.0, 0.0, 0.0)
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor
        self.OnLeftButtonDown()
        return
# A renderer and render window

ren= vtk.vtkRenderer()
num=400
boundary=Prism(num/2,num/2,num/2,num/2,num/2,num/2)
ot=OctTree(boundary,4,ren)
for i in range(100):
    p=Point(choice(range(num)),choice(range(num)),choice(range(num)))
    ot.insert(p,ren)
#start Codex draw
ot.mostrar(0,ren)
#end Codex draw


num2=vtk.vtkMath.Random(0, 600)
boundary2=Prism(num2,num2,num2,100,100,100)
f=[]
ot.query(boundary2,f)
for i in f:
    i.printp()
#Query
r = 0.4
g = 0.5
b = 0.8
#cube query
cube = vtk.vtkCubeSource()
cube.SetXLength(boundary2.w*2)
cube.SetYLength(boundary2.h*2)
cube.SetZLength(boundary2.l*2)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cube.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(r, g, b)
actor.GetProperty().SetOpacity(0.2)
actor.SetPosition(boundary2.x, boundary2.y, boundary2.z)
actor.RotateX(0)
actor.RotateY(0)
actor.RotateZ(0)
ren.AddActor(actor)

#points query
for i in f:
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(i.x, i.y, i.z)
    sphereSource.SetRadius(10)
    # Make the surface smooth.
    sphereSource.SetPhiResolution(100)
    sphereSource.SetThetaResolution(100)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())
    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper)
    actor2.GetProperty().SetColor(0,0,0)
    ren.AddActor(actor2)

ren.SetBackground(0.1,0.1,0.1)
renWin= vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(300,300)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# add the custom style
style = MouseInteractorHighLightActor()
style.SetDefaultRenderer(ren)
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()


