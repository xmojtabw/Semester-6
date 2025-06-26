from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')


def generateMac(index):
    return '00:00:00:00:00:{:02x}'.format(index)


def MyTopo():
    net = Mininet(switch=OVSSwitch)

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1', failMode="standalone")
    s2 = net.addSwitch('s2', failMode="standalone")
    s3 = net.addSwitch('s3', failMode="standalone")

    info('*** Adding links\n')
    net.addLink(s1, s3)
    net.addLink(s3, s2) 

    h1 = net.addHost('h1', mac=generateMac(1))
    net.addLink(h1, s1)

    h2 = net.addHost('h2', mac=generateMac(2))
    net.addLink(h2, s1)

    h3 = net.addHost('h3', mac=generateMac(3))
    net.addLink(h3, s2)

    h4 = net.addHost('h4', mac=generateMac(4))
    net.addLink(h4, s2)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    MyTopo()
