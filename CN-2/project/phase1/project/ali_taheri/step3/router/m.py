from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

setLogLevel('info')


def run():
    net = Mininet(controller=RemoteController)
    c0 = net.addController('c0', ip='127.0.0.1', port=6653)

    s1 = net.addSwitch('s1')

    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
    h3 = net.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.0.4/24')

    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    net.start()

    # Add default gateway and static ARP to router MAC
    for h in [h1, h2, h3, h4]:
        h.cmd('ip route add default via 10.0.0.254')
        h.cmd('arp -s 10.0.0.254 00:00:00:ff:ff:ff')  # fake router MAC

    CLI(net)
    net.stop()


if __name__ == '__main__':
    run()
