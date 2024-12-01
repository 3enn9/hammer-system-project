import logging
import random
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer

from hammersite.forms import PhoneNumberForm, VerificationCodeForm
from hammersite.models import CustomUser
# from .utils import send_sms  # Функция для отправки SMS, которую нужно реализовать

User = get_user_model()

def send_code_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            user = User.objects.filter(phone_number=phone_number).first()

            if not user:
                user = User.objects.create_user(phone_number=phone_number)
                logging.info('Юзер добавился')

            # code = str(random.randint(1000, 9999))
            code = '1234'

            user.set_code(code)
            user.save()

            # Отправляем код пользователю (псевдо-реализация)
            # send_sms(phone_number, f'Ваш код подтверждения: {code}')

            request.session['phone_number'] = phone_number

            messages.success(request, 'Код подтверждения отправлен на ваш номер телефона!')
            return redirect('verify_code')
    else:
        form = PhoneNumberForm()
    return render(request, 'send_code.html', {'form': form})

def verify_code_view(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)

        if form.is_valid():
            phone_number = request.session.get('phone_number')
            code = form.cleaned_data['code']


            user = User.objects.filter(phone_number=phone_number).first()

            if user is None:
                messages.error(request, 'Пользователь с таким номером не найден!')
                return redirect('verify_code')

            if user.verify_code(code):

                login(request, user)
                messages.success(request, 'Вы успешно авторизованы!')
                return redirect('profile')
            else:
                messages.error(request, 'Неверный или истёкший код. Попробуйте снова.')
                return redirect('verify_code')
    else:
        form = VerificationCodeForm()

    return render(request, 'verify_code.html', {'form': form})


@login_required  
def profile_view(request):
    user = request.user  

    if request.method == 'POST':
        invite_code = request.POST.get('invite_code')


        if user.activate_invite_code:
            messages.error(request, 'Вы уже активировали инвайт код.')
            return redirect('profile')


        try:
            inviter = CustomUser.objects.get(invite_code=invite_code)
            if inviter != user:
                user.invited_users.add(inviter)

                user.activate_invite_code = True
                user.save()
                messages.success(request, 'Вы успешно активировали инвайт код!')
            else:
                messages.error(request, 'Вы не можете пригласить сами себя!')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Неверный инвайт код.')
            return redirect('profile')
        
        
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})


class ProfileView(APIView):

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SendCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            user = User.objects.create_user(phone_number=phone_number)

        # code = str(random.randint(1000, 9999))
        code = '1234'

        user.set_code(code) 
        user.save()

        # Отправка SMS-кода (здесь должна быть интеграция с сервисом отправки SMS)
        # Пример: sms_service.send_code(phone_number, code)

        return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)