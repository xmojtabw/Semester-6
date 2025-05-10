from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')

def minimal_two_host_topology():
    net = Mininet()

    info('*** Adding two hosts\n')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    info('*** Creating a direct link between h1 and h2\n')
    net.addLink(h1, h2)

    info('*** Starting the network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping the network\n')
    net.stop()

if __name__ == '__main__':
    minimal_two_host_topology()
