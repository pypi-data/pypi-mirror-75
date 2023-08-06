import boto3
from botocore.exceptions import ClientError
import json
import os
from datacoco_cloud import UNIT_TEST_KEY


class SQSInteraction:
    def __init__(
        self,
        aws_access_key,
        aws_secret_key,
        queue_name,
        region="us-east-1",
        create_queue=False,
    ):
        self.sqs_queue_url = None
        self.sqs_queue_arn = None
        self.queue_name = queue_name
        self.sqs = None
        is_test = os.environ.get(UNIT_TEST_KEY, False)

        if not is_test:
            self.sqs = boto3.client(
                "sqs",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region,
            )

            if create_queue:
                self.create_queue(self.queue_name)

            try:
                self.init_sqs()
            except Exception as e:
                print(e.message)
                print("Queue does not exist, please create the queue first.")

    def init_sqs(self):
        print("---------------\nSQS starting")

        try:
            query_result = self.sqs.get_queue_url(QueueName=self.queue_name)
            self.sqs_queue_url = query_result["QueueUrl"]
        except KeyError:
            raise ValueError("SQS returned a result without a QueueUrl in it")
        except ClientError:
            raise NoSuchQueueException(
                "%s is not available in this region with these credentials.",
                self.queue_name,
            )

        print(f"Queue exists: {self.sqs_queue_url is not None}")  # nosec

        if not self.sqs_queue_url:
            raise ValueError("SQS returned a result without a QueueUrl in it")

        queue_attribs = self.get_queue_attribs()

        self.sqs_queue_arn = queue_attribs["QueueArn"]
        print(f"Queue ARN: {self.sqs_queue_arn}")

        if "Policy" in queue_attribs:
            policy = json.loads(queue_attribs["Policy"])
            print(f"Policy found: {policy}")
        else:
            print("No policy")

    def create_queue(self, queue_name):
        print(f"Creating queue: {queue_name}")
        response = self.sqs.create_queue(QueueName=queue_name)
        self.sqs_queue_url = response["QueueUrl"]

    def get_queue_attribs(self):
        return self.sqs.get_queue_attributes(
            QueueUrl=self.sqs_queue_url, AttributeNames=["All"]
        )["Attributes"]

    def set_policy(self, policy):
        self.sqs.set_queue_attributes(
            QueueUrl=self.sqs_queue_url,
            Attributes={"Policy": json.dumps(policy)},
        )
        print(f"Policy set: {policy}")

    def get_queue_url(self):
        return self.sqs.get_queue_url(QueueName=self.queue_name)

    def get_queue_count(self):
        response = self.sqs.get_queue_attributes(
            QueueUrl=self.sqs_queue_url,
            AttributeNames=["ApproximateNumberOfMessages"],
        )
        return response["Attributes"]["ApproximateNumberOfMessages"]

    def create_subscriber(self):
        return Subscriber(self.sqs, self.sqs_queue_url)

    def send_message(self, message_body, delay_seconds=10):
        self.sqs.send_message(
            QueueUrl=self.sqs_queue_url,
            DelaySeconds=delay_seconds,
            MessageBody=message_body,
        )


class Subscriber(object):
    def __init__(self, sqs, sqs_queue_url):
        self.sqs = sqs
        self.sqs_queue_url = sqs_queue_url

    def get_messages(self, num_messages=1):
        return self.sqs.receive_message(
            QueueUrl=self.sqs_queue_url, MaxNumberOfMessages=num_messages
        )

    def delete_message(self, message):
        try:
            receipt_handle = message["ReceiptHandle"]
            print(f"Receipt handle: {receipt_handle}")
        except Exception as e:
            print("Issue retrieving message handle:")
            print(e.message)
            return

        self.sqs.delete_message(
            QueueUrl=self.sqs_queue_url, ReceiptHandle=receipt_handle
        )


class NoSuchQueueException(Exception):
    pass
