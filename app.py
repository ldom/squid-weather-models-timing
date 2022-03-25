from flask import Flask, jsonify, request

from recap import get_recap_table
from squid import get_latest_table, map_table


app = Flask(__name__)


@app.route('/models')
def models():
    table = get_latest_table()
    timing_map = map_table(table)
    model_names = list(timing_map.keys())
    return jsonify(model_names)


def get_data():
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

    recap_table = get_recap_table(timing_map)

    return timing_map, recap_table


def build_html(recap_table):
    header = ""
    table_body = ""
    for i, row in enumerate(recap_table):
        if i == 0:
            header = "<tr><th>" + "</th><th>".join(row) + "</th></tr>"
        else:
            table_body += "<tr><td>" + "</td><td>".join(row) + "</td></tr>"

    html_table = f"<table><thead>{header}</thead><tbody>{table_body}</tbody></table>"

    return f"""
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Models Availability</title>
</head>
<body>
    {html_table}    
</body>
</html>
    """


@app.route('/', methods=['POST', 'GET'])
def index():
    timing_map, recap_table = get_data()
    return jsonify({"timing_details": timing_map, "recap_table": recap_table})


@app.route('/html', methods=['POST', 'GET'])
def html():
    timing_map, recap_table = get_data()

    html_result = build_html(recap_table)
    return html_result


if __name__ == '__main__':
    app.run()
