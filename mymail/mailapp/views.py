from .controller import receive_mail_content, send_email_content

from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request, 'index.html')

def receive_emails(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        request.session['email'] = email
        request.session['password'] = password

        try:
            emails = receive_mail_content(email, password)

            context = {'emails': emails}
            return render(request, 'mails.html', context)
        except:
            return redirect('mailapp:error')

    return HttpResponse('Unknown request method')

def send_email(request):
    email = request.session.get('email')
    password = request.session.get('password')
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        try:
            send_email_content(recipient, subject, message, email, password)
            emails = receive_mail_content(email, password)

            context = {'emails': emails}
            return render(request, 'mails.html', context)
        except:
            return redirect('mailapp:error')