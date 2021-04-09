from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.db.models import Q
from . import views
from . import models
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .models import User, Request, Customer
from main.forms import SignupForm, CustomerForm, OrderForm, CustomerForm2, SearchForm
from django.contrib import messages
import csv
from .resources import RequestResource
from django.http import HttpResponse
from django.contrib import messages
from twilio.rest import Client
from .forms import SendMessageForm
# Create your views here.


User = get_user_model()


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "main/signup.html"

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('main:main')


signup = SignupView.as_view()


class LoginView(auth_views.LoginView):
    template_name = "main/login.html"
    redirect_authenticated_user = True


login = LoginView.as_view()

logout = auth_views.LogoutView.as_view()


def profile(request):
    return render(request, 'main/profile.html')


class WashView(TemplateView):
    template_name = "main/wash.html"
    redirect_authenticated_user = True

    def add_customer(self, request, *args, **kwargs):
        return render(request, 'main/customer.html')


wash = WashView.as_view()


class CustomerView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "main/customer.html"

    def form_valid(self, form):
        customer = form.save()
        return redirect('main:wash')


customer = CustomerView.as_view()


class MessageView(ListView):
    template_name = "main/message.html"
    redirect_authenticated_user = True
    model = Customer

    def get_queryset(self):
        word = self.request.GET.getlist('word')
        queryset = super(MessageView, self).get_queryset()
        if word:
            queryset.filter(
                Q(phone_num__contains=word) |
                Q(name__contains=word)
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessageView, self).get_context_data(
            object_list=None, **kwargs)
        context['form'] = SearchForm()
        return context

    def get(self, request, *args, **kwargs):
        return super(MessageView, self).get(request, *args, **kwargs)


message = MessageView.as_view()


class ManageView(TemplateView):
    template_name = "main/manage.html"


manageView = ManageView.as_view()


def manage(request):
    request_info = Request.objects.all().select_related("phone_num")
    request_context = {'request_info': request_info}

    return render(request, 'main/manage.html', request_context)


def main(request):
    requests = Request.objects.all()
    return render(request, 'main/main.html', {'requests': requests})


def getOrder(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        customer = CustomerForm2()
        order = OrderForm()
        return render(request, 'main/wash.html', {'customer': customer, 'order': order})
    else:
        pass


def searchCustomer(request):
    customer_list = customer.objects.filter(phone_num='0100000000')
    # print(customer_list)
    return render(request, 'main/wash.html', {'customer': customer_list})


def saveCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="abc.csv"'

    request_resource = RequestResource()
    dataset = request_resource.export()
    dataset.csv

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    writer.writerow([
        str(u"요청번호"),
        str(u"고객번호"),
        str(u"의류"),
        str(u"서비스 종류"),
        str(u"서비스 상태"),
        str(u"요청 날짜"),
        str(u"예상 날짜"),
        str(u"완료 날짜"),
        str(u"찾아간 날짜"),
        str(u"요청사항"),
        str(u"가격"),
    ])

    for x in dataset:
        writer.writerow(x)

    return response


def message(request):
    form_class = SendMessageForm

    send_message_form = form_class(request.POST or None)
    if request.method == 'POST':

        #send_message_form = SendMessageForm(request.POST)

        if send_message_form.is_valid():
            account_sid = 'AC155820cd778430b90f0b858fb5635d9b'
            auth_token = '888b211e0bfd4cf40237999b30cfad8b'
            client = Client(account_sid, auth_token)

            customer_name = request.POST.get('customer_name')
            customer_number = request.POST.get('customer_number')
            input_number = '+82' + customer_number[1:]

            #category = request.POST.get('category')
            category = send_message_form.cleaned_data.get('category')
            input_message = request.POST.get('input_message')

            message = client.messages.create(
                body=customer_name + "님 " + input_message,
                from_='+12015819428',
                to=input_number
            )
            print(message.sid)
    # GET
    else:
        message = MessageView.as_view()

    context = {
        'form': send_message_form,
    }
    
    return render(request, 'main/message.html', context)
