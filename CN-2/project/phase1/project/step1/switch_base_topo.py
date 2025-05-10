from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info 

import argparse 


setLogLevel('info')

class MySingleNetwork():
    def __init__(self,num_host=4):
        self.mn = Mininet(switch=OVSSwitch)
        # info('*** Adding controller\n')
        # self.c0 = self.mn.addController('c0')
        info('*** Adding switch\n')
        self.s1 =  self.mn.addSwitch('s1',failMode='standalone')
        self.hosts = []
        for i in range(num_host):
            info(f'*** Adding host{i+1}\n')
            h = self.mn.addHost(f'h{i+1}')
            self.hosts.append(h)
            self.mn.addLink(h,self.s1)

    def startNetwork(self):
        info('*** Starting network\n')
        self.mn.start()
        CLI(self.mn)
        self.mn.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hosts', type=int, default=4, 
                       help='Number of hosts (default: 4)')
    args = parser.parse_args()
    mynet = MySingleNetwork(args.hosts)
    mynet.startNetwork()


