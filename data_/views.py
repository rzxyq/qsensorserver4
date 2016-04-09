import random # For random generation of an access_code key 
import string # For random generation of an access_code key 
import json # For generating various Python JSON objects 
from os import environ # For adding to mailing list via environment variable CUAPPDEV_INFO_LIST_ID 
from django.shortcuts import render # Classic Django views.py import 
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect # For view responses
from django.template import loader # To load templates 
from django.core.urlresolvers import reverse_lazy, reverse # For generating URLs 
from django.views.generic import View # Standard Generic View 
from django.views.generic.edit import FormView # Generic view used for generating forms
from django.contrib import messages # `flash` messages 
from .models import * # Import all models 
from django.core import serializers # Serializers framework 
from django.core.exceptions import ObjectDoesNotExist # To catch when this happens
from django.contrib import auth  # For logging admin in 
import datetime 
from django.views.decorators.csrf import csrf_exempt
import peakutils
from django.utils import timezone


#eda imports
import numpy as np
import sys
from scipy.ndimage import filters
import re
import csv
import time



TIME_WINDOW = 1 #in minutes
POINTS = TIME_WINDOW*60*0.3 #number of data points considered when calculating feature vectors


@csrf_exempt
def post_data(request): 
    '''takes post request and get json of the format
        data = json.dumps({
            'data': l, # Text-based data
            'seconds': data_array[0],
            'x_coord': data_array[1],
            'y_coord': data_array[2],
            'z_coord': data_array[3],
            'unknown': data_array[4],
            'temp': data_array[5],
            'eda': data_array[6],
            'trial': 299
        })
        and save them as Trial, Data model 
    '''
    if request.method=='POST':
        json_data = json.loads(request.body.decode('utf-8'))
        if json_data.get('data'): #If at least raw test data exists
            target = Data()
            target.data_text = json_data.get('data')
            target.seconds = json_data.get('seconds')
            target.x_coord = json_data.get('x_coord')
            target.y_coord = json_data.get('y_coord')
            target.z_coord = json_data.get('z_coord')
            target.unknown = json_data.get('unknown')
            target.temp = json_data.get('temp')
            target.eda = json_data.get('eda')

            target.date_time = timezone.now()

            #get trial
            trial_num = json_data.get('trial')
            t = Trial.objects.filter(num=trial_num)
            if len(t)==0:
                t = Trial(num=trial_num, name='trial#%s'%(trial_num), date=datetime.date.today())
                t.save()
            else:
                t=t[0]
            target.trial = t

            #data processing
            #WARNING: This doesn't taken into account trial. So ignore first few minutes of this trial
            print(time.time() * 1000) #print current time in miliseconds
            last_window = Data.objects.all().order_by('-id')[:POINTS] #need this many points in window size
            window_eda = []
            for point in last_window:
                if point.eda != None:
                    window_eda.append(point.eda)
            print(window_eda)
            target.mean, target.sums, target.frequency = get_simple_vals(window_eda)

            target.save() 
            return JsonResponse({ "success": True })
        else: 
            return JsonResponse({ "failure": True })


def get_simple_vals(eda_array):
    """Takes in an array of eda values, returns a list containing one value for the mean, one for the sum, and one for the peak frequency."""
    if len(eda_array)==0:
        return [0,0,0]
    eda_array = np.array(eda_array)
    print("eda array...")
    for val in eda_array:
        print(val)

    x = np.linspace(1, len(eda_array), num=len(eda_array))
    y = eda_array
    print(y)
    # normalize with log
    # and blur with gaussian
    y = filters.gaussian_filter(y, 30)
    indexes = peakutils.indexes(y, thres=np.mean(y), min_dist=10)
   
    
    print("indexes......")
    print("length:" + str(len(indexes)))
    print(indexes)
    #print(x[indexes])
    #print(y[indexes])

    if len(indexes) == 0:
        return [0,0,0]
    timestamp = datetime.datetime.now()
    print(timestamp)
    mean_ppa = sum(y)/len(y)
    sum_ppa = sum(y)
    freq = len(indexes)

    the_features = [mean_ppa, sum_ppa, freq]

    return the_features


class Results(View):
    '''Dummy class used for testing. Can be used as superclass for the different result views'''
    def get(self, request): 
        # # Get the data object 
        # result = Data.objects.get(pk=1) 
        # json_result = { 
        #                                 "data_text": result.data_text,
        #                                 "x": result.x_coord,
        #                                 "y": result.y_coord,
        #                                 "z": result.z_coord,
        #                                 "eda": result.eda,
        #                                 "mean": result.mean,
        #                                 "frequency": result.frequency,
        #                                 "sums": result.sums
        #                             }
        return JsonResponse({
            'message': 'If youre seeing this test is successful',
            }); 
    





class ResultView(View):

    def get(self, request): 
        template = loader.get_template('results.html')
        context = {}
        return HttpResponse(template.render(context, request))


    def post(self, request): 
        json_data = json.loads(request.body.decode('utf-8'))
        if json_data.get('trial_num'): 
            trial_num = json_data.get('trial_num')
            result = Data.objects.get(pk=1)
            try: 

                trial = Trial.objects.get(pk=trial_num)
                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                eda=result.eda,
                                                trial=trial_num)

                new_data.save()

            except Exception: 
                trial = Trial(pk=trial_num, name="Trial Number " + str(trial_num), date=datetime.datetime.now())
                trial.save() 

                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                eda=result.eda,
                                                trial=Trial(name='fixing_bug', date=datetime.datetime.now()))

                new_data.save()

            json_result = { 
                                "data_text": result.data_text,
                                "x": result.x_coord,
                                "y": result.y_coord,
                                "z": result.z_coord,
                                "eda": result.eda
                            }

            return JsonResponse(json_result)
        return JsonResponse({ "none": "none" })

class ResultView_mean(View):


    def get(self, request): 
        template = loader.get_template('results_mean.html')
        context = {}
        return HttpResponse(template.render(context, request))


    def post(self, request): 
        json_data = json.loads(request.body.decode('utf-8'))
        if json_data.get('trial_num'): 
            trial_num = json_data.get('trial_num')
            result = Data.objects.get(pk=1)
            try: 

                trial = Trial.objects.get(pk=trial_num)
                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                mean=result.mean,
                                                trial=trial_num)

                new_data.save()

            except Exception: 
                trial = Trial(pk=trial_num, name="Trial Number " + str(trial_num), date=datetime.datetime.now())
                trial.save() 

                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                mean=result.mean,
                                                trial=Trial(name='fixing_bug', date=datetime.datetime.now()))

                new_data.save()

            json_result = { 
                                "data_text": result.data_text,
                                "x": result.x_coord,
                                "y": result.y_coord,
                                "z": result.z_coord,
                                "mean": result.mean
                            }

            return JsonResponse(json_result)
        return JsonResponse({ "none": "none" })

class ResultView_sums(View):


    def get(self, request): 
        template = loader.get_template('results_sums.html')
        context = {}
        return HttpResponse(template.render(context, request))


    def post(self, request): 
        json_data = json.loads(request.body.decode('utf-8'))
        if json_data.get('trial_num'): 
            trial_num = json_data.get('trial_num')
            result = Data.objects.get(pk=1)
            try: 

                trial = Trial.objects.get(pk=trial_num)
                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                sums=result.sums,
                                                trial=trial_num)

                new_data.save()

            except Exception: 
                trial = Trial(pk=trial_num, name="Trial Number " + str(trial_num), date=datetime.datetime.now())
                trial.save() 

                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                sums=result.sums,
                                                trial=Trial(name='fixing_bug', date=datetime.datetime.now()))

                new_data.save()

            json_result = { 
                                "data_text": result.data_text,
                                "x": result.x_coord,
                                "y": result.y_coord,
                                "z": result.z_coord,
                                "sums": result.sums,
                            }

            return JsonResponse(json_result)
        return JsonResponse({ "none": "none" })

class ResultView_frequency(View):


    def get(self, request): 
        template = loader.get_template('results_frequency.html')
        context = {}
        return HttpResponse(template.render(context, request))


    def post(self, request): 
        json_data = json.loads(request.body.decode('utf-8'))
        if json_data.get('trial_num'): 
            trial_num = json_data.get('trial_num')
            result = Data.objects.get(pk=1)
            try: 

                trial = Trial.objects.get(pk=trial_num)
                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                frequency=result.frequency,
                                                trial=trial_num)

                new_data.save()

            except Exception: 
                trial = Trial(pk=trial_num, name="Trial Number " + str(trial_num), date=datetime.datetime.now())
                trial.save() 

                new_data = Data(data_text=result.data_text,
                                                x_coord=result.x_coord,
                                                y_coord=result.y_coord,
                                                z_coord=result.z_coord,
                                                frequency=result.frequency,
                                                trial=Trial(name='fixing_bug', date=datetime.datetime.now()))

                new_data.save()

            json_result = { 
                                "data_text": result.data_text,
                                "x": result.x_coord,
                                "y": result.y_coord,
                                "z": result.z_coord,
                                "frequency": result.frequency
                            }

            return JsonResponse(json_result)
        return JsonResponse({ "none": "none" })

@csrf_exempt
def post_graph(request): 
    json_data = json.loads(request.body.decode('utf-8'))
    # if json_data.get('trial_num'): 
    result = Data.objects.all().last() #return last object only

    json_result = { 
                        "data_text": result.data_text,
                        "x": result.x_coord,
                        "y": result.y_coord,
                        "z": result.z_coord,
                        "eda": result.eda
                    }

    return JsonResponse(json_result)
    return JsonResponse({ "none": "none" })

@csrf_exempt
def frequency_post_graph(request): 
    json_data = json.loads(request.body.decode('utf-8'))
    # if json_data.get('trial_num'): 
    result = Data.objects.all().last() #return last object only

    json_result = { 
                        "data_text": result.data_text,
                        "x": result.x_coord,
                        "y": result.y_coord,
                        "z": result.z_coord,
                        "frequency": result.frequency
                    }

    return JsonResponse(json_result)
    return JsonResponse({ "none": "none" })

@csrf_exempt
def sums_post_graph(request): 
    json_data = json.loads(request.body.decode('utf-8'))
    # if json_data.get('trial_num'): 
    result = Data.objects.all().last() #return last object only

    json_result = { 
                        "data_text": result.data_text,
                        "x": result.x_coord,
                        "y": result.y_coord,
                        "z": result.z_coord,
                        "sums": result.sums
                    }

    return JsonResponse(json_result)
    return JsonResponse({ "none": "none" })


@csrf_exempt
def mean_post_graph(request): 
    json_data = json.loads(request.body.decode('utf-8'))
    # if json_data.get('trial_num'): 
    result = Data.objects.all().last() #return last object only

    json_result = { 
                        "data_text": result.data_text,
                        "x": result.x_coord,
                        "y": result.y_coord,
                        "z": result.z_coord,
                        "mean": result.mean
                    }

    return JsonResponse(json_result)
    return JsonResponse({ "none": "none" })



