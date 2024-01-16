import os
import hydra

import pandas as pd
from loguru import logger
from omegaconf import DictConfig, OmegaConf
from pathlib import Path

from utils.cleaner import Cleaner


@hydra.main(version_base=None, config_path='.', config_name='config')
def main(config: DictConfig) -> None:
    Cleaner(config)()

if __name__ == '__main__':
    main()
