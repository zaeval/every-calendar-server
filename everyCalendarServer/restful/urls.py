"""mama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from . import views

app_name = 'restful'
urlpatterns = [
    # path('student/', include([
    #     path('', views.student),
    #     path('<str:name>',views.student)
    # ], )),
    #
    # path('result/<str:student_name>',views.result),
    path('login/',views.login),
    path('valid/',views.is_valid),
    path('friends/', views.friends),
    path('union/',views.union),
    path('sendrequest/',views.sendRequest),
]