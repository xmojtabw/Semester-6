from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from sys import argv
setLogLevel('info')


class TreeTopo(Topo):
    def __init__(self, depth=1):
        Topo.__init__(self)
        d = depth if depth > 1 else 1
        switches = [self.addSwitch(f's{i}')
                    for i in range(1, (2**d))]
        hosts = [self. addHost(f'h{i}')
                 for i in range(1, 2**d+1)]
        for i in range(1, 2**(d-1)):
            self.addLink(switches[i - 1], switches[2*i - 1])
            self.addLink(switches[i - 1], switches[2*i])
        for i in range(2**(d-1), 2**d):
            self.addLink(switches[i-1], hosts[2*i - 2**(d)])
            self.addLink(switches[i-1], hosts[2*i - 2**(d) + 1])


if __name__ == '__main__':
    if len(argv) == 2:
        depth = int(argv[1])
    else:
        depth = 1
    topo = TreeTopo(depth=depth)
    net = Mininet(topo)
    net.start()
    CLI(net)
    net.stop()
