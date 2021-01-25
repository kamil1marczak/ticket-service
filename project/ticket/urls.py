"""ticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ticket_platform.views import EventListingView, AddEventView, EventUpdateView, EventDeleteView, BuyTicketView, UserLoginView, UserLogoutView, SignUpView, BuyReservedView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('', EventListingView.as_view(), name='listing'),
    path('add_event/', AddEventView.as_view(), name='add_event'),
    path('buy_reserved/', BuyReservedView.as_view(), name='buy_reserved'),
    path('buy_ticket/<int:event_pk>/<int:ticket_type>/<int:sold_reserved>/', BuyTicketView.as_view(), name='buy_ticket'),
    # path('buy_ticket/', BuyTicketView.as_view(), name='buy_ticket'),
    path('<pk>/event_update/', EventUpdateView.as_view(), name='update_event'),
    path('<pk>/event_delete/', EventDeleteView.as_view(), name='delete_event'),
    # path('ticket/', TicketManagementView.as_view(), name='ticket_management')
]
