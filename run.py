# run.py
from __init__ import create_app
from api_service import *


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
