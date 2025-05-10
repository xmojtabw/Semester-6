from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')

def tree_topology_two_level():
    net = Mininet(switch=OVSSwitch)

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1',failMode='standalone')  # Root
    s2 = net.addSwitch('s2',failMode='standalone')  # Level 1
    s3 = net.addSwitch('s3',failMode='standalone')
    s4 = net.addSwitch('s4',failMode='standalone')

    info('*** Connecting level 1 switches to root switch\n')
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)

    info('*** Adding hosts and linking to leaf switches\n')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')


    net.addLink(h1, s2)
    net.addLink(h2, s3)
    net.addLink(h3, s4)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    tree_topology_two_level()
