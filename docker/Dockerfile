FROM python
WORKDIR /root/sns-app
COPY sns-app/. /root/sns-app
EXPOSE 5000
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
RUN unzip /tmp/awscliv2.zip -d /tmp/
RUN sh /tmp/aws/install
RUN pip install Flask boto3 jmespath gunicorn
COPY entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["/bin/sh", "-c", "/usr/bin/entrypoint.sh"]
# CMD ["gunicorn", "--bind 0.0.0.0:5000", "app:app", "--daemon", "--log-file=log.txt"]
# CMD ["flask", "--app", "/root/sns-app/app.py", "run", "--host=0.0.0.0"]
# CMD [ "sleep", "infinity" ]