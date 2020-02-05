from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name='index'),
    # path('test/', views.promise_detail, name='promise_detail'),
    path('<int:promise_id>/', views.promise_detail, name='promise_detail'),
]
