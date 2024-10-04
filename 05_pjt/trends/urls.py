from django.urls import path
from . import views
app_name= 'trends'

urlpatterns = [
    path('keyword/', views.keyword, name='keyword'),
    path('keyword/<int:pk>/', views.keyword_detail, name='delete'),
    path('crawling/', views.crawling, name='crawling'),
    path('crawling/histogram/', views.crawling_histogram, name='histogram'),
    path('crawling/advanced/', views.crawling_advanced, name='advanced'),
]
