from subprocess import Popen

def play_audio(file):
    Popen("sudo mpg321 ./audios/" + file, shell=True).wait()