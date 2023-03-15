import os
import re
import time
import winsound

alerts = [
     'Ship\'s cargo hold is full',
]

def monitor_logs(log_dir):
    '''Displays a log stream of the most update-to-date logs for realtime
    monitoring. Program beeps if any alerts are found.
    '''
    last_lines = {}

    while True:
        for filename in os.listdir(log_dir):
            filepath = os.path.join(log_dir, filename)
            with open(filepath, 'r') as f:
                last_line = f.readlines()[-1].strip()
                if filename not in last_lines or last_lines[filename] != last_line:
                    message = re.sub('<.*?>', '', last_line)
                    message = re.sub(
                        r'^\[\s*(.*?)\s*\]\s*\((.*?)\)\s*', r'\1 \2: ', message
                    )
                    print(message)
                    if any(string in message for string in alerts):
                         make_tone(iter=2)
                    last_lines[filename] = last_line
        time.sleep(1)

def make_tone(frequency=2500, duration=150, iter=1):
        for _ in range(iter):
            winsound.Beep(frequency, duration)


if __name__ == '__main__':
    log_dir = 'D:\Jameson\Documents\EVE\logs\Gamelogs'
    monitor_logs(log_dir)