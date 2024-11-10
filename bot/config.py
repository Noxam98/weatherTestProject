# config.py
from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    BOT_TOKEN: str
    WEATHER_API_KEY: str

def load_config() -> Config:
    env = Env()
    env.read_env()
    
    return Config(
        BOT_TOKEN=env.str("BOT_TOKEN"),
        WEATHER_API_KEY=env.str("WEATHER_API_KEY")
    )
