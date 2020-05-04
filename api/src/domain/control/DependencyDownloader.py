import subprocess

print('DependencyDownloader library imported')

class DependencyDownloader:

    def __init__(self) :

        subprocess.Popen('python -m pip install --upgrade pip').wait()
        subprocess.Popen('pip install Popen').wait()
        subprocess.Popen('pip install Path').wait()
        subprocess.Popen('pip install pygame').wait()
        subprocess.Popen('pip install numpy').wait()
