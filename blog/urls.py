from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    # http://127.0.0.1:8000/blog/1
    path('<int:blog_pk>', views.blog_detial, name='blog_detial'),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]