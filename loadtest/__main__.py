from dotenv import load_dotenv
from config import load_config
from loadtest import run

load_dotenv()
raise SystemExit(0 if run(load_config()) else 1)
