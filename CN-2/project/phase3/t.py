from mininet.net import Mininet
from mininet.nodelib import LinuxBridge
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')


def MyTopo():
    net = Mininet(switch=OVSSwitch)

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1', failMode="standalone", stp=True)
    s2 = net.addSwitch('s2', failMode="standalone", stp=True)

    info('*** Adding links\n')
    net.addLink(s1, s2)
    net.addLink(s2, s1)  # create loop

    h1 = net.addHost('h1')
    net.addLink(h1, s1)

    h2 = net.addHost('h2')
    net.addLink(h2, s1)

    h3 = net.addHost('h3')
    net.addLink(h3, s2)

    h4 = net.addHost('h4')
    net.addLink(h4, s2)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    MyTopo()
