from flask import Flask, jsonify, request

from squid import get_latest_table, map_table


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    table = get_latest_table()
    timing_map = map_table(table)

    try:
        requested_models = request.json["models"]
        print(requested_models)

        if requested_models:
            filtered_map = {}
            for model, data in timing_map.items():
                if model in requested_models:
                    filtered_map[model] = data
            timing_map = filtered_map
    except:
        pass

    return jsonify(timing_map)


if __name__ == '__main__':
    app.run()
