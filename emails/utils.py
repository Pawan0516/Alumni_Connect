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

def send_invite_mail(to_email, otp_code):
    context = {
        "member_name": "Alice Smith",
        "college_name": "ABC College",
        "invitation_link": "https://alumniconnect.com/join/abc123",
        "current_year": datetime.now().year
    }

    subject="You're Invited to Join Alumni Connect"
    

    html_content = render_to_string("emails/invite_member.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, sender, [to_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
