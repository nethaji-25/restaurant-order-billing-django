from django.urls import path
from CRUDapp import views


urlpatterns=[
    path('crudget/',views.Getemployees,name='crudget'),
    path('crudregister/',views.Addemployees,name='crudregister'),
    path('deletecrud/<id>',views.Deleteemployee,name='deletecrud'),
    path('update/<id>',views.Updateemployee,name='update'),
    path('search/',views.Searchemployee,name='search'),
    path('logincrud/',views.loginuser,name='logincrud'),
    path('logoutcrud/',views.logoutuser,name='logoutcrud')
]