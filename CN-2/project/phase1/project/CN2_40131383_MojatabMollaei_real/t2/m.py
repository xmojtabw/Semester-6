from mininet.net import Mininet
from mininet.nodelib import LinuxBridge
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')


def full():
    controller = RemoteController('c0', ip='127.0.0.1', port=6653)
    net = Mininet(controller=controller)
    c0 = net.addController('c0', controller=RemoteController)
    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

    info('*** Connecting switches\n')
    net.addLink(s1, h1)  # port 1 s1 -> h1

    net.addLink(s1, s2)  # port 2 s1 <-> port 1 s2

    net.addLink(h2, s2)  # port 2 s2 <-> h2

    net.addLink(s1, s3)  # port 3 s1 -> port 1 s3

    net.addLink(s2, s3)  # port 3 s2 <-> port 2 s3

    net.addLink(h3, s3)  # port 3 s3 <-> h3

    net.addLink(s1, s4)  # port 4 s1 <-> port 1 s4

    net.addLink(s2, s4)  # port 4 s2 <-> port 2 s4

    net.addLink(s3, s4)  # port 4 s3 <-> port 3 s4

    net.addLink(h4, s4)  # port 4 s4 <-> h4


    # Set default gateways and static ARP
    h1.cmd('ip route add default via 10.0.0.254')
    h1.cmd('arp -s 10.0.0.254 00:00:00:00:01:FE')

    h2.cmd('ip route add default via 10.0.0.253')
    h2.cmd('arp -s 10.0.0.253 00:00:00:00:02:FE')

    h3.cmd('ip route add default via 10.0.0.252')
    h3.cmd('arp -s 10.0.0.252 00:00:00:00:03:FE')

    h4.cmd('ip route add default via 10.0.0.251')
    h4.cmd('arp -s 10.0.0.251 00:00:00:00:04:FE')



    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    full()
