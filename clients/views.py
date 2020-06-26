from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import Http404
from django.core.files import File
from django.db.models import Max
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.utils.encoding import smart_text
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from tootsie.forms import UserUpdateForm, ProfileUpdateForm
from .models import Client, Event, Profile, Modalidade
from django.urls import reverse
from .forms import SessionFilterForm, ClientFilterForm, ClientUpdateForm

# Create your views here.


@login_required
def client_list_view(request):
    clients_qs = Client.objects.all()
    result = False

    clientOrder = request.GET.get('idOrder')
    balance = request.GET.get('balance')
    debt = request.GET.get('debt')
    discount = request.GET.get('discount')
    clientId = request.GET.get('clientID')

    if clients_qs.exists():
        result = True
        clients_qs = clients_qs.order_by('-pk')
        s = []

        if clientId != None and clientId != "":
            clients_qs = clients_qs.filter(id=clientId)
            template_name = 'clients/list.html'
            context = {'clients': clients_qs, 'form': ClientFilterForm}
            return render(request, template_name, context)

        if clientOrder != None:
            if clientOrder == "descending":
                clients_qs = clients_qs.order_by('-pk')
            else:
                clients_qs = clients_qs.order_by('pk')

        if balance != None:
            if balance == "ascending":
                clients_qs = sorted(clients_qs, key=lambda ModelClass: int(
                    ModelClass.balance))
            elif balance == "descending":
                clients_qs = sorted(clients_qs, key=lambda ModelClass: int(
                    ModelClass.balance), reverse=True)

        if debt != None:
            if debt == "ascending":
                clients_qs = sorted(clients_qs, key=lambda ModelClass: int(
                    ModelClass.debt))
            elif debt == "descending":
                clients_qs = sorted(clients_qs, key=lambda ModelClass: int(
                    ModelClass.debt), reverse=True)

        if discount != None:
            if discount == "ascending":
                clients_qs = sorted(clients_qs, key=lambda ModelClass: int(
                    ModelClass.discount))
            elif discount == "descending":
                clients_qs = sorted(clients_qs, key=lambda ModelClass: int(
                    ModelClass.discount), reverse=True)

    if result:
        template_name = 'clients/list.html'
        context = {'clients': clients_qs, 'form': ClientFilterForm}
    else:
        template_name = 'clients/list.html'
        context = {'clients': None, 'form': ClientFilterForm}

    return render(request, template_name, context)


class client_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = '/'  # Home

    def test_func(self):
        return True


class staff_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    success_url = '/staff-list'

    def test_func(self):
        return True


def client_edit_view(request, id=None):
    instance = Client()
    if id:
        instance = get_object_or_404(Client, pk=id)
    else:
        instance = Client()

    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=instance)

        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('client_show', kwargs={'client_id': id}))

    else:
        form = ClientUpdateForm(instance=instance)

    context = {
        'form': form,
    }

    return render(request, 'clients/edit.html', context)


def staff_edit_view(request, id=None):
    instance = Profile()
    if id:
        instance = get_object_or_404(Profile, pk=id)
    else:
        instance = Profile()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=instance.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=instance)

        if request.POST and u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return HttpResponseRedirect(reverse('staff-list'))

    else:
        u_form = UserUpdateForm(instance=instance.user)
        p_form = ProfileUpdateForm(instance=instance)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'staff/edit.html', context)


def delete_staff(request, id):
    obj = get_object_or_404(Profile, id=id)
    if request.method == "POST":
        obj.delete_user()
        return redirect('staff-list')
    context = {
        "object": obj
    }
    return render(request, "staff/profile_delete.html", context)


@login_required
def session_list_view(request):

    sessionOrder = request.GET.get('sessionOrder')
    p = request.GET.get('payed')
    t = request.GET.get('time')
    m = request.GET.get('modality')
    d = request.GET.get('driver')
    i = request.GET.get('instructor')
    b = request.GET.get('boat')
    c = request.GET.get('sessionID')
    print("form")
    form = SessionFilterForm()
    #newForm = form.save()
    # print(newForm)

    if p == "False":
        sessions_qs = Event.objects.filter(payed=False)
        sessions_qs = sessions_qs.order_by('-pk')
    elif p == "True":
        sessions_qs = Event.objects.filter(payed=True)
        sessions_qs = sessions_qs.order_by('-pk')
    else:
        sessions_qs = Event.objects.all()
        sessions_qs = sessions_qs.order_by('-pk')

    if sessions_qs.exists():
        s = []

        if c != None and c != '':
            sessions_qs = sessions_qs.filter(id=c)
            template_name = 'Session/sessions_list.html'
            context = {'events': sessions_qs, 'form': form}
            return render(request, template_name, context)

        if sessionOrder != None:
            if sessionOrder == "descending":
                sessions_qs = sessions_qs.order_by('-pk')
            else:
                sessions_qs = sessions_qs.order_by('pk')

        if t != None and t != "indifferent":
            if t == "descending":
                sessions_qs = sessions_qs.order_by('-time')
            else:
                sessions_qs = sessions_qs.order_by('time')

        if m != None and m != "All":
            for session in sessions_qs:
                if session.modality.name == m:
                    s.append(session)
            sessions_qs = s
            s = []
        else:
            print("modality = All")

        if d != None and d != "All":
            for session in sessions_qs:
                if session.driver.firstName == d:
                    s.append(session)
            sessions_qs = s
            s = []
        else:
            print("driver = All")

        if i != None and i != "All":
            for session in sessions_qs:
                if session.instructor.firstName == i:
                    s.append(session)
            sessions_qs = s
            s = []
        else:
            print("instructor = All")

        if b != None and b != "All":
            for session in sessions_qs:
                if session.boat.name == b:
                    s.append(session)
            sessions_qs = s
            s = []
        else:
            print("Boat = All")

        template_name = 'Session/sessions_list.html'
        context = {'events': sessions_qs, 'form': form}
    else:
        template_name = 'Session/sessions_list.html'
        context = {'events': None, 'form': form}

    return render(request, template_name, context)


@login_required
def sessions_choices_ajax(request):
    uf = request.GET.get('payed')
    if uf == "False":
        sessions_qs = Event.objects.filter(payed=False)
    elif uf == "True":
        sessions_qs = Event.objects.filter(payed=True)
    else:
        sessions_qs = Event.objects.all()

    template_name = 'Session/sessions_choices_ajax.html'
    context = {'events': sessions_qs}
    return render(request, template_name, context)


@login_required
def staff_list_view(request):
    profile_qs = Profile.objects.all()
    template_name = 'staff/list.html'

    context = {'profile': profile_qs}
    return render(request, template_name, context)
