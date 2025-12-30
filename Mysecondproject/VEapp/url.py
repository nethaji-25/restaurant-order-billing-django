from django.urls import path
from VEapp import views

urlpatterns=[
    path('get/',views.get_apis,name='get'),
    path('post/',views.post_apis,name='post'),
    path('put/<id>',views.put_apis,name='put'),
    path('del/<id>',views.delete_api,name='del')
]