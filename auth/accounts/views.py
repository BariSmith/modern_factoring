import random

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.shortcuts import get_object_or_404
# Create your views here.
#
#
# link = r'https://2factor.in/API/R1/?module=TRANS_SMS& apikey=18ca992b-ba95-11ea-9fa5-0200cd936042&to=(phone)& from=Stanga&templatename=testtask1& var1=(name)& var2=(otp_key)'
#
# requests.get(link)

class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.object.filter(phone_number = phone)
            if user.exists():
                return Response({
                    'status' : False,
                    'detail' : 'phone number already exist'
                })
            else:
                key = send_otp(phone)
                if key:
                    pass

                else:
                    return Response({
                        'status': False,
                        'detail': 'sending otp error'
            return Response({
                'status' : False,
                'detail' : "Phone number is not given in post request"
            })



def send_otp(phone):
    if phone:
        random.random(999, 9999)
        return key
    else:
        return False