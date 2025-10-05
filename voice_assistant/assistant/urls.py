from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.assistant_api, name='assistant_api'),  # ✅ Add this
]
