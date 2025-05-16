from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')

def custom_tree_topology():
    net = Mininet(switch=OVSSwitch)

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1',failMode='standalone')  # root
    s2 = net.addSwitch('s2',failMode='standalone')  # level 1 left
    s3 = net.addSwitch('s3',failMode='standalone')  # level 1 right
    s4 = net.addSwitch('s4',failMode='standalone')  # level 2 under s2

    info('*** Creating switch hierarchy\n')
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s4)

    info('*** Adding hosts\n')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    info('*** Connecting hosts\n')
    net.addLink(h1, s4)
    net.addLink(h2, s4)
    net.addLink(h3, s3)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    custom_tree_topology()
