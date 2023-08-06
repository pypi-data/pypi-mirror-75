import boto3
import os
from past.builtins import basestring
from datacoco_cloud import UNIT_TEST_KEY


class SESInteraction:
    """
    wrapper on boto3 ses
    """

    def __init__(
        self,
        to,
        subject,
        sender,
        aws_access_key,
        aws_secret_key,
        aws_region="us-east-1",
    ):
        """
        :param to:
        :param subject:
        :return:
        """
        self.connection = None
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None
        self._format = "html"
        self.def_sender = sender

        is_test = os.environ.get(UNIT_TEST_KEY, False)

        if not is_test:
            self.connection = boto3.client(
                "ses",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region,
            )

    def html(self, html):
        """
        set's email html message property
        :param html:
        :return:
        """
        self._html = html

    def text(self, text):
        """
        set's email text message property
        :param text:
        :return:
        """
        self._text = text

    def send(self, from_addr=None):
        """
        sends email
        :param from_addr:
        :return:
        """
        body = self._html

        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = self.def_sender
        if not self._html and not self._text:
            raise Exception("You must provide a text or html body.")
        if not self._html:
            self._format = "text"
            body = self._text

        return self.connection.send_email(
            Source=from_addr,
            Destination={"ToAddresses": self.to},
            Message={
                "Subject": {"Data": self.subject},
                "Body": {"Text": {"Data": body}, "Html": {"Data": body}},
            },
        )
