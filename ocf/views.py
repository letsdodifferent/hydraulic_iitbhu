from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request,"index.html")

def oc(request):
    return render(request,"opencf.html")


import math

class Openchannalflow:
    
    def __init__(self,basewidth=0,height=0,slope1=0,slope2=0,cslope=0,mc=1):
        self.b = basewidth
        self.y = height
        self.z1 = slope1
        self.z2 = slope2
        self.s = cslope
        self.n = mc
    

    def Trapezoid(self):
        t = self.b + self.y*(self.z1 + self.z2)
        A = (self.y*(self.b + t))/2
        P = self.b + self.y * (math.sqrt(1+self.z1**2) + math.sqrt(1+self.z2**2))
        R = A/P
        D=A/t
        V = (1/self.n)*(R**(2/3))*(self.s**0.5)
        Q = A*V
        result = {'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"topwidth":t,"hydraulic_depth":D,"velocity":V,"flow":Q}
        return result


    def Rectangle(self):
        A = self.b*self.y
        P = self.b+2*self.y
        R = A/P
        t = self.b
        D=A/t
        V = (1/self.n)*(R**(2/3))*(self.s**0.5)
        Q = A*V
        result = {'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"topwidth":t,"hydraulic_depth":D,"velocity":V,"flow":Q}
        return result


    def Triangle(self):
        t = (self.z1 + self.z2) * self.y
        A = 0.5 * t * self.y
        P = self.y * (math.sqrt(1+self.z1**2) + math.sqrt(1+self.z2**2))
        R = A/P
        D=A/t
        V = (1/self.n)*(R**(2/3))*(self.s**0.5)
        Q = A*V
        result = {'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"topwidth":t,"hydraulic_depth":D,"velocity":V,"flow":Q}
        return result


def calculate(request):
    if request.method == 'POST':
        height = float(request.POST.get('water_depth'))
        cslope = float(request.POST.get('channel_slope'))
        channelType = request.POST.get('channel_type')
        mc = float(request.POST.get('n'))

        try:
            basewidth = float(request.POST.get('bottom_width'))
        except:
            basewidth = 0

        try:
            slope1 = float(request.POST.get('z1'))
            slope2 = float(request.POST.get('z2'))
        except:
            slope1 = 0
            slope2 = 0


    a = Openchannalflow(basewidth,height,slope1,slope2,cslope,mc)
    if channelType == 'Trapezoid':
        result =  a.Trapezoid()
    elif channelType == 'Rectangle':
        result =  a.Rectangle()
    elif channelType == 'Triangle':
        result =  a.Triangle()
    
    return render(request,'opencf.html',result)

    
    
   

# To Check error
    # try:
    #         # basewidth = float(basewidth) 
    #         slope1 = float(slope1) 
    # except:
    #         # basewidth = 0  # Default value for invalid input
    #         slope1 = 0  # Default value for invalid input
    # return JsonResponse(result)
    # return JsonResponse(
    #     result

    #         # 'slope1': slope1,
    #         # 'a':request.POST
    #         # 'calculation_type': calculation_type,
    #         # 'unit_system': unit_system,
    #         # 'bottom_width': basewidth,
    #     , safe=False )


    # JsonResponse({'error': 'Invalid request method'}, status=405)






