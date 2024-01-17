import hydra

from loguru import logger
from omegaconf import DictConfig

from utils.cleaner import Cleaner


@hydra.main(version_base=None, config_path='.', config_name='config')
def main(config: DictConfig) -> None:
    new_data = Cleaner(config)()
    new_data.to_csv(config.input_dir + '_cleaned.csv', index=False)

if __name__ == '__main__':
    main()
