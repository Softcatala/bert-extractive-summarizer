cd /opt/service
python3 init.py
gunicorn --workers=1 --threads=1 server:app -b 0.0.0.0:8900
