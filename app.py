"""Flask App Project."""

from flask import Flask, jsonify

from squid import get_latest_table


app = Flask(__name__)


@app.route('/')
def index():
    print(get_latest_table())

    json_data = {'Hello': 'World!'}
    return jsonify(json_data)


if __name__ == '__main__':
    app.run()
