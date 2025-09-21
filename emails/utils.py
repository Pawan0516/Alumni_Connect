from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from alumniconnect.settings import EMAIL_HOST_USER as sender


def send_admin_onboarding_otp(to_email, otp_code):
    subject = "College Onboarding - Verify Your Email"
    context = {
        "otp_code": otp_code,
        "current_year": datetime.now().year,
    }

    html_content = render_to_string("emails/admin_onboarding_otp.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, sender, [to_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
