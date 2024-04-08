import smtplib
import ssl
import datetime as dt
import time
from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def user(request):
    sender_email = request.POST.get('s_mail', 'default')
    password = request.POST.get('password', 'default')
    receiver_email = request.POST.get('r1_mail','default')
    subject = request.POST.get('subject', 'default')
    message_content = request.POST.get('message', 'default')
    date_send = request.POST.get('date','default')
    time_send = request.POST.get('time','default')
    date_parts = date_send.split("-")
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    time_parts = time_send.split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    port = 587
    smtp_server = "smtp.gmail.com"

    message = f"""\
    Subject: {subject}

    {message_content}"""

    context = ssl.create_default_context()
    send_time = dt.datetime(year, month, day, hours, minutes, seconds)
    current_time = dt.datetime.now()
    time_difference = (send_time - current_time).total_seconds()

    try:
        with smtplib.SMTP(smtp_server, port) as email:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            email.starttls(context=context)
            email.login(sender_email, password)
            send_time = dt.datetime(year, month, day, hours, minutes, seconds)
            current_time = dt.datetime.now()
            time_difference = (send_time - current_time).total_seconds()
            
            if time_difference > 0:
                print(f"Waiting for {time_difference} seconds before sending the email...")
                time.sleep(time_difference)
                email.sendmail(sender_email, receiver_email, message)
                print('Email sent')
                params = {'position':f"Waiting for {time_difference} seconds before sending the email..."}
                
            else:
                print('Invalid send time. Email not sent.')
                params = {'position':'Invalid send time. Email not sent.'}
            
    except Exception as e:
        print(f"An error occurred: {e}")
        params = {'position':"An error occurred: please fill correct details"}
    
    return render(request,'user.html',params)
