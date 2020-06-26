from django.urls import path, re_path

from .views import (
    client_list_view,
    session_list_view,
    client_delete_view,
    staff_list_view,
    staff_delete_view,
    delete_staff,
    staff_edit_view,
    client_edit_view,
    sessions_choices_ajax,
)

urlpatterns = [
    path('', client_list_view, name='home'),
    path('clients/<int:pk>/delete',
         client_delete_view.as_view(), name='client-delete'),
    path('sessions-list/', session_list_view, name='sessions-list'),
    path('sessions-list/sessions_choices_ajax/',
         sessions_choices_ajax,
         name='sessions_choices_ajax'),
    path('staff-list/', staff_list_view, name='staff-list'),
    path('staff-list/<int:id>/delete-staff',
         delete_staff, name='delete-staff'),
    path('staff-list/<int:id>/edit', staff_edit_view, name='staff-edit'),
    path('clients/<int:id>/edit', client_edit_view, name='client-edit'),
]
