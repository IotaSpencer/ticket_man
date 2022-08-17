# built-in
import os
from dataclasses import dataclass
# 3rd party
from typing import Union

from omegaconf import OmegaConf, DictConfig, ListConfig

config_path = os.path.join(os.path.expanduser('~'), '.ticket_man', 'config.yml')


@dataclass
class Configs:
    cfg: Union[DictConfig, ListConfig] = OmegaConf.load(config_path)
