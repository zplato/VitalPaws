import random
from flask import Flask
app = Flask(__name__)

@app.route('/')
def process_data():
    respirations = str(random.randint(10, 50))
    return "Respiratory Rate: {0}".format(respirations)

if __name__ == '__main__':
    app.run()
