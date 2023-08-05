import os

from django.template.loader import render_to_string
from django.views.generic.base import TemplateView

from email_tools.emails import EmailPreviewContext, html_to_text
from email_tools.settings import email_settings


class EmailPreviewView(TemplateView):
    """
    Debug endpoint used for previewing how email templates will look.
    """

    template_name = "email_preview.html"

    def get_context_data(self, **kwargs):
        email_templates = os.listdir(email_settings.TEMPLATE_DIRECTORY)
        email_templates = [e.rsplit(".", 1)[0] for e in email_templates if e.endswith(".html")]

        email = None
        text_email = None
        context = None

        if "email" in self.request.GET:
            email_path = os.path.basename(self.request.GET.get("email"))
            context = EmailPreviewContext({})
            email = render_to_string(f"emails/{email_path}.html", context)
            text_email = html_to_text(email)

        return {
            "templates": email_templates,
            "email": email,
            "text_email": text_email,
            "variables": context.get_used_variables() if context is not None else [],
        }
