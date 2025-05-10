from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')

class LinearSwitchTopology():
    def __init__(self):
        self.net = Mininet(switch=OVSSwitch)
        self.hosts = []
        self.switches = []

        info('*** Adding switches and hosts\n')
        for i in range(4):
            # Add switch
            sw = self.net.addSwitch(f's{i+1}', failMode='standalone')
            self.switches.append(sw)

            # Add host
            host = self.net.addHost(f'h{i+1}')
            self.hosts.append(host)

            # Link host to its corresponding switch
            self.net.addLink(host, sw)
            info(f'Added host h{i+1} <-> switch s{i+1}\n')

        info('*** Connecting switches in a linear chain\n')
        for i in range(3):  # s1-s2, s2-s3, s3-s4
            self.net.addLink(self.switches[i], self.switches[i+1])
            info(f'Linked s{i+1} <-> s{i+2}\n')

    def start(self):
        info('*** Starting network\n')
        self.net.start()
        CLI(self.net)
        self.net.stop()

if __name__ == '__main__':
    topo = LinearSwitchTopology()
    topo.start()
