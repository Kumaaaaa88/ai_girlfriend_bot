from datetime import datetime

def log(title, message):

    time = datetime.now().strftime("%H:%M:%S")

    print(f"\n[{time}] {title}")
    print(message)