flask --app /root/sns-app/app.py run --host=0.0.0.0 > /root/sns-app/log.txt 
# 2>&1 &
# gunicorn --bind 0.0.0.0:5000 app:app --daemon --log-file=log.txt

# sleep infinity