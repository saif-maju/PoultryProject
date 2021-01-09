from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),    
    path('products/', views.ProductListView.as_view(), name='products'),
    path('categories/', views.categories, name='categories'),
    path('brands/', views.brands, name='brands'),
    path('scrap/', views.scrap, name='scrap'),    
 ]