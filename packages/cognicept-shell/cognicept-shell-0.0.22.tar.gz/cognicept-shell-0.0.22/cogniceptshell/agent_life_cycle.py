# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> AgentLifeCycle handles life cycle of Cognicept Agents

import docker
import boto3
import base64
import json
import os
import dateutil
from datetime import datetime
import re
import glob
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AgentLifeCycle:

    # default configuration of containers and images
    _docker_container_names = ["cgs_diagnostics_agent","remote_intervention_agent","cgs_diagnostics_ecs_api","cgs_diagnostics_streamer_api"]
    _docker_images = {}
    _docker_images["remote_intervention_agent"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/remote_intervention_agent:latest"
    _docker_images["cgs_diagnostics_agent"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_agent:latest"
    _docker_images["cgs_diagnostics_ecs_api"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_api:latest"
    _docker_images["cgs_diagnostics_streamer_api"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_api:latest"
    _docker_images["orbitty"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/orbitty:latest"
    
    def configure_containers(object, cfg):
        if("COG_AGENT_CONTAINERS" in cfg.config and "COG_AGENT_IMAGES" in cfg.config):
            container_names = cfg.config["COG_AGENT_CONTAINERS"].split(";")
            image_names = cfg.config["COG_AGENT_IMAGES"].split(";")
            if(len(image_names) == len(container_names)):
                object._docker_container_names = container_names
                object._docker_images = {}
                i = 0
                for container_name in container_names:
                    object._docker_images[container_name] = image_names[i]
                    i = i + 1
            else:
                print("`COG_AGENT_CONTAINERS` and `COG_AGENT_IMAGES` do not coincide. Using default.")

            if("COG_ORBITTY_ENABLED" in cfg.config and "COG_ORBITTY_IMAGE" in cfg.config):
                if(bool(cfg.config["COG_ORBITTY_ENABLED"])):
                    object._docker_images["orbitty"] = cfg.config["COG_ORBITTY_IMAGE"]
        else:
            print("Undefined `COG_AGENT_CONTAINERS` or `COG_AGENT_IMAGES`. Using default.")

    def get_latest_log_loc(object, args):
        # get latest log location
        latest_log_loc_file_path = os.path.expanduser(args.path+"agent/logs/latest_log_loc.txt")
        latest_log_loc = ""
        try:            
            with open(latest_log_loc_file_path) as txt_file:                
                latest_log_loc_temp = txt_file.readline()
                latest_log_loc_temp = latest_log_loc_temp[:-1]
                latest_log_loc = latest_log_loc_temp.replace("/$HOME/.cognicept/","")
                latest_log_loc = latest_log_loc.replace(".cognicept/","")
        except:
            cgs_agent_status = f"{bcolors.FAIL}UNKNOWN{bcolors.ENDC}"
        
        return latest_log_loc

    def get_status(object, args):
        client = docker.from_env()

        # check status of cgs_agent
        # get latest log location
        latest_log_loc = object.get_latest_log_loc(args)
        
        # read latest status and set for display
        file_path = os.path.expanduser(args.path+latest_log_loc+"/logDataStatus.json")        
        try:            
            with open(file_path) as json_file:                
                data = json.load(json_file)
                period_since_update = datetime.utcnow() - dateutil.parser.parse(data["timestamp"])
                if(period_since_update.seconds < 30 and period_since_update.seconds >= 0):
                    cgs_agent_status = bcolors.OKBLUE + data["message"].upper() + bcolors.ENDC
                else:
                    cgs_agent_status = f"{bcolors.WARNING}STALE{bcolors.ENDC}"

        except:
            cgs_agent_status = f"{bcolors.FAIL}ERROR{bcolors.ENDC}"


        for container_name in object._docker_container_names:
            print(container_name, end = ': ', flush=True)
            try:
                container = client.containers.get(container_name)
                if container.status != "running":
                    print(f"{bcolors.WARNING}OFFLINE{bcolors.ENDC}")
                else:
                    if(container_name == "cgs_agent"):
                        print(cgs_agent_status)
                    elif(container_name == "remote_intervention_agent"):
                        object.parseRemoteInterventionAgentLogs(container.logs(tail=50))
                    elif(container_name == "cgs_diagnostics_agent"):
                        print(cgs_agent_status)                        
                    else:
                        print(f"{bcolors.OKBLUE}ONLINE{bcolors.ENDC}")
            except docker.errors.NotFound:
                print(f"{bcolors.FAIL}CONTAINER NOT FOUND{bcolors.ENDC}")
    
    def get_last_event(object, args):
        
        # get latest log location
        latest_log_loc = object.get_latest_log_loc(args)
        
        # read and display latest log if any
        file_path = os.path.expanduser(args.path+latest_log_loc)        
        try:
            print(f"{bcolors.OKBLUE}Looking for the latest event log...{bcolors.ENDC}")
            # should read only latest logData#.json file and not logDataStatus.json
            list_of_log_files = [fn for fn in glob.glob(file_path + "/*.json") \
                                    if not os.path.basename(fn).endswith("logDataStatus.json")]
            latest_log_file = max(list_of_log_files, key=os.path.getctime)            
            
            with open(latest_log_file) as json_file:                
                data = json.load(json_file)
                print(f"{bcolors.OKGREEN}Latest Event Log:{bcolors.ENDC}")
                print(json.dumps(data, indent=4, sort_keys=True))                
        except:
            print(f"{bcolors.WARNING}No event logs present.{bcolors.ENDC}")

    def parseRemoteInterventionAgentLogs(object, logs):
        ## Parses logs to find status of remote intervention agent
        logs_lines = logs.splitlines()
        # parse logs to get current status
        ri_agent_status = {}
        ri_agent_status["AGENT"] = ""
        ri_agent_status["WEBRTC"] = ""
        ri_agent_status["WEBSOCKET"] = ""

        # find latest status of the each module (agent, webrtc, websocket)
        for line in reversed(logs_lines):
            for key,value in ri_agent_status.items():
                if(value != ""):
                    continue
                matches = re.search(rf'^.*{key}:: STATUS:: (?P<status>.*).*$', str(line))
                if(matches is not None):
                    ri_agent_status[key] = matches.groups(0)[0]
            if(ri_agent_status["AGENT"] != "" and ri_agent_status["WEBRTC"] != "" and ri_agent_status["WEBSOCKET"] != ""):
                continue
        
        output_text = f"{bcolors.OKBLUE}ONLINE{bcolors.ENDC}"
        for key,value in ri_agent_status.items():
            if(value == ""):
                #if not found, it was not yet initialized
                output_text = f"{bcolors.WARNING} NOT INITIALIZED {bcolors.ENDC}"
                break
            if(value != "OK"):
                output_text = f"{bcolors.WARNING} {key} {value} {bcolors.ENDC}"
                break
        print(output_text)

    def restart(object, args):
        print("Restarting agents")
        object.remove_agents(args)
        result = object.run(args)
        return result


    def remove_agents(object, args):   
        client = docker.from_env()
        print("STOP: ")
        for container_name in object._docker_container_names:
            print("   - " + container_name, end = ': ', flush=True)
            try:
                container = client.containers.get(container_name)
                container.stop(timeout=10)
                container.remove()
                print(f"{bcolors.OKBLUE}DONE{bcolors.ENDC}")
                return True
            except docker.errors.NotFound:
                print(f"{bcolors.WARNING}NOT FOUND{bcolors.ENDC}")                	
                return True
            except docker.errors.APIError:
                print(f"{bcolors.FAIL}ERROR{bcolors.ENDC}")
                return False
    
    def run(object, args):
        object._agent_run_options = {}
        object._agent_run_options["cgs_agent"] = {"command": "start_cognicept_agent.py","volumes":{args.config.config_path + "agent/logs/": {"bind": "/root/.cognicept/agent/logs", "mode":"rw"}},"network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_agent"] = {"command": "roslaunch rosrect-listener-agent listener-agent.launch" ,"volumes":{args.config.config_path + "agent/logs/": {"bind": "/root/.cognicept/agent/logs", "mode":"rw"}} ,"network_mode": "host"}        
        object._agent_run_options["ecs_server"] = {"command": "/ecs_api_server/ecs_endpoint.py","network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_ecs_api"] = {"command": "/ecs_api_server/ecs_endpoint.py" ,"network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_streamer_api"] = {"command": "/data_streamer/streamer_endpoint.py" ,"network_mode": "host"}
        object._agent_run_options["remote_intervention_agent"] = {"command": "rosrun remote_intervention_agent cognicept_agent_node" ,"network_mode": "host"}        
        object._agent_run_options["rosbridge"] = {"command": "roslaunch rosbridge_server rosbridge_websocket.launch" ,"network_mode": "host"}  
        object._agent_run_options["test"] = {"command": "bash"}
        client = docker.from_env()
        print("RUN: ")
        success_flag = True
        for container_name in object._docker_container_names:
            print("   - " + container_name, end = ': ', flush=True)
            try:
                options = object._agent_run_options[container_name]
                options["name"] = container_name
                options["detach"] = True
                options["environment"] = args.config.config
                options["restart_policy"] = {"Name":"unless-stopped"}
                options["tty"] = True
                command = options.pop("command")
                container = client.containers.run(object._docker_images[container_name], command, **options)
                print(f"{bcolors.OKBLUE}DONE{bcolors.ENDC}")
            except docker.errors.ContainerError:
                print(f"{bcolors.WARNING}ALREADY EXISTS{bcolors.ENDC} (run `cognicept update`)")
            except docker.errors.ImageNotFound:
                print(f"{bcolors.WARNING}IMAGE NOT FOUND{bcolors.ENDC} (run `cognicept update`)")
                success_flag = False
            except docker.errors.APIError:
                print(f"{bcolors.FAIL}DOCKER ERROR{bcolors.ENDC}")
                success_flag = False
        return success_flag
    
    def run_orbitty(object, args):
        os.system("xhost +local:root")
        client = docker.from_env()
        try:
            options = {}
            options["name"] = "orbitty"
            options["detach"] = False
            options["privileged"] = True
            options["volumes"] = {}
            options["volumes"][args.config.config_path] = {"bind": "/config", "mode":"rw"}
            options["volumes"]["/tmp/.X11-unix"] = {"bind": "/tmp/.X11-unix", "mode":"rw"}
            environment = args.config.config
            environment["QT_X11_NO_MITSHM"] = 1
            environment["DISPLAY"] = ":0"
            options["environment"] = args.config.config
            options["remove"] = True
            options["tty"] = True
            command = "roslaunch orbitty orbitty.launch"
            client.containers.run(object._docker_images["orbitty"], command, **options)
        except docker.errors.ContainerError:
            print(f"{bcolors.WARNING}ALREADY RUNNING{bcolors.ENDC}")
        except docker.errors.ImageNotFound:
            print(f"{bcolors.WARNING}IMAGE NOT FOUND{bcolors.ENDC} (run `cognicept update`)")
        except docker.errors.APIError:
            print(f"{bcolors.FAIL}DOCKER ERROR{bcolors.ENDC}")
        os.system("xhost -local:root")

    def update(object, args):
        
        if(args.reset):
            # reset credentials if requested
            args.config.cognicept_login()
        # retrieve jwt
        token = args.config.get_cognicept_jwt()

        headers = {"Authorization": "Bearer " + token}
        try:
            resp = requests.get( args.config.get_cognicept_api_uri() + "aws/assume_role/ecr", headers= headers, timeout = 5)
            
            if resp.status_code != 200:
                print(f'Cognicept REST API error: `{args.config.get_cognicept_api_uri()}` responded with {resp.status_code}')
                return False     
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return False
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return False
        except:
            print("Cognicept REST API error")
            return False


        ecr_client = boto3.client('ecr', region_name='ap-southeast-1', aws_access_key_id=resp.json()["AccessKeyId"], aws_secret_access_key = resp.json()["SecretAccessKey"], aws_session_token = resp.json()["SessionToken"])
        print("Info: This may take a while depending on your connection.")
        
        token = ecr_client.get_authorization_token()
        username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        registry = token['authorizationData'][0]['proxyEndpoint']        

        docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        try:
            result = docker_client.login(username, password, registry=registry, reauth=True)
        except docker.errors.APIError:
            print("You don't have ECR repository permissions. Check you AWS credentials with Cognicept team.")
            return False

        images = set(object._docker_images.values())
        N = len(images)
        i = 0
        success_flag = True
        for image_name in images:
            i = i + 1
            try:
                
                for status in docker_client.pull(image_name, stream = True, decode = True):
                    if("progress" not in status):
                        status["progress"] = ""
                    print(f"\r[{i}/{N}] {image_name} - " + status["status"] + " " + status["progress"], end="")                    
                print(f"\r[{i}/{N}] {image_name} - {bcolors.OKBLUE}OK{bcolors.ENDC}\033[K")                
            except docker.errors.ImageNotFound:
                print(f"\r[{i}/{N}] {image_name} - {bcolors.FAIL}FAILED{bcolors.ENDC}\033[K")
                success_flag = False

        print("Info: Run `cognicept restart` to redeploy updated agents.")
        return success_flag
        
