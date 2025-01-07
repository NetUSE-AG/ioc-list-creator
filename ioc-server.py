import os
import csv
import argparse

from ioc import Config
from flask import Flask, jsonify, g, request

app = Flask(__name__)
app.config.config_file = os.environ.get("CONFIG_FILE")

@app.route('/lookup', methods=["GET"])
def lookup():
    client_token = request.args.get("token")
    if not client_token:
        return jsonify({'status': 'parameter error'}), 403

    if client_token != app.config.token:
        return jsonify({'status': 'invalid token'}), 403
    
    lookup_value= request.args.get("value")
    if not lookup_value:
        return jsonify({'status': 'parameter error'}), 403

    return jsonify({'status':'success', 'ioc':app.config.values[lookup_value] if lookup_value in app.config.values else False}), 200 


@app.route('/reload', methods=['POST'])
def reload():
    client_token = request.args.get("token")
    if not client_token:
        return jsonify({'status': 'parameter error'}), 403

    if client_token != app.config.token:
        return jsonify({'status': 'invalid token'}), 403

    setup_lookup_dictionaries()
    return jsonify({'status':'success'}), 200


def setup():
    config = Config(app.config.config_file)
    app.config.token = config.token
    file_names = [config.output_dir/config.output_ip_filename,
                    config.output_dir/config.output_domain_filename,
                    config.output_dir/config.output_url_filename
                ]
    if 'values' not in app.config:
        app.config.values = {}

    for name in file_names:
        csv_file = csv.reader(open(name), delimiter=";")
        csv_file.__next__()
        for row in csv_file:
            app.config.values[row[0]]=row[1]


with app.app_context():
    setup()
