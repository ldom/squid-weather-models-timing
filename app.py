from flask import Flask, jsonify, request, render_template
import re

from recap import get_recap_table
from squid import get_latest_table, map_table


app = Flask(__name__)


@app.route('/models')
def models():
    table = get_latest_table()
    timing_map = map_table(table)
    model_names = list(timing_map.keys())
    return jsonify(model_names)


def requested_models(request, models_map):
    if request.json and request.json.get("models"):
        return request.json["models"]

    if request.form:
        return [models_map[k] for k in request.form.keys()]

    return []


def normalized_model_name(model_name):
    result = model_name.lower()
    result = re.sub(r'[\s]', '-', result)
    result = re.sub(r'[é]', 'e', result)
    result = re.sub(r'[^a-z-\d]', '', result)
    return result


def get_data():
    table = get_latest_table()
    timing_map = map_table(table)

    models_map = {normalized_model_name(m): m for m in timing_map.keys()}

    models = requested_models(request, models_map)
    if models:
        filtered_map = {}
        for model, data in timing_map.items():
            if model in models:
                filtered_map[model] = data
        timing_map = filtered_map

    recap_table = get_recap_table(timing_map)

    return timing_map, recap_table


def model_checkboxes(models):
    return [f"<div class='item'><input type='checkbox' name='{normalized_model_name(m)}' " \
            f"id='{normalized_model_name(m)}'></input>"
            f"<label for='{normalized_model_name(m)}'>{m}</label></div>"
            for m in models]


def build_flex_form(checkboxes):
    result = '<div class="container">'
    result += "\n".join(checkboxes)
    result += "</div>"
    return result


def build_html_table(recap_table):
    header = ""
    table_body = ""
    for i, row in enumerate(recap_table):
        if i == 0:
            header = "<tr><th>" + "</th><th>".join(row) + "</th></tr>"
        else:
            table_body += "<tr><td class='model'>" + "</td><td>".join(row) + "</td></tr>"

    return f"<table><thead>{header}</thead><tbody>{table_body}</tbody></table>"


@app.route('/', methods=['GET'])
def index():
    timing_map, recap_table = get_data()
    checkboxes = model_checkboxes(timing_map.keys())
    model_form = build_flex_form(checkboxes)

    return render_template('index.html', model_form=model_form)


@app.route('/json', methods=['POST', 'GET'])
def json():
    timing_map, recap_table = get_data()
    return jsonify({"timing_details": timing_map, "recap_table": recap_table})


@app.route('/', methods=['POST'])
def html():
    timing_map, recap_table = get_data()
    table = build_html_table(recap_table)
    return render_template('result.html', html_table=table)


if __name__ == '__main__':
    app.run()
