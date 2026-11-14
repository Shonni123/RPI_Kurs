import logging
from django.conf import settings
from django.core.mail import send_mail
from .models import EmailVerificationCode

logger = logging.getLogger(__name__)


def send_verification_email(user, code_obj: EmailVerificationCode):
    """
    Отправляет 6-значный код на почту пользователя.
    В зависимости от назначения письма (регистрация или сброс пароля)
    формирует соответствующую тему и текст.
    """
    first_name = user.first_name.strip() if user.first_name else ''
    greeting_name = first_name or user.username or 'пользователь'

    if code_obj.purpose == EmailVerificationCode.Purpose.RESET_PASSWORD:
        subject = f'Код сброса пароля: {code_obj.code} — АВИАРЕЙСЫ'
        message = (
            f'Здравствуйте, {greeting_name}!\n\n'
            f'Вы запросили восстановление пароля в сервисе «Авиарейсы».\n'
            f'Ваш 6-значный код для подтверждения сброса пароля:\n\n'
            f'    {code_obj.code}\n\n'
            f'Срок действия кода: 15 минут.\n'
            f'Если вы не отправляли этот запрос, проигнорируйте данное сообщение.\n\n'
            f'---\nИнформационный сервис «Авиарейсы»'
        )
    else:
        subject = f'Код подтверждения почты: {code_obj.code} — АВИАРЕЙСЫ'
        message = (
            f'Здравствуйте, {greeting_name}!\n\n'
            f'Благодарим за регистрацию в сервисе «Авиарейсы».\n'
            f'Ваш 6-значный код для подтверждения электронной почты:\n\n'
            f'    {code_obj.code}\n\n'
            f'Срок действия кода: 15 минут.\n'
            f'Если вы не регистрировались на сайте, просто проигнорируйте это письмо.\n\n'
            f'---\nИнформационный сервис «Авиарейсы»'
        )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'Авиарейсы <noreply@aviaraces.ru>'),
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f'Verification email sent to {user.email} (purpose: {code_obj.purpose}, code: {code_obj.code})')
        return True
    except Exception as e:
        logger.error(f'Failed to send email to {user.email}: {e}')
        return False

