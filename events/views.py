from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import Event, Registration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import EventForm,PasswordsChangeForm
from django.contrib.auth.views import PasswordChangeView



class HomeView(ListView):
    model = Event
    template_name='index.html'

class EventView(LoginRequiredMixin,ListView):
    model = Event
    template_name='event_list.html'

class EventDetailView(LoginRequiredMixin,DetailView):
    model =Event
    template_name="event_detail.html"

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'event_form.html'
    form_class = EventForm
    redirect_field_name="login"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('eventdetail', kwargs={'pk': self.object.pk})


@login_required(login_url="login")
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    registration = Registration(event=event, user=user)
    registration.save()
    return redirect('user-registered-events')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_update_form.html'
    redirect_field_name="login"
    
    def get_success_url(self):
        return reverse('eventdetail', kwargs={'pk': self.object.pk})

class EventDeleteView(LoginRequiredMixin,DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')
    redirect_field_name="login"



class UserRegisteredEventsView(LoginRequiredMixin, ListView):
    template_name = 'user_registered_events.html'
    context_object_name = 'registered_events'
    redirect_field_name="login"

    def get_queryset(self):
        # Retrieve events registered by the current user
        return Registration.objects.filter(user=self.request.user)


@login_required(login_url="login")
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    registration = Registration.objects.filter(event=event, user=user).first()
    if registration:
        registration.delete()
    # Redirect to the event detail page
    return redirect('eventdetail', pk=event_id)


class PasswordsChangeView(LoginRequiredMixin,PasswordChangeView):
    form_class = PasswordsChangeForm
    template_name="change_password.html"
    
    def get_success_url(self):
        return reverse('password_success')

@login_required(login_url="login")    
def password_success(request):
    return render(request, 'password_success.html',{})


@login_required(login_url="login")  
def event_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        print("Query:", query)  # Debugging statement
        if query:
            events = Event.objects.filter(name__icontains=query)
            print("Filtered Events SQL:", events.query)  # Debugging statement
        else:
            events = Event.objects.all()

        return render(request, 'event_search.html', {'events': events, 'query': query})
    else:
        return render(request, 'event_search.html')
