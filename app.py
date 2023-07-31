from flask import Flask, jsonify

app = Flask(__name__)

# Sample data to be returned as JSON
sample_data = {
    "message": "Hello, this is a simple Flask API!",
    "data": [1, 2, 3, 4, 5]
}

@app.route('/')
def hello():
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(debug=True)
