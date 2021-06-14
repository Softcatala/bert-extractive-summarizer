cd /opt/service
python3 init.py
gunicorn --workers=2 --threads=2 server:app -b 0.0.0.0:8900
