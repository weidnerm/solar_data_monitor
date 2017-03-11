import argparse
import errno
import os
from select import select
import time

class OneFifo(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        if os.path.exists(self.name):
            os.unlink(self.name)
        os.mkfifo(self.name)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if os.path.exists(self.name):
            os.unlink(self.name)

    def write(self, data):
        print "Waiting for client to open FIFO..."
        try:
            server_file = os.open(self.name, os.O_WRONLY | os.O_NONBLOCK)
        except OSError as exc:
            if exc.errno == errno.ENXIO:
                server_file = None
            else:
                raise
        if server_file is not None:
            print "Writing line to FIFO..."
            try:
                os.write(server_file, data)
                print "Done."
            except OSError as exc:
                if exc.errno == errno.EPIPE:
                    pass
                else:
                    raise
            os.close(server_file)

    def read_nonblocking(self):
        result = None
        try:
            client_file = os.open(self.name, os.O_RDONLY | os.O_NONBLOCK)
        except OSError as exc:
            if exc.errno == errno.ENOENT:
                client_file = None
            else:
                raise
        if client_file is not None:
            try:
                rlist = [client_file]
                wlist = []
                xlist = []
                rlist, wlist, xlist = select(rlist, wlist, xlist, 0.01)
                if client_file in rlist:
                    result = os.read(client_file, 1024)
            except OSError as exc:
                if exc.errno == errno.EAGAIN or exc.errno == errno.EWOULDBLOCK:
                    result = None
                else:
                    raise
            os.close(client_file)
        return result

    def read(self):
        try:
            with open(self.name, 'r') as client_file:
                result = client_file.read()
        except OSError as exc:
            if exc.errno == errno.ENOENT:
                result = None
            else:
                raise
        if not len(result):
            result = None
        return result

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', action='store_true',
                        help='Set this flag for the client')
    parser.add_argument('-n', '--non-blocking', action='store_true',
                        help='Set this flag to read without blocking')
    result = parser.parse_args()
    return result

if __name__ == '__main__':
    args = parse_argument()
    if not args.client:
        with OneFifo('/tmp/fifotest.fifo') as one_fifo:
            while True:
                one_fifo.write('one line')
                time.sleep(0.1)
    else:
        one_fifo = OneFifo('/tmp/fifotest.fifo')
        while True:
            if args.non_blocking:
                result = one_fifo.read_nonblocking()
            else:
                result = one_fifo.read()
            if result is not None:
                print result
