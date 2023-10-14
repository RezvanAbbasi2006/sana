from rest_framework import routers
from django.urls import path, include
from clinic import views

router = routers.DefaultRouter()
router.register('reception', views.ReceptionViewSet, basename='reception')
router.register('visit', views.VisitViewSet, basename='visit')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('log_out/', views.log_out, name='log_out'),
    path('api/', include(router.urls)),
]
