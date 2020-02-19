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

num=600
boundary=Prism(num/2,num/2,num/2,num/2,num/2,num/2)

ot=OctTree(boundary,4,ren)
for i in range(30):
    p=Point(choice(range(num)),choice(range(num)),choice(range(num)))
    ot.insert(p,ren)


#start Codex draw
ot.mostrar(0,ren)
#end Codex draw

boundary2=Prism(num/2,num/2,num/2,100,100,100)
f=[]
ot.query(boundary2,f)
for i in f:
    i.printp()
#Query

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


