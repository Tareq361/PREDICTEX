import os
from pathlib import Path

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json

from .models import covidImages
from django.shortcuts import render
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


model = load_model('resnet_model.h5')
# Create your views here.
def home(request):
    return render(request,"index.html")


def diabetes(request):
    if request.method == 'POST':
        context = diabetesPrediction(Pregnancies=request.POST.get('Pregnancies'),Glucose=request.POST.get('Glucose'),
                                     BloodPressure=request.POST.get('BloodPressure'),
                           SkinThickness=request.POST.get('SkinThickness'),Insulin=request.POST.get('Insulin'),
                                     BMI=request.POST.get('BMI'),
                           DiabetesPedigreeFunction=request.POST.get('DiabetesPedigreeFunction'),Age=request.POST.get('dAge'))

        return render(request,'result.html',context)
    return render(request,"diabetes.html")

def heart(request):
    if request.method == 'POST':
        to_predict_list = request.POST
        if request.POST.get('smoke') == 1:
            smoke=request.POST.get('smoke')
        else:
            smoke=0
        if request.POST.get('Alcoholintake') == 1:
            alcohol=request.POST.get('Alcoholintake')
        else:
            alcohol=0
        if request.POST.get('Physicalactivity') == 1:
            active=request.POST.get('Physicalactivity')
        else:
            active=0

        context = heartPrediction(Age=request.POST.get('hAge'),Gender=request.POST.get('Gender'),Height=request.POST.get('Height'),
                            Weight=request.POST.get('Weight'),sbd=request.POST.get('sbd'),dbd=request.POST.get('dbd'),
                            Cholesterol=request.POST.get('Cholesterol'),Glucose=request.POST.get('Glucose'),
                           smoke=smoke,alcohol=alcohol,
                           active=active)


        return render(request,'result.html',context )
    return render(request,"heart.html")

def kidney(request):
    if request.method == 'POST':
        print(request.POST)
        context = kidneyPrdeiction(Age=request.POST.get('kAge'),bp=request.POST.get('bp'),rbc=request.POST.get('rbc'),
                            wbc=request.POST.get('wbc'),appet=request.POST.get('appet'),pc_normal=request.POST.get('pc_normal'),
                           htn=request.POST.get('htn'),hemo=request.POST.get('hemo'),
                           bgr=request.POST.get('bgr'),dm=request.POST.get('dm'),
                           ane=request.POST.get('ane'))

        return render(request,'result.html',context)
    return render(request,"kidney.html")


def liver(request):
    if request.method == 'POST':
        context = liverPrediction(Age=request.POST.get('lAge'),Gender=request.POST.get('Gender'),tb=request.POST.get('tb'),
                            db=request.POST.get('db'),ap=request.POST.get('ap'),aa=request.POST.get('aa'),
                            aa2=request.POST.get('aa2'),tp=request.POST.get('tp'),
                           a=request.POST.get('a'),ag=request.POST.get('ag'))


        return render(request,'result.html',context)
    return render(request,"liver.html")


def covid(request):
    if request.method == 'POST':

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

        file = request.FILES['image']
        img=covidImages(image=file)
        img.save()
        b = """\\"""
        u = str(img.image)
        print(u)
        u.replace(u[0], """\\""")
        u.replace(u[12], """\\""")
        loc = (str(MEDIA_ROOT) + b + u)

        print(loc)
        data=image.load_img(loc,target_size=(128,128,3))
        data = np.expand_dims(data, axis=0)
        data = data * 1.0 / 255

        print(data.shape)
        result=model.predict(data)
        print(result)
        indices = {0: 'COVID', 1: 'Lung_Opacity', 2: 'Normal', 3: 'Viral Pneumonia'}
        predicted_class = np.asscalar(np.argmax(result, axis=1))
        accuracy = round(result[0][predicted_class] * 100, 2)

        label = indices[predicted_class]
        print(predicted_class)
        print(accuracy)
        print(label)
        return render(request,"result.html",{'accuracy':accuracy,'label':label,'covid':'true','disease':'Covid-19','image':img.image})

    return render(request,"covid.html")


#for api using rest framework
@api_view(['GET'])
def apiView(request):
    api_urls = {
        'diabetes': 'api/diabetes/',
        'liver disease ': 'api/liver_disease/',

    }
    return Response(api_urls)


@api_view(['POST'])
def diabetesApi(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = diabetesPrediction(Pregnancies=body['Pregnancies'], Glucose=body['Glucose'],
                           BloodPressure=body['BloodPressure'],
                           SkinThickness=body['SkinThickness'], Insulin=body['Insulin'], BMI=body['BMI'],
                           DiabetesPedigreeFunction=body['DiabetesPedigreeFunction'], Age=body['Age'])
        json_data = JSONRenderer().render(js)
        return HttpResponse(json_data, content_type='application/json')

@api_view(['POST'])
def liverApi(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = liverPrediction(Age=body['Age'], Gender=body['Gender'],
                           tb=body['TotalBilirubin'],
                           db=body['DirectBilirubin'], ap=body['AlkalinePhosphatase'], aa=body['AlanineAminotransferase'],
                           aa2=body['AsparateAminotransferase'],tp=body['TotalProtein'],a=body['Albumin'],ag=body['AlbuminGlobulinRatio'])
        json_data = JSONRenderer().render(js)
        return HttpResponse(json_data, content_type='application/json')
@api_view(['POST'])
def kidneyApi(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = kidneyPrdeiction(Age=body['Age'], bp=body['bp'],
                           rbc=body['rbc'],
                           wbc=body['wbc'], appet=body['appet'], pc_normal=body['pc_normal'],
                           htn=body['htn'],hemo=body['hemo'],bgr=body['bgr'],dm=body['dm'],ane=body['ane'])
        json_data = JSONRenderer().render(js)
        return HttpResponse(json_data, content_type='application/json')
@api_view(['POST'])
def heartApi(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = heartPrediction(Age=body['Age'], Gender=body['Gender'], Height=body['Height'],
                       Weight=body['Weight'], sbd=body['sbd'],dbd=body['dbd'],
                       Cholesterol=body['Cholesterol'],Glucose=body['Glucose'],
                       smoke=body['smoke'], alcohol=body['alcohol'],
                       active=body['active'])
        json_data = JSONRenderer().render(js)
        return HttpResponse(json_data, content_type='application/json')

@api_view(['POST'])
def covidApi(request):
    print(request)
    print(request.FILES['image'])
    js=covidprediction(request.FILES['image'])
    json_data = JSONRenderer().render(js)
    return HttpResponse(json_data, content_type='application/json')

def diabetesPrediction(**par):
    to_predict_list = [par['Pregnancies'], par['Glucose'],
                       par['BloodPressure'],
                       par['SkinThickness'], par['Insulin'], par['BMI'],
                       par['DiabetesPedigreeFunction'], par['Age']]
    # to_predict_list = list(map(float, to_predict_list))
    to_predict_list = np.array(to_predict_list).reshape(1, 8)
    print(to_predict_list)
    # to_predict_list=to_predict_list.reshape(-1, 1)
    loaded_model = joblib.load("diabetes_detector")
    result = loaded_model.predict(to_predict_list)
    print(result[0])
    if (int(result[0]) == 1):
        print('Sorry ! You are Suffering Diabetes')
    else:
        print('Congrats ! you are Healthy')
    # return render(request, 'result.html', {'result': int(result[0]), "disease": "diabetes"})
    js = {'result': int(result[0]), "disease": "diabetes"}

    return js

def liverPrediction(**par):

    to_predict_list = [par['Age'], par['Gender'],
                       par['tb'],
                       par['db'], par['ap'], par['aa'],
                       par['aa2'], par['tp'],par['a'], par['ag']]
    # to_predict_list = list(map(float, to_predict_list))
    to_predict_list = np.array(to_predict_list).reshape(1, 10)
    print(to_predict_list)
    # to_predict_list=to_predict_list.reshape(-1, 1)
    loaded_model = joblib.load("Liver_diseases_detector")
    result = loaded_model.predict(to_predict_list)
    print(result[0])
    if (int(result[0]) == 1):
        print('Sorry ! You are Suffering Liver disease')
    else:
        print('Congrats ! you are Healthy')
    # return render(request, 'result.html', {'result': int(result[0]), "disease": "diabetes"})
    js = {'result': int(result[0]), "disease": "Liver disease"}

    return js

def kidneyPrdeiction(**par):
    to_predict_list = [par['Age'], par['bp'], par['rbc'],
                       par['wbc'], par['appet'], par['pc_normal'],
                       par['htn'], par['hemo'],
                       par['bgr'], par['dm'],
                       par['ane']]
    # to_predict_list = list(map(float, to_predict_list))
    to_predict_list = np.array(to_predict_list).reshape(1, 11)
    print(to_predict_list)
    # # to_predict_list=to_predict_list.reshape(-1, 1)
    loaded_model = joblib.load("chronic_kidney_disease")
    result = loaded_model.predict(to_predict_list)
    print(result)
    if (int(result[0]) == 0):
        r = 1
        print('Sorry ! You are Suffering kidey disease')
    else:
        r = 0
        print('Congrats ! you are Healthy')
    js={'result': r, "disease": "kidney disease"}

    return js
def heartPrediction(**par):
    to_predict_list = [0, par['Age'],par['Gender'], par['Height'],
                       par['Weight'], par['sbd'],par['dbd'],
                       par['Cholesterol'],par['Glucose'],
                       par['smoke'], par['alcohol'],
                       par['active']]
    # to_predict_list = list(map(float, to_predict_list))
    to_predict_list = np.array(to_predict_list).reshape(1, 12)
    print(to_predict_list)
    # to_predict_list=to_predict_list.reshape(-1, 1)
    loaded_model = joblib.load("heart_disease_detector")
    result = loaded_model.predict(to_predict_list)
    print(result)
    if (int(result[0]) == 1):
        print('Sorry ! You are Suffering Diabetes')
    else:
        print('Congrats ! you are Healthy')
    js={'result': int(result[0]), "disease": "heart disease"}
    return js

def covidprediction(file):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


    img = covidImages(image=file)
    img.save()
    b = """\\"""
    u = str(img.image)
    print(u)
    u.replace(u[0], """\\""")
    u.replace(u[12], """\\""")
    loc = (str(MEDIA_ROOT) + b + u)

    print(loc)
    data = image.load_img(loc, target_size=(128, 128, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    print(data.shape)
    result = model.predict(data)
    print(result)
    indices = {0: 'COVID', 1: 'Lung_Opacity', 2: 'Normal', 3: 'Viral Pneumonia'}
    predicted_class = np.asscalar(np.argmax(result, axis=1))
    accuracy = round(result[0][predicted_class] * 100, 2)

    label = indices[predicted_class]
    print(predicted_class)
    print(accuracy)
    print(label)

    js = {'accuracy': accuracy, 'label': label, 'covid': 'true', 'disease': 'Covid-19', 'image': str(img.image)}

    return js