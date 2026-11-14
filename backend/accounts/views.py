from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import UserProfile, EmailVerificationCode
from .services import send_verification_email
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    VerifyCodeSerializer,
    ResendCodeSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
)


class RegisterAPIView(views.APIView):
    """
    Регистрация нового пользователя.
    Создает аккаунт и отправляет 6-значный код подтверждения на почту.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        full_name = serializer.validated_data.get('fullName', '').strip()

        # Проверяем, существует ли уже неподтвержденный пользователь
        user = User.objects.filter(email__iexact=email).first()
        if user:
            # Обновляем пароль и имя для повторной попытки
            user.set_password(password)
            if full_name:
                user.first_name = full_name
            user.save()
        else:
            username = email.lower()
            # Если имя пользователя уже занято кем-то другим
            if User.objects.filter(username=username).exists():
                username = f"{email.split('@')[0]}_{User.objects.count() + 1}"

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
                is_active=True,
            )

        # Профиль пользователя
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_email_verified = False
        profile.save()

        # Генерация 6-значного кода
        code_obj = EmailVerificationCode.generate_for_user(
            user=user,
            purpose=EmailVerificationCode.Purpose.VERIFY_EMAIL
        )

        # Отправка письма
        email_sent = send_verification_email(user, code_obj)

        return Response({
            'success': True,
            'message': f'Код подтверждения отправлен на почту {email}',
            'email': email,
            'emailSent': email_sent,
            'debugCode': code_obj.code if settings.DEBUG else None,
        }, status=status.HTTP_201_CREATED)


class VerifyCodeAPIView(views.APIView):
    """
    Подтверждение email 6-значным кодом.
    При успехе активирует пользователя и возвращает токен авторизации.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code'].strip()
        purpose = serializer.validated_data.get('purpose', EmailVerificationCode.Purpose.VERIFY_EMAIL)

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({'success': False, 'error': 'Пользователь с таким email не найден.'}, status=status.HTTP_404_NOT_FOUND)

        verification_entry = EmailVerificationCode.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False
        ).first()

        if not verification_entry:
            return Response({'success': False, 'error': 'Код подтверждения не найден. Запросите код повторно.'}, status=status.HTTP_400_BAD_REQUEST)

        if verification_entry.is_expired():
            return Response({'success': False, 'error': 'Срок действия кода истёк (15 минут). Запросите новый код.'}, status=status.HTTP_400_BAD_REQUEST)

        if verification_entry.code != code:
            return Response({'success': False, 'error': 'Неверный 6-значный код. Проверьте цифры из письма.'}, status=status.HTTP_400_BAD_REQUEST)

        # Код верный!
        verification_entry.is_used = True
        verification_entry.save()

        if purpose == EmailVerificationCode.Purpose.VERIFY_EMAIL:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.is_email_verified = True
            profile.save()
            user.is_active = True
            user.save()

        # Авторизуем пользователя и отдаем токен
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'success': True,
            'message': 'Почта успешно подтверждена!',
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class ResendCodeAPIView(views.APIView):
    """
    Повторная отправка 6-значного кода подтверждения.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        purpose = serializer.validated_data.get('purpose', EmailVerificationCode.Purpose.VERIFY_EMAIL)

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({'success': False, 'error': 'Пользователь с таким email не найден.'}, status=status.HTTP_404_NOT_FOUND)

        code_obj = EmailVerificationCode.generate_for_user(user=user, purpose=purpose)
        email_sent = send_verification_email(user, code_obj)

        return Response({
            'success': True,
            'message': f'Новый код отправлен на {email}',
            'email': email,
            'emailSent': email_sent,
            'debugCode': code_obj.code if settings.DEBUG else None,
        }, status=status.HTTP_200_OK)


class LoginAPIView(views.APIView):
    """
    Вход в систему по email (или username) и паролю.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': 'Неверный email или пароль.'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Если почта ещё не подтверждена
        if not profile.is_email_verified:
            # Генерируем свежий код на всякий случай
            code_obj = EmailVerificationCode.generate_for_user(
                user=user,
                purpose=EmailVerificationCode.Purpose.VERIFY_EMAIL
            )
            send_verification_email(user, code_obj)

            return Response({
                'success': False,
                'requiresVerification': True,
                'email': user.email,
                'message': 'Ваша почта ещё не подтверждена. Мы отправили свежий код подтверждения.',
                'debugCode': code_obj.code if settings.DEBUG else None,
            }, status=status.HTTP_200_OK)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'success': True,
            'message': 'Успешный вход в систему!',
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class PasswordResetRequestAPIView(views.APIView):
    """
    Запрос на восстановление пароля.
    Отправляет 6-значный код сброса на указанную почту.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].lower().strip()
        user = User.objects.filter(email__iexact=email).first()

        if not user:
            # Для безопасности не раскрываем факт отсутствия email в базе
            return Response({
                'success': True,
                'message': f'Если аккаунт с почтой {email} зарегистрирован, код для сброса пароля отправлен.',
                'email': email,
            }, status=status.HTTP_200_OK)

        code_obj = EmailVerificationCode.generate_for_user(
            user=user,
            purpose=EmailVerificationCode.Purpose.RESET_PASSWORD
        )
        email_sent = send_verification_email(user, code_obj)

        return Response({
            'success': True,
            'message': f'Код для сброса пароля отправлен на почту {email}',
            'email': email,
            'emailSent': email_sent,
            'debugCode': code_obj.code if settings.DEBUG else None,
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(views.APIView):
    """
    Подтверждение сброса пароля по 6-значному коду и установка нового пароля.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            first_err = next(iter(serializer.errors.values()))[0] if serializer.errors else 'Ошибка валидации'
            return Response({'success': False, 'error': first_err, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code'].strip()
        new_password = serializer.validated_data['newPassword']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({'success': False, 'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        verification_entry = EmailVerificationCode.objects.filter(
            user=user,
            purpose=EmailVerificationCode.Purpose.RESET_PASSWORD,
            is_used=False
        ).first()

        if not verification_entry:
            return Response({'success': False, 'error': 'Код сброса пароля не найден. Пожалуйста, запросите код повторно.'}, status=status.HTTP_400_BAD_REQUEST)

        if verification_entry.is_expired():
            return Response({'success': False, 'error': 'Срок действия кода истёк (15 минут). Запросите новый код.'}, status=status.HTTP_400_BAD_REQUEST)

        if verification_entry.code != code:
            return Response({'success': False, 'error': 'Неверный 6-значный код сброса пароля.'}, status=status.HTTP_400_BAD_REQUEST)

        # Код верный! Обновляем пароль
        user.set_password(new_password)
        user.save()

        verification_entry.is_used = True
        verification_entry.save()

        # Также подтверждаем почту, раз пользователь подтвердил доступ к ней
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_email_verified = True
        profile.save()

        # Пересоздаем токен для безопасного авто-входа
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({
            'success': True,
            'message': 'Пароль успешно изменён! Вы вошли в систему с новым паролем.',
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class CurrentUserAPIView(views.APIView):
    """
    Получение и обновление данных текущего авторизованного пользователя.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data,
        })

    def put(self, request):
        user = request.user
        full_name = request.data.get('fullName')
        phone = request.data.get('phone')

        if full_name is not None:
            user.first_name = full_name.strip()
            user.save()

        if phone is not None:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone = phone.strip()
            profile.save()

        return Response({
            'success': True,
            'message': 'Профиль успешно обновлён!',
            'user': UserSerializer(user).data,
        })


class ChangePasswordAPIView(views.APIView):
    """
    Смена пароля из личного кабинета (требует ввода старого пароля).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        old_password = serializer.validated_data['oldPassword']
        new_password = serializer.validated_data['newPassword']

        if not user.check_password(old_password):
            return Response({'success': False, 'error': 'Текущий пароль указан неверно.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        # Обновляем токен
        Token.objects.filter(user=user).delete()
        new_token = Token.objects.create(user=user)

        return Response({
            'success': True,
            'token': new_token.key,
            'message': 'Пароль успешно изменён!',
        })


class LogoutAPIView(views.APIView):
    """
    Выход из системы. Удаляет текущий токен авторизации.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return Response({'success': True, 'message': 'Вы успешно вышли из системы.'})
