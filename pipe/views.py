from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.


def page(request):
    return render(request,"pipe.html")

class pipefriction:
    def __init__(self,diameter=0,length=0,roughness=0,flow_rate=0):
        self.d = diameter
        self.l = length
        self.pm = roughness
        self.pf = flow_rate

    def calculation(self):
        friction_loss = 10.44 * self.l * (self.pf/self.pm)**1.85 * (1/self.d**4.8655)
        result = {'diameter':self.d,'length':self.l,'roughness':self.pm,'flow_rate':self.pf,'friction_loss':friction_loss}
        return result





def pipe_calculation(request):
    if request.method == 'POST':
        pipe_diameter = float(request.POST.get('pipe_diameter'))
        pipe_length = float(request.POST.get('pipe_length'))
        roughness_coefficient = float(request.POST.get('roughness_coefficient'))
        flow_rate = float(request.POST.get('flr'))

        object = pipefriction(pipe_diameter,pipe_length,roughness_coefficient,flow_rate)
        result = object.calculation()

        context = {
            'pipe_diameter': pipe_diameter,
            'pipe_length': pipe_length,
            'roughness_coefficient': roughness_coefficient,
            'flow_rate': flow_rate,
            'friction_loss': result['friction_loss']
        }

        return render(request, 'pipe.html', context)

    return render(request, 'pipe.html')