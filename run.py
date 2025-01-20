import csv

from src.process_bucket import list_bucket, main
from flask import Flask
import logging

logging.basicConfig(
    level=logging.INFO,  # Set logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = Flask(__name__)

@app.route('/')
def index():
    return 'ok'
@app.route('/run',)
def run_etl():
    try:
        main()
        return 'OK'
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

