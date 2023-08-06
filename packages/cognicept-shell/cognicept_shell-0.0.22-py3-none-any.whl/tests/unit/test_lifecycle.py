
import pytest
import re
import requests
import jwt
import datetime
import os

from cogniceptshell.configuration import Configuration
from cogniceptshell.agent_life_cycle import AgentLifeCycle


class SuccessEcrCredentials(object):
    def __init__(self):
        self.status_code = 200
    def json(self):
        return {"AccessKeyId": os.getenv('AWS_ACCESS_KEY_ID',""), "SecretAccessKey": os.getenv('AWS_SECRET_ACCESS_KEY', ""), "SessionToken": "" }

class NotFoundLoginResponse(object):
    def __init__(self):
        self.status_code = 404

def mock_ecr_endpoint(*args, **kwargs):
    if(args[0] == "https://test.cognicept.systems/api/v1/aws/assume_role/ecr"):
        return SuccessEcrCredentials()
    else:
        return NotFoundMockResponse()

def setup_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2")

def setup_with_orbitty(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2\nCOG_ORBITTY_ENABLED=True\nCOG_ORBITTY_IMAGE=412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/orbitty:latest")

def setup_wrong_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1")

def setup_test_docker_file(tmpdir):
    p = tmpdir.join("runtime.env")
    payload = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, 'secret')
    p.write("COG_AGENT_CONTAINERS=test\nCOG_AGENT_IMAGES=ubuntu:latest\nCOGNICEPT_API_URI=https://test.cognicept.systems/api/v1/\nCOGNICEPT_JWT=" + payload.decode("utf-8") )

def setup_wrong_api(tmpdir):
    p = tmpdir.join("runtime.env")
    payload = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, 'secret')
    p.write("COG_AGENT_CONTAINERS=test\nCOG_AGENT_IMAGES=ubuntu:latest\nCOGNICEPT_API_URI=https://wrongaddress.com/\nCOGNICEPT_JWT=" + payload.decode("utf-8") )


def setup_logs(tmpdir):

    expected_location = ".cognicept/agent/logs/directory"
    logs_dir = tmpdir.mkdir("agent").mkdir("logs")
    p = logs_dir.join("latest_log_loc.txt")
    p.write(expected_location + "\n")
    latest_log_dir = logs_dir.mkdir("directory")
    p2 = latest_log_dir.join("logDataStatus.json")
    p2.write('{"agent_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","compounding":"Null","create_ticket":true,"description":"Null","event_id":"Null","level":"Heartbeat","message":"Offline","module":"Status","property_id":"64dd2881-7010-4d9b-803e-42ea9439bf17","resolution":"Null","robot_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","source":"Null","telemetry":{},"timestamp":"2020-06-26T09:33:47.995496"}')

    p3 = latest_log_dir.join("logData1.json")
    p3.write('{"agent_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","compounding":false,"create_ticket":false,"description":"Null","event_id":"2a9e5abc-0412-4840-badc-d83094ddc0c6","level":"2","message":"Setting pose (10.986000): 9.700 9.600 -0.000","module":"Localization","property_id":"64dd2881-7010-4d9b-803e-42ea9439bf17","resolution":"Null","robot_id":"d1d26af0-27f0-4e45-8c6c-3e6d6e1736b7","source":"amcl","telemetry":{"nav_pose":{"orientation":{"w":0.99999148220339307,"x":0,"y":0,"z":-0.0041274108907466923},"position":{"x":0.02080195682017939,"y":0.024943113508386214,"z":0}},"odom_pose":{"orientation":{"w":0.99999999991375599,"x":0,"y":0,"z":-1.3133466028590658e-05},"position":{"x":7.9073011611115254e-06,"y":-1.4214209401935302e-10,"z":0}}},"timestamp":"2020-06-26T07:37:25.506519"}')

def test_init(tmpdir):
    # setup container/image config
    setup_file(tmpdir)


    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    assert(len(agent_lifecycle._docker_container_names) == 2)
    assert(len(agent_lifecycle._docker_images) == 2)
    assert(agent_lifecycle._docker_images[agent_lifecycle._docker_container_names[0]] == "image1")
    assert(agent_lifecycle._docker_images[agent_lifecycle._docker_container_names[1]] == "image2")

def test_orbitty_init(tmpdir):
    # setup container/image config
    setup_with_orbitty(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    assert(len(agent_lifecycle._docker_container_names) == 2)
    assert(len(agent_lifecycle._docker_images) == 3)


def test_incorrect_init(tmpdir):

    # setup container/image config
    setup_wrong_file(tmpdir)


    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    assert(len(agent_lifecycle._docker_container_names) == 4)
    assert(len(agent_lifecycle._docker_images) == 5)

def test_latest_log_loc(tmpdir):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_logs(tmpdir)

    agent_lifecycle = AgentLifeCycle()
    returned_location = agent_lifecycle.get_latest_log_loc(args)

    assert(returned_location == "agent/logs/directory")

def test_get_last_event(tmpdir, capsys):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_logs(tmpdir)

    agent_lifecycle = AgentLifeCycle()

    capsys.readouterr().out
    agent_lifecycle.get_last_event(args)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"\b2020-06-26T07:37:25.506519\b", output, re.MULTILINE)
    # check if file was found and printed 
    assert len(matches) == 1

def test_parsing_ok_ria_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: ERROR
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: ERROR
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: ERROR
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK"""
    capsys.readouterr().out
    agent_lifecycle.parseRemoteInterventionAgentLogs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ONLINE", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_not_init_ria_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.169204677]: WEBSOCKET:: STATUS:: INIT"""
    capsys.readouterr().out
    agent_lifecycle.parseRemoteInterventionAgentLogs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"NOT INITIALIZED", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_agent_error_ria_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: ERROR"""
    capsys.readouterr().out
    agent_lifecycle.parseRemoteInterventionAgentLogs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ERROR", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_websocket_error_ria_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: ERROR
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK"""
    capsys.readouterr().out
    agent_lifecycle.parseRemoteInterventionAgentLogs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ERROR", output, re.MULTILINE)
    assert len(matches) == 1

def test_parsing_webrtc_error_ria_logs(capsys):
    agent_lifecycle = AgentLifeCycle()

    log = """[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: OK
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK
[ INFO] [1594729019.086950527]: WEBRTC:: STATUS:: ERROR
[ INFO] [1594729019.166115169]: WEBSOCKET:: STATUS:: OK
[ INFO] [1594729019.169204677]: AGENT:: STATUS:: OK"""
    capsys.readouterr().out
    agent_lifecycle.parseRemoteInterventionAgentLogs(log)
    output = str(capsys.readouterr().out)
    matches = re.findall(r"ERROR", output, re.MULTILINE)
    assert len(matches) == 1

def test_run(tmpdir, capsys):
    args = type('', (), {})()
    args.path = str(tmpdir) + "/"

    setup_test_docker_file(tmpdir)
    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)

    args.config = local_cfg

    # run container
    result = agent_lifecycle.restart(args)
    assert result == True

    # check status
    capsys.readouterr().out
    agent_lifecycle.get_status(args)
    output = str(capsys.readouterr().out)
    matches1 = re.findall(r"ONLINE", output, re.MULTILINE)
    assert len(matches1) == 1

    result = agent_lifecycle.remove_agents(args)
    assert result == True

    # check if offline
    capsys.readouterr().out
    agent_lifecycle.get_status(args)
    output = str(capsys.readouterr().out)
    matches2 = re.findall(r"CONTAINER NOT FOUND", output, re.MULTILINE)
    assert len(matches2) == 1


def test_correct_ecr_credentials(tmpdir, monkeypatch):

    try:  
        os.environ["AWS_ACCESS_KEY_ID"]
        os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError: 
        pytest.skip("AWS credentials are not defined.")

    monkeypatch.setattr(requests, "get", mock_ecr_endpoint)

    # setup API URI
    setup_test_docker_file(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    args = type('', (), {})()
    args.path = str(tmpdir) + "/"
    args.reset = False
    args.config = local_cfg

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)
    result = agent_lifecycle.update(args)

    assert(result == True)

def test_ecr_not_found_endpoint(tmpdir, monkeypatch):

    monkeypatch.setattr(requests, "get", mock_ecr_endpoint)

    # setup API URI
    setup_wrong_api(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    args = type('', (), {})()
    args.path = str(tmpdir) + "/"
    args.reset = False
    args.config = local_cfg

    agent_lifecycle = AgentLifeCycle()
    agent_lifecycle.configure_containers(local_cfg)
    result = agent_lifecycle.update(args)

    assert(result == False)