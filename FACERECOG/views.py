from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import EmployeeInfo, AboutEmployees
from .forms import EmployeeForm, ContactUsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import cv2
import pandas as pd
import numpy as np
import time
import datetime
import csv
from PIL import Image
import os
import urllib

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmployeeInfoSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

# Create your views here.

@login_required
def ShowFace(request):
    if request.method=="POST":
        form=EmployeeForm(request.POST,request.FILES)
        #form.instance.profile=request.user.profile
        #print(form.instance.profile)
        if form.is_valid():
            form.save()
            eid=form.cleaned_data.get("id")
            ename=form.cleaned_data.get("name")
            print(eid)
            print(ename)

            cam = cv2.VideoCapture(0) #rtspadmin:2019@192.168.3.202:554/Streaming/Channels/201/
            #cam.set(cv2.CAP_PROP_POS_FRAMES,30)

            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0

#            url=""

            while (True):

                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite(r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\EmployeeImages\\" + str(ename) + '.' + str(eid) + '.' + str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    # display the frame
                    cv2.imshow('frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 60:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + str(eid) + " Name : " + str(ename)
            row = [eid, ename]
            with open(r'E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\FACERECOG\\EmployeeDetails\\EmployeeDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()

            def getImagesAndLabels(path):
                #get the path of all the files in the folder
                imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
                #print(imagePaths)

                #Create empty face list
                faces=[]
                #Create empty ID list
                Ids=[]
                #now looping through all the image paths and loading the Ids and the images
                for imagePath in imagePaths:
                    # loading the image and converting it to gray scale
                    pilImage = Image.open(imagePath).convert('L')
                    # Now we are converting the PIL image into numpy array
                    imageNp = np.array(pilImage, 'uint8')
                    # getting the Id from the image
                    Id = int(os.path.split(imagePath)[-1].split(".")[1])
                    # extract the face from the training image sample
                    faces.append(imageNp)
                    Ids.append(Id)
                #print(faces,Ids)
                return faces, Ids


            recognizer = cv2.face_LBPHFaceRecognizer.create()   #recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            faces,Id = getImagesAndLabels("EmployeeImages")
            recognizer.train(faces,np.array(Id))
            recognizer.save(r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\TrainingImageLabel\\Trainer.yml")
            res="Image Trained"
            messages.info(request,res)

            messages.success(request,f"Employee Data stored")
            return redirect("main-page")

    else:
        form=EmployeeForm()

    return render(request,"FACERECOG/home.html",{"form":form})

@login_required
def DetectAndAttendance(request):
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer() #gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE
    recognizer.read(r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\TrainingImageLabel\\Trainer.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv(r'E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\FACERECOG\\EmployeeDetails\\EmployeeDetails.csv')
    cam = cv2.VideoCapture(0)
    #cam.open("rtsp://admin:2019@192.168.3.202:554/Streaming/Channels/201/")
    cam.set(cv2.CAP_PROP_POS_FRAMES, 1500)

    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            print(Id)
            print(conf)
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
            else:
                Id = 'Unknown'
                tt = str(Id)
            if (conf > 75):
                noOfFile = len(os.listdir(r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\ImagesUnknown")) + 1
                cv2.imwrite(r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\ImagesUnknown\\Image\\" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        print(attendance.values)
        print(attendance["Id"].values)
        print(attendance["Name"].values)
        print(attendance["Date"].values)
        print(attendance["Time"].values)

        cv2.imshow('Press q to close after detecting your face', im)
        if (cv2.waitKey(1) == ord('q')):
            break


    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\Attendance\\Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    attendance.to_csv(fileName, index=False)

    atten = attendance.values
    # Write Attendance in MAINAllAttendance.csv
    fn = (r"E:\\FACE RECOGNITION DJANGO PROJECT\\FACE\\Attendance\\MAINAllAttendance.csv")
    w = csv.writer(open(fn, 'a'), dialect='excel')
    w.writerows(atten)

    cam.release()
    cv2.destroyAllWindows()
    # print(attendance)
    #res = attendance
    #messages.info(request,res)
    return redirect("main-page")

def about(request):
    context = {
        "members" : AboutEmployees.objects.all()
    }
    return render(request,"FACERECOG/about.html",context)

def mainpage(request):
    return render(request,"FACERECOG/base.html")

class EmployeeInfoAPIView(APIView):
    def get(self,request):
        employees=EmployeeInfo.objects.all()
        serializer=EmployeeInfoSerializer(employees,many=True)
        return Response(serializer.data,status=200)

    def post(self,request):
        data=request.data
        serializer=EmployeeInfoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)

        return Response(serializer.data,status=400)

class EmployeeInfoViewsets(viewsets.ModelViewSet):
    serializer_class = EmployeeInfoSerializer
    queryset = EmployeeInfo.objects.all()
    lookup_field='id'

def Contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        print(name)
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        form = ContactUsForm({'name':name,'phone':phone,'email':email,'message':message})
        if form.is_valid():
            form.save()
            name=form.cleaned_data.get("name")
            print(name)
            phone=form.cleaned_data.get("phone")
            email=form.cleaned_data.get("email")
            message=form.cleaned_data.get("message")
            messages.success(request,f'Someone Contact us')
            return redirect("contact")
    return render(request,"FACERECOG/contact.html")