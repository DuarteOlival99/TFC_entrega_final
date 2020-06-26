from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm
)
from django.contrib import messages
from django.contrib.auth.forms import (
    UserChangeForm,
    PasswordChangeForm
)
from .forms import UserRegisterForm
from clients.models import Event
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from clients.models import *
from clients.utils import Calendar
from .forms import EventForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.now()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    # define o driver e instructor por default a aparecer quando e criada uma nova sessao
    for staff in Profile.objects.all():
        if staff.firstName == "User":
            instance.instructor = staff
            instance.driver = staff

    for boat in Boat.objects.all():
        if boat.name == "teste":
            instance.boat = boat

    modalidade_qs = Modalidade.objects.all()
    if modalidade_qs.exists():
        for modalidade in modalidade_qs:
            if modalidade.name == "sky":
                instance.modality = modalidade

    instance.price = instance.modality.price

    instance.start_time = instance.start_time - timedelta(minutes=30)
    h3 = instance.end_time - instance.start_time
    duration_in_s = h3.total_seconds()
    instance.time = divmod(duration_in_s, 60)[0]

    instance.price = instance.modality.price * instance.time

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        if instance.client.balance >= instance.price:
            Event.objects.filter(id=instance.pk).update(payed=True)
            Client.objects.filter(name=instance.client.name).update(
                balance=(instance.client.balance - instance.price))
        else:
            Client.objects.filter(name=instance.client.name).update(
                debt=(instance.client.debt + instance.price))
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'session/event.html', {'form': form})


def event_show(request, event_id=None):
    # form = EventForm(request.POST or None)
    # return render(request, 'session/event_show.html', {'form': form})
    event = get_object_or_404(Event, pk=event_id)
    context = {'event': event}
    return render(request, 'session/event_show.html', context)


def client_show(request, client_id=None):
    client = get_object_or_404(Client, pk=client_id)

    balance = request.GET.get('balance')
    print(balance)
    if balance != None:
        client.balance += int('0' + balance)
        Client.objects.filter(id=client_id).update(
            balance=client.balance)

    sessions_qs = Event.objects.all()
    sessions_qs = Event.objects.order_by('-pk')

    context = {"client": client, "sessions": sessions_qs}
    return render(request, 'client/client_show.html', context)


def client_show_pay_sessions(request, client_id=None):
    client = get_object_or_404(Client, pk=client_id)

    balance = request.GET.get('balance')
    print(balance)
    if balance != None:
        client.balance += int('0' + balance)
        Client.objects.filter(id=client_id).update(
            balance=client.balance)

    s = []
    sessions_qs = Event.objects.all()
    sessions_qs = Event.objects.order_by('-pk')
    for session in sessions_qs:
        if session.client.name == client.name:
            s.append(session)

    for session in s:
        if client.balance >= session.price and session.payed == False:
            client.balance -= session.price
            client.debt -= session.price
            Event.objects.filter(id=session.pk).update(payed=True)

    print(client.balance)
    Client.objects.filter(id=client_id).update(
        balance=client.balance)
    Client.objects.filter(id=client_id).update(
        debt=client.debt)

    sessions_qs = Event.objects.all()
    sessions_qs = Event.objects.order_by('-pk')
    for session in sessions_qs:
        if session.client.name == client.name:
            s.append(session)

    context = {"client": client, "sessions": sessions_qs}
    return render(request, 'client/client_show.html', context)


def popUp(request):
    return render(request, 'client/add_balance.html')


def staff_show(request, staff_id=None):
    # form = EventForm(request.POST or None)
    # return render(request, 'session/event_show.html', {'form': form})
    staff = get_object_or_404(Profile, pk=staff_id)
    context = {'staff': staff}
    return render(request, 'staff/staff_show.html', context)


def event_edit(request, event_id=None):
    instance = Event()
    if id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)

        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sessions-list'))

    else:
        form = EventForm(instance=instance)

    context = {
        'form': form,
    }

    return render(request, 'session/event_edit.html', context)


class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/calendar'

    def test_func(self):
        return True


@login_required
def about_page(request):
    return render(request, "about.html", {"title": "About"})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            return redirect('staff-list')
        else:
            messages.error(request, 'Invalid registration')
            return redirect('register')
    else:
        form = UserRegisterForm()

        args = {'form': form}
        return render(request, 'staff/register.html', args)


def login(request):
    return render(request, 'registration/login.html', {'title': 'Login'})


def sessions(request):
    return render(request, 'session/sessions.html', {'title': 'sessions'})


def sessions_Details(request):
    return render(request, 'session/sessions_details.html', {'title': 'sessions'})


def sessions_Details_Edit(request):
    return render(request, 'session/session_edit.html', {'title': 'sessions'})


def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below.'))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/edit.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/profile.html', context)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['name', 'email', 'gender', 'birthday',
              'country', 'phone', 'nIF', 'balance', 'debt', 'discount', 'notes']


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })
