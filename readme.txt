Start AI:
celery -A job_finder worker --loglevel=DEBUG
(venv)
sudo systemctl start redis
sudo systemctl status redis
(lokal)