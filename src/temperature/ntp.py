import socket
import struct
import sys
import time

if sys.implementation.name == 'micropython':
    import machine

UNIX_EPOCH = 2208988800  # 1970-01-01 00:00:00


def get_ntp_time(host='pool.ntp.org'):
    port = 123
    buf = 1024
    try:
        address = socket.getaddrinfo(host, port)[0][-1]
        msg = b'\x1b' + 47 * b'\0'

        # connect to server
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5)
        client.sendto(msg, address)
        msg, address = client.recvfrom(buf)
    except OSError as ose:
        print(ose)
        return None

    t = struct.unpack('!12I', msg)[10]
    # reference time (in seconds since 1900-01-01 00:00:00)
    t -= UNIX_EPOCH
    tt = time.gmtime(t)
    if sys.implementation.name == 'micropython':
        # set the RTC
        rtc = machine.RTC()
        ttt = (tt[0], tt[1], tt[2], tt[6], tt[3], tt[4], tt[5], 0)
        try:
            rtc.datetime(ttt)
        except OSError as e:
            print(e)
    return tt


def main():
    ntp_time = get_ntp_time()
    print('ntptime: ', ntp_time)
    tt = time.gmtime()
    print('gmtime:  ', tt)
    dt = f'{tt[0]:04d}-{tt[1]:02d}-{tt[2]:02d}T{tt[3]:02d}:{tt[4]:02d}:{tt[5]:02d}+00:00'
    print(dt)


if __name__ == '__main__':
    main()
