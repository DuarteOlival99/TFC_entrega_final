"""nucleos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from tootsie import views as tootsie_views
from .views import ClientCreateView, SessionDeleteView

from .views import about_page
from django.conf.urls import url


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls'), name='accounts/login'),
    re_path(r'^about/$', about_page, name='about'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='templates/registration/logout.html'), name='logout'),
    path('sessions', views.sessions, name='sessions'),
    path('sessions-details', views.sessions_Details, name='sessions-details'),
    path('sessions-details-edit', views.sessions_Details_Edit,
         name='sessions-details-edit'),
    path('client-create', ClientCreateView.as_view(), name='client-create'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/(?P<event_id>\d+)/edit/$',
        views.event_edit, name='event_edit'),
    url(r'^event/(?P<event_id>\d+)/$',
        views.event_show, name='event_show'),
    url(r'^client/(?P<client_id>\d+)/$',
        views.client_show, name='client_show'),
    url(r'^client/(?P<client_id>\d+)/pay/sessions/$',
        views.client_show_pay_sessions, name='pay-sessions'),
    url(r'^staff/(?P<staff_id>\d+)/$',
        views.staff_show, name='staff_show'),
    path('event/<int:pk>/delete/',
         SessionDeleteView.as_view(), name='session-delete'),
    path('profile', views.profile, name='profile'),
    path('popUp', views.popUp, name='popUp'),
    path('profile/edit', views.profile_edit, name='profile-edit'),
    path('profile/edit/change-password',
         views.change_password, name='change-password'),
    url(r'^profile/password/$', views.change_password, name='change_password'),
    url(r'^register/$', views.register, name='register'),
    path('', include('clients.urls')),
] + staticfiles_urlpatterns()


if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
