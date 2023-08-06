import os
import subprocess


def _get_default_local_ip():
    cmd = '''ifconfig eth0|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"'''
    local_ip = None
    try:
        local_ip = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        pass
    if local_ip is None or local_ip == '':
        local_ip = "localhost"
    return local_ip


_env_variables = [
    ("debug_mode", "ENABLE_DEBUG_MODE", False, bool),
    ("flink_home", "FLINK_HOME", "/opt/flink-1.9.0"),
    ("alink_deps_dir", "ALINK_DEPS_DIR", ""),
    ("local_ip", "LOCAL_IP", _get_default_local_ip()),
    ("gateway_port", "PYALINK_GATEWAY_PORT", None),
]

g_config = {}

for entry in _env_variables:
    env_v = os.getenv(entry[1], entry[2])
    if len(entry) > 3:
        env_v = entry[3](env_v)
    g_config[entry[0]] = env_v
