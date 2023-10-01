import datetime
from smtplib import SMTPException
from urllib.error import HTTPError

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingLog, MailingSettings


def send_email(message_settings, message_client):
    """ Функция отправки рассылки клиентам рассылки + запись лога """

    result_text = 'OK'
    try:
        result = send_mail(
            subject=message_settings.message.subject,
            message=message_settings.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message_client.client.email],
            fail_silently=False
        )
    except SMTPException as e:
        result_text = e

    MailingLog.objects.create(
        status=MailingLog.STATUS_OK if result else MailingLog.STATUS_FAILED,
        settings=message_settings,
        client_id=message_client.client_id,
        server_response=result_text
    )


def send_mails():

    """ Проверяет необходимость отправки письма """

    datetime_now = datetime.datetime.now(datetime.timezone.utc)

    for mailing_settings in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):

        if (datetime_now > mailing_settings.start_time) and (datetime_now < mailing_settings.end_time):

            for mailing_client in mailing_settings.mailingclient_set.all():

                mailing_log = MailingLog.objects.filter(client=mailing_client.client, settings=mailing_settings)

                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-last_try').first().last_try
                    delta = (datetime_now - last_try_date).days

                    if mailing_settings.period == MailingSettings.PERIOD_DAILY:
                        if delta >= 1:
                            send_email(mailing_settings, mailing_client)
                    elif mailing_settings.period == MailingSettings.PERIOD_WEEKLY:
                        if delta >= 7:
                            send_email(mailing_settings, mailing_client)
                    elif mailing_settings.period == MailingSettings.PERIOD_MONTHLY:
                        if delta >= 30:
                            send_email(mailing_settings, mailing_client)
                else:
                    send_email(mailing_settings, mailing_client)
