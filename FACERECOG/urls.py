from django.urls import path,include
from FACERECOG.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('faceApiViewsets',EmployeeInfoViewsets)

urlpatterns = [
    path('',mainpage,name="main-page"),
    path('CollectData/',ShowFace,name="face-recog"),
    path('Detect/',DetectAndAttendance,name="face-detect-attendance"),
    path('about/',about,name="about"),
    path('faceApi/',EmployeeInfoAPIView.as_view(),name="FaceApi"),
    path('faceApiViewsets/',include(router.urls)),
    path('contact/',Contact,name="contact")
]