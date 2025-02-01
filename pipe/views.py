from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

class pipe:
    def __init__(self,diameter=0,length=0,roughness=0,flr=0):
        self.d = diameter
        self.l = length
        self.pm = roughness
        self.pf = flr

    def pipe_calculation(self):
        A = 3.14159*(self.d**2)/4
        P = 3.14159*self.d
        R = A/P
        V = 1.318*(self.pf**0.5)*(R**0.63)*(self.pm**0.54)
        Q = A*V
        result = {'diameter':self.d,'length':self.l,'roughness':self.pm,'flow_rate':self.pf,'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"velocity":V,"flow":Q}
        return result





def pipe_calculation(request):
    if request.method == 'POST':
        diameter = float(request.POST.get('pipe_diameter'))
        len = float(request.POST.get('pipe_length'))
        pm = float(request.POST.get('roughness_coefficient'))
        pf = float(request.POST.get('flr'))

        return render(request,'fl.html',"")