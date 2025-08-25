from tickr.utils import get_json_data
from pathlib import Path

TICKR_DIR = Path(__file__).parent.parent # Proyect base dir
CONFIG_PATH = TICKR_DIR / 'tickr' / 'config' / 'config.json' #"tickr\config\config.json"

config = get_json_data(CONFIG_PATH)

config['event']['path'] = Path(config['event']['path']).expanduser() 