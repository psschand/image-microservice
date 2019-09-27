import os, subprocess
from app import app

env = os.environ['FLASK_ENV']

if __name__ == '__main__':
    if env == 'dev':
        app.run(host='0.0.0.0', debug=True)
    else:
        subprocess.run(["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi"])