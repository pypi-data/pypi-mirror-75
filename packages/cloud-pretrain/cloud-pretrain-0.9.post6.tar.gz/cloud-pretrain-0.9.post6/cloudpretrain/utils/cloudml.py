# coding: utf8
from __future__ import print_function, absolute_import

import re
import os
import tempfile
import json
import click
from six import iteritems
from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.models.train_job import TrainJob
from cloud_ml_sdk.models.model_service import ModelService
from cloudpretrain.config import default_config
from cloudpretrain.constants import V100_16G_GPU, CLOUD_PRETRAIN_BUCKET
from cloudpretrain.constants import V100_32G_GPU
from cloudpretrain.constants import T4_16G_GPU
from cloudpretrain.constants import P4_8G_GPU
from contextlib import contextmanager
from enum import Enum


class Cloud_ml_task_type(Enum):
    TRAIN = 1
    SERVING = 2


class CloudMlException(Exception):
    pass


class XCloudMlClient(CloudMlClient):

    @staticmethod
    def process_response(response, select_col_name=None, enable_exit=True):
        if response.ok:
            if select_col_name:
                return json.loads(response.content.decode("utf-8"))[select_col_name]
            else:
                return json.loads(response.content.decode("utf-8"))
        else:
            raise CloudMlException(response.content)

if default_config.validate():
    cloudml_client = XCloudMlClient()
else:
    cloudml_client = None


@contextmanager
def create_temp_dir():
    temp_dir = tempfile.mkdtemp(prefix="cloud-pretrain")
    try:
        yield temp_dir
    finally:
        if os.path.exists(temp_dir):
            os.removedirs(temp_dir)


def create_cloudml_name(stage, task_name, timestamp=None):
    """ {stage}-{task_name}[-{timestamp}] """
    cloudml_name = "{}-{}".format(stage, task_name)
    if timestamp:
        cloudml_name += "-{}".format(timestamp)
    return cloudml_name


def rerun_train_job(task_name):
    cloudml_client.rerun_train_job(task_name)


def delete_cloudml_job(cloudml_task):
    try:
        if is_train_job(cloudml_task.name, cloudml_task.task_type):
            cloudml_client.delete_train_job(cloudml_task.name)
        else:
            cloudml_client.delete_model_service(cloudml_task.name, cloudml_task.get_serving_version())
    except:
        click.echo("maybe target cloudml job: {} deleted".format(cloudml_task.name))


def is_train_job(task_name, task_type):
    if task_type and task_type == Cloud_ml_task_type.TRAIN:
        return True
    
    if task_name.startswith("train-"):
        return True
    
    return False


def is_cloudml_job_exists(job_name, is_train_job, serving_version):
    try:
        if is_train_job:
            cloudml_client.describe_train_job(job_name)
        else:
            cloudml_client.describe_model_service(job_name, serving_version)
    except:
        return False
    
    return True


def get_task_state(task_name, task_type):
    try:
        if is_train_job(job_name, task_type):
            job_info = cloudml_client.describe_train_job(job_name)
        else:
            job_info = cloudml_client.describe_model_service(job_name, "1")
        
        return job_info['state']
    except:
        return None


def get_cloudml_train_job(cloudml_job_name):
    return cloudml_client.describe_train_job(cloudml_job_name)


def get_cloudml_serving_job(cloudml_task_name, serving_version):
    return cloudml_client.describe_model_service(cloudml_task_name, serving_version)


def parse_memory(memory_string):
    """
    Only support Gigabytes and Megabytes memories.
    10G ==> 10
    10Gi ==> 10
    0 ==> 0
    500M ==> 0.5
    500Me ==> 0.5
    otherwise, ValueError
    """
    if memory_string.endswith("G"):
        memory = int(memory_string[:-1])
    elif memory_string.endswith("Gi"):
        memory = int(memory_string[:-2])
    elif memory_string.isdigit():
        memory = int(memory_string)
    elif memory_string.endswith("M"):
        m_memory = int(memory_string[:-1])
        memory = m_memory / 1000.0
    elif memory_string.endswith("Me"):
        m_memory = int(memory_string[:-2])
        memory = m_memory / 1000.0
    else:
        raise ValueError("Cannot parse memory string: {}".format(memory_string))
    return memory


def parse_cpu(cpu_string):
    """
    Parse CPU string into number.
    10 ==> 10
    500m ==> 0.5
    """
    if cpu_string.isdigit():
        return int(cpu_string)
    elif cpu_string.endswith("m"):
        m_cpu = int(cpu_string[:-1])
        return m_cpu / 1000.0
    else:
        raise ValueError("Cannot parse cpu string: {}".format(cpu_string))


def find_available_priority_class(gpu_limit=None, cpu_limit=None, memory_limit=None, model_service=False):
    """
    Find available priority class with the limit of gpu/cpu/memory (all integers, only support Gigabytes memory).
    If None, then find without such limit.
    The available priority class will be used to submit CloudML train job or model service. Because model service
    doesn't support 'preferred' priority class, if model_service is True, we will ignore the 'preferred' priority class.

    For example:
    # find priority class with 10 cpu, 25G memory available, which will NOT be used to submit model service
    find_available_priority_class(None, 10, 25)
    # or
    find_available_priority_class(0, 10, 25)
    # find priority class with 1 gpu, 10 cpu, 25G memory available, which will be used to submit model service
    find_available_priority_class(1, 10, 25, True)
    """
    quotas = cloudml_client.get_quota_v2()
    return _find_available_priority_class(quotas,
                                          gpu_limit=gpu_limit,
                                          cpu_limit=cpu_limit,
                                          memory_limit=memory_limit,
                                          model_service=model_service)


def list_history_servings(serving_name):
    return ""


def _find_any_available_class(quota, gpu_type):
    if 'spec' not in quota or 'used' not in quota:
        raise ValueError("No spec / used quota find!")

    spec = quota['spec']
    used = quota['used']

    if gpu_type not in spec or gpu_type not in used:
        return 0
    
    return int(spec[gpu_type]) - int(used[gpu_type])


def _find_available_priority_class(quotas, gpu_limit=None, cpu_limit=None, memory_limit=None, model_service=False):
    available_quotas = {}
    for quota in quotas:
        match = re.search("^.*-(best-effort|preferred|guaranteed)$", quota["name"])
        if match:
            priority_class = match.group(1)
        else:
            raise ValueError("Quota name parsed error! {}".format(quota["name"]))
        
        # find gpu which type is v100 first.
        available_gpu = _find_any_available_class(quota, V100_16G_GPU)

        if available_gpu is None or available_gpu <= 0:
            available_gpu = _find_any_available_class(quota, V100_32G_GPU)

        available_cpu = (parse_cpu(quota["spec"]["limits.cpu"]) -
                         parse_cpu(quota["used"]["limits.cpu"]))

        available_memory = (parse_memory(quota["spec"]["limits.memory"]) -
                            parse_memory(quota["used"]["limits.memory"]))

        if (gpu_limit is None or available_gpu >= gpu_limit) \
                and (cpu_limit is None or available_cpu >= cpu_limit) \
                and (memory_limit is None or available_memory >= memory_limit):
            available_quotas[priority_class] = {
                "gpu": available_gpu,
                "cpu": available_cpu,
                "memory": available_memory
            }
   
    # find available priority class
    if "guaranteed" in available_quotas:
        return "guaranteed"
    elif "preferred" in available_quotas and not model_service:
        return "preferred"
    elif "best-effort" in available_quotas:
        return "best-effort"
    else:
        raise ValueError("No available quota.")


class ConfiguredTrainJob(TrainJob):

    def __init__(self, job_name, module_name, trainer_uri, *args, **kwargs):
        super(ConfiguredTrainJob, self).__init__(job_name, module_name, trainer_uri, *args, **kwargs)
        # self.fds_bucket = default_config.fds_bucket
        self.fds_mounts = "fds://{}/{},fds://{}/{}".format(default_config.fds_endpoint, default_config.fds_bucket, default_config.fds_endpoint, CLOUD_PRETRAIN_BUCKET)
        self.fds_endpoint = default_config.fds_endpoint
        self.owner_email = default_config.org_mail
        self.args = {}
        self.config_quota()

    def config_quota(self, priority_class="best-effort",
                     cpu_limit="10",
                     memory_limit="25G",
                     gpu_limit="1",
                     gpu_type="v100",
                     gpu_memory="32g"):
        self.priority_class = priority_class
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit
        if gpu_limit == '0':
            self.gpu_limit = None
        else:
            self.gpu_limit = gpu_limit
        if self.gpu_limit is not None and int(self.gpu_limit):
            self.gpu_type = gpu_type
            self.gpu_memory = gpu_memory
        else:
            self.gpu_type = None

    def submit(self):
        self.job_args = self.get_job_args()
        cloudml_client.submit_train_job(self.get_json_data())

    def get_job_args(self):
        _args = []
        for k, v in iteritems(self.args):
            if isinstance(v, bool):
                # if True, then add this option to args.
                if v:
                    _args.append("--{}".format(k))
            else:
                _args.append("--{} {}".format(k, v))
        return " ".join(_args)


class ConfiguredModelService(ModelService):

    def __init__(self, model_name, model_version, model_uri, *args, **kwargs):
        super(ConfiguredModelService, self).__init__(model_name, model_version, model_uri, *args, **kwargs)
        self.fds_bucket = default_config.fds_bucket
        self.fds_endpoint = default_config.fds_endpoint
        self.owner_email = default_config.org_mail
        self.config_quota()

    def config_quota(self, priority_class="best-effort",
                     cpu_limit="5",
                     memory_limit="20G",
                     gpu_limit="1",
                     gpu_type="v100",
                     gpu_memory="32g"):
        self.priority_class = priority_class
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit
        self.gpu_limit = gpu_limit
        self.gpu_memory = gpu_memory
        self.gpu_type = gpu_type

    def submit(self):
        # todo:: check quota here
        cloudml_client.create_model_service(self)