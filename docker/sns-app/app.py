import logging
import boto3
from botocore.exceptions import ClientError
from flask import Flask, render_template, request
import os
import jmespath

app = Flask(__name__)
secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

logger = logging.getLogger(__name__)

# snippet-start:[python.example_code.sns.SnsWrapper]
class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""
    def __init__(self, sns_resource):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_resource = sns_resource
# snippet-end:[python.example_code.sns.SnsWrapper]

    @staticmethod
# snippet-start:[python.example_code.sns.Subscribe]
    def subscribe(topic, protocol, endpoint):
        """
        Subscribes an endpoint to the topic. Some endpoint types, such as email,
        must be confirmed before their subscriptions are active. When a subscription
        is not confirmed, its Amazon Resource Number (ARN) is set to
        'PendingConfirmation'.
        :param topic: The topic to subscribe to.
        :param protocol: The protocol of the endpoint, such as 'sms' or 'email'.
        :param endpoint: The endpoint that receives messages, such as a phone number
                         (in E.164 format) for SMS messages, or an email address for
                         email messages.
        :return: The newly added subscription.
        """
        try:
            subscription = topic.subscribe(
                Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
            logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic.arn)
        except ClientError:
            logger.exception(
                "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic.arn)
            raise
        else:
            return subscription
# snippet-end:[python.example_code.sns.Subscribe]

def usage_demo(email_address):
    app.logger.info('-'*88)
    app.logger.info("Welcome to the Amazon SNS demo!")
    app.logger.info('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    sns_wrapper = SnsWrapper(boto3.resource('sns'))
    sns = boto3.resource('sns')
    
    sns_client = boto3.client('sns')
    topic_name = os.environ.get('SNS_TOPIC_NAME')
    if topic_name == '':
        app.logger.info("ERROR: SNS_TOPIC_NAME env variable is not defined")
    response = sns_client.list_topics()
    list_of_topics = jmespath.search('Topics[].TopicArn', response)
    for topic_arn in list_of_topics:
        if topic_name in topic_arn:
            topic_arn = topic_arn
    app.logger.info(topic_arn)

    topic = sns.Topic(arn=topic_arn)

    app.logger.info(f"Subscribing {email_address} to {topic_name}.")
    sns_wrapper.subscribe(topic, 'email', email_address)

    app.logger.info('-'*88)
    app.logger.info("Succesfully subscribed", email_address, "to", topic_name)
    app.logger.info('-'*88)    

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email_address = request.form['email-address']

        while not email_address:
            # flash('email-address is required!')
            app.logger.info('email-address is required!')

        else:
            # email_var = ({'email-address': email_address})
            app.logger.info('-'*88)
            app.logger.info(email_address)
            app.logger.info('-'*88)
            usage_demo(email_address)
            return render_template('success.html')
        
    return render_template('index.html')

