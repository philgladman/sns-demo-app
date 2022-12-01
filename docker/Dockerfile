FROM python
WORKDIR /root/sns-app
COPY sns-app/. /root/sns-app
EXPOSE 5000
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
RUN unzip /tmp/awscliv2.zip -d /tmp/
RUN sh /tmp/aws/install
RUN pip install Flask boto3 jmespath gunicorn
# CMD ["gunicorn", "--bind 0.0.0.0:5000", "app:app", "--daemon", "--log-file=log.txt"]
# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
CMD [ "sleep", "infinity" ]