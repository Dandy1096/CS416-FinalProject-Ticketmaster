from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('search',views.search,name='search'),
    path('saveTicket', views.saveTicket, name='save_ticket'),
    path('ticket/<int:id>', views.ticket, name='view_ticket'),
    path('my_tickets',views.myTickets,name='my_tickets'),
    path('update/<int:id>',views.updateTicket,name='update_ticket'),
    path('delete/<int:id>',views.deleteTicket,name='delete_ticket'),

]