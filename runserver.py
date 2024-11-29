import subprocess


def collect_static():
    print("Dinesh, I am Collecting static files...")
    subprocess.run(["python", "manage.py", "collectstatic"])


def run_server():
    print("Dinesh, I am Starting Django server...")
    subprocess.run(["python", "manage.py", "runserver"])


if __name__ == "__main__":
    collect_static()
    run_server()