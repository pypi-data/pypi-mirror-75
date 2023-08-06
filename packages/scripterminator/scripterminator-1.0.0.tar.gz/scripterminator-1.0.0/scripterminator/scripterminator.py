import time
import psutil
import subprocess


def terminate_script(file, delay=0):
    try:
        sprocess = subprocess.Popen(['python '+file], shell=True)
        pid = sprocess.pid
        process = psutil.Process(pid)
        if psutil.pid_exists(pid):
            if process.status() == 'running':
                time.sleep(delay)
                process.terminate()
                return True
        else:
            return False
    except IOError:
        return False
