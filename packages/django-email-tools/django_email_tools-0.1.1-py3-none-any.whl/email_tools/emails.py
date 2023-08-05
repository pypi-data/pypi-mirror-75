import re

from bs4 import BeautifulSoup, NavigableString
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from email_tools.settings import email_settings


def send_email(
    template,
    context,
    subject="",
    to=None,
    from_email=None,
    bcc=None,
    connection=None,
    attachments=None,
    headers=None,
    alternatives=None,
    cc=None,
    reply_to=None,
):
    """
    Send an email given a template, context, and to email.
    """

    html_content = render_to_string(template, context)
    text_content = html_to_text(html_content)
    send_to = to if isinstance(to, list) else [to]
    from_email = from_email if from_email is not None else email_settings.FROM_EMAIL

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        send_to,
        bcc,
        connection,
        attachments,
        headers,
        alternatives,
        cc,
        reply_to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def html_to_text(html):
    """
    Cleans up HTML and converts into a text-only format,
    trying to preserve links and other objects.
    Used for the text-only version of emails.
    """
    if html is None:
        return None

    def traverse(children):
        output = ""
        for child in children:
            if child.name:
                if child.name.startswith("h"):
                    continue
                elif child.name == "a":
                    if child.text.lower() == "here":
                        output += f"at {child['href']}"
                    else:
                        output += f"{child.text} ({child['href']})"
                    continue
                elif child.name in ["ol", "ul"]:
                    for item in child.children:
                        if item.name == "li":
                            output += f"- {traverse([item]).strip()}\n"
                        else:
                            output += traverse([item])
                    continue
                elif child.name == "img":
                    output += f"[{child.attrs['alt']}]" if "alt" in child.attrs else "[Image]"
                    continue
            if isinstance(child, NavigableString):
                output += re.sub(r"([\t ])[\t ]*", r"\1", str(child))
            elif child.children:
                output += traverse(child.children)
            if child.name in ["p", "br"]:
                output += "\n"
        return "\n".join(line.strip() for line in output.strip().split("\n"))

    soup = BeautifulSoup(html, "html.parser")
    return traverse(soup.children).strip()


class EmailPreviewContext(dict):
    """
    A dict class to keep track of which variables were actually used by the template.
    """

    def __init__(self, *args, **kwargs):
        self._called = {}
        super().__init__(*args, **kwargs)

    def __getitem__(self, k):
        try:
            preview = super().__getitem__(k)
        except KeyError:
            preview = None

        if preview is None:
            preview = "{{" + k + "}}"

        self._called[k] = preview
        return preview

    def __contains__(self, k):
        return True

    def get_used_variables(self):
        return self._called
