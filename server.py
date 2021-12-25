import socket
from cachetools import TTLCache
from signal import signal, SIGPIPE, SIG_DFL

# Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal(SIGPIPE, SIG_DFL)


def covert_bool_to_string(b):
    if b:
        return "True"
    else:
        return "False"


def is_palindrome(string):
    if len(string) % 2 == 0:
        for i in range(int(len(string) / 2)):
            if string[i] == string[len(string) - i - 1]:
                continue
            else:
                return False
    else:
        for i in range(int(len(string) / 2) + 1):
            if string[i] == string[len(string) - i - 1]:
                continue
            else:
                return False
    return True


def have_palindrome(string):
    if len(string) == 1:
        return False
    elif len(string) == 2:
        if string[0] == string[1]:
            return True
        else:
            return False
    elif len(string) == 3:
        if string[0] == string[2]:
            return True
        elif string[0] == string[1]:
            return True
        elif string[1] == string[2]:
            return True
        else:
            return False
    else:
        if is_palindrome(string):
            return True
        elif have_palindrome(string[:len(string) - 1]):
            return True
        elif have_palindrome(string[1:]):
            return True
        else:
            return False


cache = TTLCache(maxsize=10, ttl=360)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
s.bind(('127.0.1.1', port))
s.listen(5)
print("socket is listening")
while True:
    connection, address = s.accept()
    with connection:
        print("connected by:", address)
        while True:
            data = connection.recv(1024).decode()
            if data not in cache:
                cache[data] = have_palindrome(data)
                connection.send(covert_bool_to_string(cache[data]).encode())
            else:
                connection.send(covert_bool_to_string(cache[data]).encode())
        connection.close()

