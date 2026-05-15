import subprocess
import sys


def main():
    commands = [
        [sys.executable, "manage.py", "daily_report_reminder"],
        [sys.executable, "manage.py", "runserver"],
    ]
    running_services = [
        subprocess.Popen(command)
        for command in commands
    ]
    try:
        for service in running_services:
            service.wait()
    except KeyboardInterrupt:
        print("\nShutting down services...")

        for service in running_services:
            service.terminate()

if __name__ == "__main__":
    main()
