
import pytest
import requests
import getpass
import jwt
import datetime

from cogniceptshell.configuration import Configuration
from tests.functional.test_config import check_file_for_value

class SuccessLoginResponse(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        payload = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, 'secret')
        return {"access_token": payload.decode("utf-8") }

class NotFoundLoginResponse(object):
    def __init__(self):
        self.status_code = 404

class FailedLoginResponse(object):
    def __init__(self):
        self.status_code = 401   

def mock_login_api(*args, **kwargs):
    if(args[0] == "https://test.cognicept.systems/api/v1/user/login"):
        if(kwargs["json"]["username"] == "mock@cognicept.systems" and kwargs["json"]["password"]== "correct_password"):
            return SuccessLoginResponse()
        else:
            return NotFoundLoginResponse()
    else:
        return NotFoundMockResponse()

def setup_correct_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COGNICEPT_API_URI=https://test.cognicept.systems/api/v1/\nTEST_VARIABLE2=second_value")

def setup_expired_config(tmpdir):
    p = tmpdir.join("runtime.env")
    payload = jwt.encode({'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=30)}, 'secret')
    p.write("COGNICEPT_API_URI=https://test.cognicept.systems/api/v1/\nCOGNICEPT_JWT=" + payload.decode("utf-8") )


def setup_config_with_token(tmpdir):
    p = tmpdir.join("runtime.env")
    payload = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, 'secret')
    p.write("COGNICEPT_API_URI=https://test.cognicept.systems/api/v1/\nCOGNICEPT_JWT=" + payload.decode("utf-8") )


def setup_wrong_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COGNICEPT_API_URI=https://wrongaddress.com/\nTEST_VARIABLE2=second_value")

def test_wrong_uri(tmpdir, capsys, monkeypatch):
    # setup wrong API URI
    setup_wrong_file(tmpdir)

    monkeypatch.setattr(requests, "post", mock_login_api)
    monkeypatch.setattr(getpass, "getpass", lambda: "correct_password")
    monkeypatch.setattr('builtins.input', lambda prompt: "mock@cognicept.systems" if prompt == "Username: " else "")
    
    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")
    try: 
        local_cfg.cognicept_login()
        pytest.fail("Wrong uri did not give an exception", pytrace=True)
    except:
        pass


def test_correct_login(tmpdir, capsys, monkeypatch):
    monkeypatch.setattr(requests, "post", mock_login_api)
    monkeypatch.setattr(getpass, "getpass", lambda: "correct_password")
    monkeypatch.setattr('builtins.input', lambda prompt: "mock@cognicept.systems" if prompt == "Username: " else "")    
    
    # setup API URI
    setup_correct_file(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")
    try:
        result = local_cfg.cognicept_login()
    except:
        pytest.fail("Login gave exception", pytrace=True)

    assert(result == True)
    # check if token was stored
    check_file_for_value(tmpdir, capsys, "COGNICEPT_JWT", 1)

    # check if username needs to be entered again
    monkeypatch.setattr('builtins.input', lambda prompt: pytest.fail("Username needs to be re-entered after succesful login", pytrace=True))
    token = local_cfg.get_cognicept_jwt()
    assert len(token) > 0
    

def test_wrong_login(tmpdir, monkeypatch):
    monkeypatch.setattr(requests, "post", mock_login_api)

    # give wrong password
    monkeypatch.setattr(getpass, "getpass", lambda: "wrong_password")
    monkeypatch.setattr('builtins.input', lambda prompt: "mock@cognicept.systems" if prompt == "Username: " else "")    
    
    # setup API URI
    setup_correct_file(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")
    try:
        result = local_cfg.cognicept_login()
        assert(result == False)
    except:
        pytest.fail("Wrong login should not give exception", pytrace=True)

def test_expired_token(tmpdir, capsys, monkeypatch):
    monkeypatch.setattr(requests, "post", mock_login_api)
    monkeypatch.setattr(getpass, "getpass", lambda: "correct_password")
    monkeypatch.setattr('builtins.input', lambda prompt: "mock@cognicept.systems" if prompt == "Username: " else "")    
    
    # setup API URI
    setup_expired_config(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    monkeypatch.setattr(getpass, "getpass", lambda: "wrong_password")
    token = local_cfg.get_cognicept_jwt()
    assert len(token) == 0

    monkeypatch.setattr(getpass, "getpass", lambda: "correct_password")
    token = local_cfg.get_cognicept_jwt()
    assert len(token) > 0

def test_correct_token(tmpdir, capsys, monkeypatch):
    monkeypatch.setattr(requests, "post", mock_login_api)

    # make sure we don't need to reenter password
    monkeypatch.setattr('builtins.input', lambda prompt: pytest.fail("Username needs to be re-entered after succesful login", pytrace=True))  
    
    # setup API URI
    setup_config_with_token(tmpdir)

    local_cfg = Configuration()
    local_cfg.load_config(str(tmpdir) + "/")

    monkeypatch.setattr(getpass, "getpass", lambda: "correct_password")
    token = local_cfg.get_cognicept_jwt()
    assert len(token) > 0