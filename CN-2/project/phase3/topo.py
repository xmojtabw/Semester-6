from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from sys import argv
setLogLevel('info')


class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        s1 = self.addSwitch('s1',failmode='standalone',stp=True)
        s2 = self.addSwitch('s2', failmode='standalone',stp=True)
        self.addLink(s1, s2)
        self.addLink(s2, s1)  # create loop
        h1 = self.addHost('h1')
        self.addLink('s1', 'h1')
        self.addHost('h2')
        self.addLink('s1', 'h2')
        self.addHost('h3')
        self.addLink('s2', 'h3')
        self.addHost('h4')
        self.addLink('s2', 'h4')




if __name__ == '__main__':
    topo = MyTopo()
    net = Mininet(topo,switch=OVSSwitch)
    net.start()
    CLI(net)
    net.stop()
