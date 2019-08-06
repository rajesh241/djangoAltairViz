from django.urls import path
from .views import cricket,exportView,NFHSView
from . import views
urlpatterns = [ 
                path('cricket/', cricket.as_view()),
                path('export/', exportView.as_view()),
                path('nfhs/', NFHSView.as_view()),
                path('', cricket.as_view()),
        ]
