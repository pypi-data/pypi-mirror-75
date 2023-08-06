import dataclasses as dc
import os.path as path
from configparser import ConfigParser
from typing import Any, Callable, Dict, List


@dc.dataclass
class Hyperparams:
    def to_dict(self):
        ret = {}
        for fld in dc.fields(self):
            ret[fld.name] = getattr(self, fld.name)
        return ret

    @classmethod
    def load(cls, conffile: str) -> "Hyperparams":
        conf = ConfigParser()
        if not path.exists(conffile):
            raise ValueError(f"Unable to find {conffile}")
        conf.read(conffile)
        confgetters = {int: conf.getint, float: conf.getfloat, bool: conf.getboolean, str: conf.get}
        kwargs = {}
        for fld in dc.fields(cls):
            if fld.name in conf["HYPERPARAMS"]:
                kwargs[fld.name] = confgetters[fld.type]("HYPERPARAMS", fld.name)
        return cls(**kwargs)


@dc.dataclass
class HyperparamsSpec:
    spec: List[Dict[str, Any]]
    factory: Callable[[Dict[str, Any]], Hyperparams]
