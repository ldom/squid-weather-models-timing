from flask import Flask, jsonify, request
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




def build_model_form(models):

    model_list = "\n".join([f"<input type='checkbox' name='{normalized_model_name(m)}'></input><label for='{normalized_model_name(m)}'>{m}</label><br />" for m in models])

    form = f"<form id='models' action'/html' method='POST' enctype='application/x-www-form-urlencoded'>{model_list}" \
           f"<button type='submit' form='models' value='view' formaction='/html'>View/Voir</button>" \
           f"</form>"

    return f"""
    <!doctype html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Models Availability</title>
      <style>
      body {{
        font-family: "arial";
        font-size: small;
      }}
      </style>
    </head>
    <body>
        <div>Select the models your wish to use - Sélectionnez les modèles que vous voulez utiliser :</div>
        {form}    
    </body>
    </html>
        """


def build_html(recap_table):
    header = ""
    table_body = ""
    for i, row in enumerate(recap_table):
        if i == 0:
            header = "<tr><th>" + "</th><th>".join(row) + "</th></tr>"
        else:
            table_body += "<tr><td class='model'>" + "</td><td>".join(row) + "</td></tr>"

    html_table = f"<table><thead>{header}</thead><tbody>{table_body}</tbody></table>"

    return f"""
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Models Availability</title>
  <style>
  th {{
    background-color: #333;
    color: #eee;
    padding: 3px;
  }}
  body {{
    font-family: "arial";
    text-align: center;
  }}
  table {{
    display: table;
    border: 1px solid #333;
    border-spacing: 0;
    -webkit-border-horizontal-spacing: 0;
    -webkit-border-vertical-spacing: 0;
  }}
  th, td {{
    padding: 10px;
  }}
  td {{ 
    border-top: 1px solid #666;
    border-right: 1px dotted #666;
  }}
  td.model {{ 
    text-align: right;
  }}
  tr:nth-child(even) {{background: #CCC}}
  tr:nth-child(odd) {{background: #FFF}}
  </style>
</head>
<body>
    {html_table}    
</body>
</html>
    """


@app.route('/', methods=['POST', 'GET'])
def index():
    timing_map, recap_table = get_data()

    html_result = build_model_form(timing_map.keys())
    return html_result

@app.route('/json', methods=['POST', 'GET'])
def json():
    timing_map, recap_table = get_data()
    return jsonify({"timing_details": timing_map, "recap_table": recap_table})

@app.route('/html', methods=['POST', 'GET'])
def html():
    timing_map, recap_table = get_data()

    html_result = build_html(recap_table)
    return html_result


if __name__ == '__main__':
    app.run()
