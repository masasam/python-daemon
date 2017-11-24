from datetime import datetime
import os
import sys
import time


def daemonize():
    def fork():
        if os.fork():
            sys.exit()

    def throw_away_io():
        stdin = open(os.devnull, 'rb')
        stdout = open(os.devnull, 'ab+')
        stderr = open(os.devnull, 'ab+', 0)

        for (null_io, std_io) in zip((stdin, stdout, stderr),
                                     (sys.stdin, sys.stdout, sys.stderr)):
            os.dup2(null_io.fileno(), std_io.fileno())

    fork()
    os.setsid()
    fork()
    throw_away_io()


def create_empty_file():

    now = datetime.now().strftime('%Y%m%d%H%M%S')

    filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), f'tmp/{now}.txt')

    with open(filepath, 'w') as f:
        f.write(str(os.getpid()))


def create_empty_files(interval=60):

    while True:
        create_empty_file()
        time.sleep(interval)


if __name__ == '__main__':
    daemonize()
    create_empty_files()
