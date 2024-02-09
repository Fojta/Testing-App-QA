from flask import Flask, render_template, redirect, jsonify
import UpdateBRE
import Authorizations
import yaml

app = Flask(__name__)


class Server:
    member_id_external = "M1000000000"
    member_id_internal = ""

    last_authorization_id = ""
    last_authorization_li_id = ""
    last_appeal_id = ""

    services_connector = ""

    def __init__(self, name, hostname, local=False, options=None):
        self.name = name
        self.hostname = hostname
        self.is_localhost = local
        self.options = options or {}

    def update_last_authorization_ids(self, auth_json):
        self.last_authorization_id = auth_json["authorizationId"]
        self.last_authorization_li_id = auth_json["lineItems"][0]["id"]
        self.last_appeal_id = ""


def load_servers_from_yaml(file_path='servers.yml'):
    with open(file_path, 'r') as file:
        file_servers = yaml.safe_load(file)

        load = [Server(
            server['name'],
            server['hostname'],
            server.get('is_localhost', False),
            server.get('options', {})
        ) for server in file_servers]

    return load


servers = [
    Server("localhost", "localhost", True,
           {"bre": True, "authorization": True, "appeals": True, "links": True, "text": True}),
    Server("anyhost", "random", False,
           {"bre": True, "authorization": True, "appeals": True, "links": True, "text": True})
    ]

loaded_servers = load_servers_from_yaml()
servers += loaded_servers


def get_server(name):
    for server in servers:
        if server.name == name:
            return server

    raise Exception("server not found in configuration")


@app.route("/")
def index():
    return render_template("index.html", servers=servers)


@app.route("/update_bre/<string:server_name>", methods=['POST'])
def update_bre(server_name):
    # print("updating bre")
    # server = get_server(server_name)
    # if not server.services_connector:
    #     server.services_connector = UpdateBRE.UpdateBRE(server.hostname)
    # if server.is_localhost:
    #     server.services_connector.update_bre()
    # else:
    #     redirect("{hostname}/update_bre/localhost".format(server.hostname))
    return "BRE updated"


@app.route("/create_authorization_sp/<server_name>", methods=['POST'])
def create_authorization_sp(server_name):
    print("creating authorization")
    server = get_server(server_name)
    response = Authorizations.create_sp_authorization(server.hostname)
    if response.status_code != 200:
        return jsonify({"message": "Failed to create SP authorization"}), response.status_code, response.text
    else:
        server.update_last_authorization_ids(response.json())
        return jsonify({"message": "SP authorization created"})


@app.route("/create_authorization_ip/<server_name>", methods=['POST'])
def create_authorization_ip(server_name):
    print("creating authorization")
    server = get_server(server_name)
    response = Authorizations.create_ip_authorization(server.hostname)
    print(response.status_code)
    if response.status_code != 200:
        return jsonify({"message": "Failed to create IP authorization"}), response.status_code, response.text
    else:
        server.update_last_authorization_ids(response.json())
        return jsonify({"message": "IP authorization created"})


@app.route("/create_authorization_rx/<server_name>", methods=['POST'])
def create_authorization_rx(server_name):
    print("creating authorization")
    server = get_server(server_name)
    response = Authorizations.create_rx_authorization(server.hostname)
    if response.status_code != 200:
        return jsonify({"message": "Failed to create RX authorization"}), response.status_code, response.text
    else:
        server.update_last_authorization_ids(response.json()["createAuthorizationResponse"])
        return jsonify({"message": "RX authorization created"})


@app.route("/determinne_line_item/<server_name>", methods=['POST'])
def determin_li(server_name):
    print('determining line item for last authorization')
    server = get_server(server_name)
    response = Authorizations.determine_line_item(server)
    if response.status_code != 200:
        return jsonify({"message": "Failed to determine last authorization"}), response.status_code, response.text
    else:
        return jsonify({"message": "Last authorization determinate"})


@app.route("/create_appeal/<server_name>", methods=['POST'])
def create_appeal(server_name):
    print("creating new appeal")
    server = get_server(server_name)
    response = Authorizations.create_appeal(server)
    if response.status_code != 200:
        return jsonify({"message": "Failed to create appeal"}), response.status_code, response.text
    else:
        server.last_appeal_id = response.json()["appealId"]
        return jsonify({"message": "Appeal has been created"})


@app.route("/add_outcome/<server_name>", methods=['POST'])
def appeal_add_outcome(server_name):
    print("adding outcome to appeal")
    server = get_server(server_name)
    response = Authorizations.add_outcome(server)
    print(response)
    if response.status_code != 204:
        return jsonify({"message": "Failed to create outcome"}), response.status_code, response.text
    else:
        return jsonify({"message": "Outcome created"})


@app.route("/add_advisor_review/<server_name>", methods=['POST'])
def add_advisor_review(server_name):
    print("adding advisor review to appeal")
    server = get_server(server_name)
    response = Authorizations.add_advisor_review(server)
    if response.status_code != 200:
        return jsonify({"message": "Failed to create advisor review"}), response.status_code, response.text
    else:
        return jsonify({"message": "Advisor Review Created"})


@app.route("/add_clinical_review/<server_name>", methods=['POST'])
def add_clinical_review(server_name):
    print("adding clinical review to appeal")
    server = get_server(server_name)
    response = Authorizations.add_clinical_review(server)
    if response.status_code != 200:
        return jsonify({"message": "Failed to create clinical review"}), response.status_code, response.text
    else:
        return jsonify({"message": "Clinical Review Created"})


@app.route("/tc_client/<server_name>", methods=['GET'])
def tc_client(server_name):
    print("redirecting to tc_client")
    server = get_server(server_name)

    if not server.member_id_internal:
        member_info = Authorizations.get_member_info(server)
        server.member_id_internal = member_info["id"]

    return redirect("http://" + server.hostname + ":8085/trucare-client/member/" + server.member_id_internal
                    + "/um/authorization")


app.run("localhost", 5050, debug=True)
