from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'Cars', CarViewSet)
router.register(r'Drivers', DriverViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', cars, name='cars'),
    path('add_car/', add_car, name='add_car'),
    path('<int:pk>/car_edit/', car_edit, name='car_edit'),
    path('<int:pk>/car_info/', car_info, name='car_info'),
    path('drivers/', drivers, name='drivers'),
    path('add_driver/', add_driver, name='add_driver'),
    path('<int:pk>/driver_edit/', driver_edit, name='driver_edit'),
    path('<int:pk>/driver_info/', driver_info, name='driver_info'),
    path('<int:pk>/event_info/', event_info, name='event_info'),
    path('<int:pk>/add_car_event/', add_car_event, name='add_car_event'),
    path('<int:pk>/event_edit/', event_edit, name='event_edit'),
    path('<int:pk>/add_photo/', add_photo, name='add_photo'),
    path('<int:pk>/add_techpassport/', add_techpassport, name='add_techpassport'),
    path('<int:pk>/techpassport_info/', techpassport_info, name='techpassport_info'),
    path('<int:pk>/techpassport_edit/', techpassport_edit, name='techpassport_edit'),
    path('<int:pk>/add_techpassport_scans/', add_techpassport_scans, name='add_techpassport_scans'),
    path('<int:pk>/passport_info/', passport_driver_info, name='passport_info'),
    path('<int:pk>/passport_edit/', passport_driver_edit, name='passport_edit'),
    path('<int:pk>/add_passport/', add_passport_driver, name='add_passport'),
    path('<int:pk>/add_passport_scans/', add_passport_driver_scans, name='add_passport_scans'),
]
