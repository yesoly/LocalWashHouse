from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.main, name="main"),
    path('main/wash/', views.getOrder, name='wash'),
    path('main/wash/search', views.searchCustomer, name='search'),
    path('main/wash/customer/', views.customer, name='customer'),
    path('main/message/', views.message, name='message'),
    path('main/manage/', views.manage, name='manage'),
    path('main/manage/csv', views.saveCSV, name='saveCSV'),
    path('main/login/', views.login, name='login'),
    path('main/signup/', views.signup, name='signup'),
    path('main/logout/', views.logout, name='logout'),
    path('main/profile/', views.profile, name='profile'),

]
