from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('flights.urls')),
    path('api/auth/', include('accounts.urls')),
]
