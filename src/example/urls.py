from django.urls import path
from .views import cricket
from . import views
urlpatterns = [ 
                path('cricket/', cricket.as_view()),
                path('', cricket.as_view()),
        ]
