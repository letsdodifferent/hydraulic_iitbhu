from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def oc(request):
    return render(request,"opencf.html")


import math

class Openchannalflow:
    
    def __init__(self,calculation_type,basewidth=0,height=0,slope1=0,slope2=0,cslope=0,Manning_coefficient=1,velocity=0,discharge=0):
        self.calculation_type = calculation_type
        self.b = basewidth
        self.y = height
        self.z1 = slope1
        self.z2 = slope2
        self.s = cslope
        self.n = Manning_coefficient
        self.V = velocity
        self.Q = discharge
    
    

    def Trapezoid(self):
        t = self.b + self.y*(self.z1 + self.z2)
        A = (self.y*(self.b + t))/2
        P = self.b + self.y * (math.sqrt(1+self.z1**2) + math.sqrt(1+self.z2**2))
        R = A/P
        D=A/t       
        self.different_calculations(R,A) 
        result = {'z1':self.z1,'z2':self.z2,'bottom_width':self.b,'water_depth':self.y,'channel_slope':self.s,'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"topwidth":t,"hydraulic_depth":D,"velocity":self.V,"flow":self.Q}
        return result


    def Rectangle(self):
        A = self.b*self.y
        P = self.b+2*self.y
        R = A/P
        t = self.b
        D=A/t
        self.different_calculations(R,A)
        result = {'bottom_width':self.b,'water_depth':self.y,'channel_slope':self.s,'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"topwidth":t,"hydraulic_depth":D,"velocity":self.V,"flow":self.Q}
        return result


    def Triangle(self):
        A = 0.5*(self.z1 + self.z2)*(self.y**2)
        P = self.y*(math.sqrt(1+self.z1**2) + math.sqrt(1+self.z2**2))
        R = A/P
        t = self.z1*self.y + self.z2*self.y
        D=A/t
        self.different_calculations(R,A)        
        result = {'z1':self.z1,'z2':self.z2,'bottom_width':self.b,'water_depth':self.y,'channel_slope':self.s,'flow_area':A,"wetted_perimeter":P,"hydraulic_radius":R,"topwidth":t,"hydraulic_depth":D,"velocity":self.V,"flow":self.Q}
        return result
    
    def Circle(self):
        pass

    def different_calculations(self,R,A):
        if self.calculation_type == "velocity_discharge":
            self.V = (1/self.n)*(R**(2/3))*(self.s**0.5)
            self.Q = A*self.V
            
        elif self.calculation_type == "channel_slope_v":
            self.s = (self.n**2)*(self.V**2)/(R**(2/3))
            self.Q = A*self.V
        
        elif self.calculation_type == "channel_slope_q":
            self.s = (self.n**2)*(self.Q**2)/((R**(2/3))*(A**2))
            self.V = self.Q/A

        elif self.calculation_type == "manning_v":
            self.n = (self.s**0.5)*(R**(2/3))/self.V
            self.Q = A*self.V
        
        elif self.calculation_type == "manning_q":
            self.n = (self.s**0.5)*(R**(2/3))/(self.Q/A)
            self.V = self.Q/A
        
        elif self.calculation_type == "depth_q":
            pass


def calculate(request):
    if request.method == 'POST':
        calculation_type = request.POST.get('calculation_type')
        channel_type = request.POST.get('channel_type')
        basewidth = float(request.POST.get('bottom_width'))
        height = float(request.POST.get('water_depth'))
        try:
            slope1 = float(request.POST.get('z1'))
            slope2 = float(request.POST.get('z2'))
        except:
            slope1 = 0
            slope2 = 0

        if calculation_type == 'velocity_discharge':
            cslope = float(request.POST.get('channel_slope'))
            Manning_coefficient = float(request.POST.get('n'))
            a = Openchannalflow(calculation_type,basewidth,height,slope1,slope2,cslope,Manning_coefficient)
        
        elif calculation_type == 'channel_slope_v':
            velocity = float(request.POST.get('velocity'))
            Manning_coefficient = float(request.POST.get('n'))
            a = Openchannalflow(calculation_type,basewidth,height,slope1,slope2,velocity,Manning_coefficient)
        
        elif calculation_type == 'channel_slope_q':
            discharge = float(request.POST.get('flow'))
            Manning_coefficient = float(request.POST.get('n'))
            a = Openchannalflow(calculation_type,basewidth,height,slope1,slope2,discharge,Manning_coefficient)

        elif calculation_type == 'manning_v':
            velocity = float(request.POST.get('velocity'))
            cslope = float(request.POST.get('channel_slope'))
            a = Openchannalflow(calculation_type,basewidth,height,slope1,slope2,cslope,velocity)

        elif calculation_type == 'manning_q':
            discharge = float(request.POST.get('flow'))
            cslope = float(request.POST.get('channel_slope'))
            a = Openchannalflow(calculation_type,basewidth,height,slope1,slope2,cslope,discharge)

        elif calculation_type == 'depth_q':
            discharge = float(request.POST.get('flow'))


        if channel_type == 'Trapezoid':
            result = a.Trapezoid()
        
        elif channel_type == 'Rectangle':
            result = a.Rectangle()

        elif channel_type == 'Triangle':
            result = a.Triangle()

        elif channel_type == 'Circle':
            result = a.Circle()

        context = {
                    'calculation_type': calculation_type,
                    'channel_type': channel_type,
                    'basewidth': basewidth,
                    'height': height,
                    'slope1': slope1,
                    'slope2': slope2,
                    'channel_slope': cslope,
                    'velocity': request.POST.get('velocity', ''),
                    'flow': request.POST.get('flow', ''),
                    'result': result
                }

        return render(request, 'opencf.html', context)

    return render(request, 'opencf.html')


# Try for error handling
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

    # return render(request,'opencf.html',result)

    # JsonResponse({'error': 'Invalid request method'}, status=405)






