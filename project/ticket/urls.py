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
from django.urls import path, include, re_path
from ticket_platform.views import EventListingView, AddEventView, EventUpdateView, EventDeleteView, BuyTicketView, \
    UserLoginView, UserLogoutView, SignUpView, BuyReservedView, EventViewSet, TicketSetView, AccountSetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter, SimpleRouter
from .routers import ReadOnlyRouter
import debug_toolbar

router = SimpleRouter()
read_only_router = ReadOnlyRouter()
router.register(r'event', EventViewSet)
router.register(r'ticket', TicketSetView)
read_only_router.register(r'account', AccountSetView)
# from django.conf import settings

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(read_only_router.urls)),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('', EventListingView.as_view(), name='listing'),
    # path('api/event_list/', APIEventListingView.as_view(), name='api_event'),

    # re_path(r'^api/event_list/$', APIEventListingView.as_view(), name='api_event'),
    # path('api/ticket/', APITicketView.as_view(), name='api_ticket'),
    path('add_event/', AddEventView.as_view(), name='add_event'),
    path('buy_reserved/', BuyReservedView.as_view(), name='buy_reserved'),
    path('buy_ticket/<int:event_pk>/<int:ticket_type>/<int:sold_reserved>/', BuyTicketView.as_view(),
         name='buy_ticket'),
    # path('buy_ticket/', BuyTicketView.as_view(), name='buy_ticket'),
    path('<pk>/event_update/', EventUpdateView.as_view(), name='update_event'),
    path('<pk>/event_delete/', EventDeleteView.as_view(), name='delete_event'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("__debug__/", include(debug_toolbar.urls)),

    # path('ticket/', TicketManagementView.as_view(), name='ticket_management')
]

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     # Serve static and media files from development server
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
#     import debug_toolbar
#
#     urlpatterns = [
#                       path('__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns
#
# # urlpatterns += router.urls
