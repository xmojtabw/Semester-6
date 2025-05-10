from mininet.net import Mininet 
from mininet.node import OVSSwitch
from mininet.cli import CLI 
from mininet.log import setLogLevel, info

setLogLevel('info')

def torus():
    net = Mininet(switch=OVSSwitch)

    info('*** Adding switches\n')
    s00 = net.addSwitch('s00')  
    s10 = net.addSwitch('s10')  
    s01 = net.addSwitch('s01')  

    info('*** Connecting switches\n')
    net.addLink(s00, s01)
    net.addLink(s00, s10)
    net.addLink(s01, s10)

    info('*** Adding hosts and linking to switches\n')
    h00 = net.addHost('h00')
    net.addLink(h00, s00)
    
    h10 = net.addHost('h10')
    net.addLink(h10, s10)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    torus()
