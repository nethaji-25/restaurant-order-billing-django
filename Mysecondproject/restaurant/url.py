from django.urls import path
from restaurant import views

urlpatterns=[
    path('create_order/<table_id>',views.create_order,name='create_order'),
    path('add_order_items/<order_id>',views.add_order_items,name='add_order_items'),
    path('order_summary/<order_id>',views.order_summary,name='order_summary'),
    path('generate_bill/<order_id>',views.generate_bill,name='generate_bill'),
    path('mark_bill_paid/<bill_id>',views.mark_bill_paid,name='mark_bill_paid'),
    path('table_dashboard/',views.table_dashboard,name='table_dashboard'),
    path('kitchen/', views.kitchen_dashboard, name='kitchen'),
    path('mark_notification_read/<notification_id>',views.mark_notification_read,name='mark_notification_read'),
    path('export_bill_pdf/<bill_id>', views.export_bill_pdf, name='export_bill_pdf'),


]