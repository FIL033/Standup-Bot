from os import system
from time import sleep
from standup.config import BASE_DIR

main_file_dir = BASE_DIR / 'bot/main.py'
on_start_file_dir = BASE_DIR / 'bot/on_start.py'
system(f"python {on_start_file_dir}")
while True:
    system(f"python {main_file_dir}")
    sleep(10)