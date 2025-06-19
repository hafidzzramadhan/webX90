from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),        # untuk web HTML
    path('', include('myapp.api_urls')),    # untuk API REST
]
