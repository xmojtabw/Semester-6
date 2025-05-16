from mininet.net import Mininet
from mininet.nodelib import LinuxBridge
from mininet.node import OVSSwitch, Controller , RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')


def full():
    controller = RemoteController('c0', ip='127.0.0.1', port=6653)
    net = Mininet(controller=controller)
    c0 = net.addController('c0',controller=RemoteController)
    info('*** Adding switches\n')
    s11 = net.addSwitch('s11')
    s21 = net.addSwitch('s21') 
    s12 = net.addSwitch('s12')
    s22 = net.addSwitch('s22')

    info('*** Connecting switches\n')
    net.addLink(s11, s12)
    net.addLink(s11, s21)
    net.addLink(s22, s21)
    net.addLink(s22, s12)
    net.addLink(s11, s22)

    info('*** Adding hosts and linking to leaf switches\n')
    h00 = net.addHost('h00')
    net.addLink(h00, s11)

    h10 = net.addHost('h10')
    net.addLink(h10, s21)

    # h20 = net.addHost('h20')
    # net.addLink(h20, s20)

    h01 = net.addHost('h01')
    net.addLink(h01, s12)

    h11 = net.addHost('h11')
    net.addLink(h11, s22)

    # h21 = net.addHost('h21')
    # net.addLink(h21, s21)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    full()
