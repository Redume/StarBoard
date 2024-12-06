from aiogram import Bot
import yaml

config = yaml.safe_load(open('config.yaml'))
bot = Bot(config['token'])