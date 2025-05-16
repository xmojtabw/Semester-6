from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


class SimpleTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')  # No failMode set here
        self.addLink(h1, s1)
        self.addLink(h2, s1)


def run():
    topo = SimpleTopo()
    # Connect to Ryu controller
    controller = RemoteController('c0', ip='127.0.0.1', port=6653)
    net = Mininet(topo=topo, controller=controller)
    net.start()
    CLI(net)  # Enter Mininet CLI to interact
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
