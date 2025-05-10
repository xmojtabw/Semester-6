from mininet.net import Mininet 
from mininet.nodelib import LinuxBridge
from mininet.cli import CLI 
from mininet.log import setLogLevel, info

setLogLevel('info')

def torus():
    net = Mininet(switch=LinuxBridge)

    info('*** Adding switches\n')
    s00 = net.addSwitch('s00')  
    s10 = net.addSwitch('s10')  
    s01 = net.addSwitch('s01')  
    s11 = net.addSwitch('s11')  

    info('*** Connecting switches\n')
    net.addLink(s00,s01)
    net.addLink(s00,s10)
    net.addLink(s11,s10)
    net.addLink(s11,s01)




    info('*** Adding hosts and linking to leaf switches\n')
    h00 = net.addHost('h00')
    net.addLink(h00, s00)
    
    h10 = net.addHost('h10')
    net.addLink(h10, s10)
    
    # h20 = net.addHost('h20')
    # net.addLink(h20, s20)
    
    h01 = net.addHost('h01')
    net.addLink(h01, s01)
    
    h11 = net.addHost('h11')
    net.addLink(h11, s11)
    
    # h21 = net.addHost('h21')
    # net.addLink(h21, s21)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    torus()
