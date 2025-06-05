from django.urls import path
from .views import login_view
from .views import sistem_view
from .views import dashboard_view

urlpatterns = [
    path('login', login_view, name='login'),
    path('sistem/', sistem_view, name='sistem'),
    path('dashboard/', dashboard_view, name='dashboard'),

]
