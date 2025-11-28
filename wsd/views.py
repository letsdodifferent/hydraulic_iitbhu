from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import urllib.request
import urllib.parse
import json

# ======================================================================
# HEAVY LIBRARIES COMMENTED OUT FOR VERCEL DEPLOYMENT
# These libraries exceed Vercel's 250MB serverless function limit
# ======================================================================
# from pysheds.grid import Grid
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvas
# import io

def main(request):
    return render(request,"wsd.html")

def get_location_info(lat, lon):
    """
    Fetch interesting information about a location using reverse geocoding
    and return famous landmarks, places of interest
    """
    try:
        # Use Nominatim (OpenStreetMap) for reverse geocoding - it's free!
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10"
        headers = {'User-Agent': 'HydraulicsApp/1.0'}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        # Extract interesting information
        location_name = data.get('display_name', 'Unknown Location')
        address = data.get('address', {})
        
        city = address.get('city') or address.get('town') or address.get('village') or 'Unknown'
        state = address.get('state', 'Unknown')
        country = address.get('country', 'Unknown')
        
        # Create a nice description
        description = f"📍 **{location_name}**"
        
        info = {
            'location': location_name,
            'city': city,
            'state': state,
            'country': country,
            'coordinates': f"{lat}, {lon}",
            'description': description,
            'message': f"You've selected a location in {city}, {state}, {country}!"
        }
        
        return info
        
    except Exception as e:
        return {
            'location': f'Location at {lat}, {lon}',
            'city': 'Unknown',
            'state': 'Unknown',
            'country': 'Unknown',
            'coordinates': f"{lat}, {lon}",
            'description': f"Coordinates: {lat}, {lon}",
            'message': 'Location information unavailable',
            'error': str(e)
        }

# ======================================================================
# WATERSHED VIEW - MODIFIED FOR VERCEL DEPLOYMENT
# Shows location information and interesting facts instead of watershed analysis
# ======================================================================
@csrf_exempt
def wsd(request):
    if request.method == 'POST':
        try:
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('long'))
            
            # Validate inputs
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return JsonResponse({
                    'error': 'Latitude must be between -90 and 90, and longitude must be between -180 and 180.'
                })
            
            # Get location information
            location_info = get_location_info(lat, lon)
            
            return JsonResponse({
                'success': True,
                'location_info': location_info,
                'note': 'Showing location information. Heavy watershed analysis disabled for cloud deployment.'
            })
            
        except ValueError:
            return JsonResponse({'error': 'Invalid latitude or longitude values.'})
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'})
            
    elif request.method == 'GET':
        return JsonResponse({'error': 'Invalid request method. Use POST to submit data.'})


# ======================================================================
# FULL WATERSHED PROCESSOR - COMMENTED OUT FOR VERCEL DEPLOYMENT
# Uncomment this section when deploying on Render, Railway, or similar
# ======================================================================

# class WatershedProcessor:
#     def __init__(self):
#         self.grid = None
#         self.dem = None
#         self.pit_filled_dem = None
#         self.flooded_dem = None
#         self.inflated_dem = None
#         self.fdir = None
#         self.acc = None
#         self.dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
# 
#     def initialize(self):
#         print("Initializing DEM and preprocessing...")
#         self.grid = Grid.from_raster(r"/path/to/output_SRTMGL1.tif")
#         self.dem = self.grid.read_raster(r"/path/to/output_SRTMGL1.tif")
#         self.pit_filled_dem = self.grid.fill_pits(self.dem)
#         self.flooded_dem = self.grid.fill_depressions(self.pit_filled_dem)
#         self.inflated_dem = self.grid.resolve_flats(self.flooded_dem)
#         self.fdir = self.grid.flowdir(self.inflated_dem, dirmap=self.dirmap)
#         self.acc = self.grid.accumulation(self.fdir, dirmap=self.dirmap)
#         print("DEM initialization complete.")