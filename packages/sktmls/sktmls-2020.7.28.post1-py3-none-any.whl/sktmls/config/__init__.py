import os
import sys
import importlib

MLS_RUNTIME_ENV = os.environ.get("MLS_RUNTIME_ENV")

if MLS_RUNTIME_ENV and MLS_RUNTIME_ENV not in ["YE", "EDD", "LOCAL"]:
    raise Exception(f"Unsupported MLS_RUNTIME_ENV: {MLS_RUNTIME_ENV}")
else:
    __HOSTNAME = os.environ.get("HOSTNAME", "").lower()

    if __HOSTNAME.startswith("bdp-dmi"):
        MLS_RUNTIME_ENV = "YE"
    elif __HOSTNAME.startswith("vm-skt"):
        MLS_RUNTIME_ENV = "EDD"
    else:
        MLS_RUNTIME_ENV = "LOCAL"

importlib.import_module(f"sktmls.config.{MLS_RUNTIME_ENV.lower()}")


class Config:
    def __init__(self, runtime_env: str):
        setattr(self, "MLS_RUNTIME_ENV", MLS_RUNTIME_ENV)

        module = sys.modules[f"sktmls.config.{runtime_env}"]
        for key in dir(module):
            if key.isupper():
                setattr(self, key, getattr(module, key))


config = Config(MLS_RUNTIME_ENV.lower())
