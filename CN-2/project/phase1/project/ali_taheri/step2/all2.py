from mininet.topo import LinearTopo, MinimalTopo , Topo   
from mininet.topolib import TreeTopo, TorusTopo 
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

import argparse


class FullTopo(Topo):
    def build(self, k=3, n=1):
        if k <= 1 or n <= 0:
            raise Exception("k must be > 1 and n must be > 0")

        switches = {}

        # Create switches
        for i in range(k):
            sw_name = f's{i+1}'
            switches[i] = self.addSwitch(sw_name)

        # Create hosts and connect them to switches
        for i in range(k):
            for j in range(n):
                host_name = f'h{i+1}x{j+1}' if n > 1 else f'h{i+1}'
                host = self.addHost(host_name)
                self.addLink(host, switches[i])

        # Create full mesh between switches
        for i in range(k):
            for j in range(i + 1, k):
                self.addLink(switches[i], switches[j])

            


class CustomizedSwitch(OVSSwitch):
    def __init__(self, *args, **kwargs):
        kwargs['stp'] = True
        kwargs['failMode'] = "standalone"
        super(CustomizedSwitch, self).__init__(*args, **kwargs)


def linear():
    topo = LinearTopo(k=4, n=1)  # k swtiches and 1 host for each one
    net = Mininet(topo=topo,switch=CustomizedSwitch,controller=None)
    net.start()
    CLI(net)
    net.stop()


def minimal():
    topo = MinimalTopo()  # 2 switches 2 hosts
    net = Mininet(topo=topo,switch=CustomizedSwitch,controller=None)
    net.start()
    CLI(net)
    net.stop()


def tree():
    topo = TreeTopo(depth=2, fanout=2)  #
    net = Mininet(topo=topo,switch=CustomizedSwitch,controller=None)
    net.start()
    CLI(net)
    net.stop()


def torus():
    topo = TorusTopo(x=3, y=3, n=1)
    net = Mininet(topo=topo, switch=CustomizedSwitch, controller=None)
    net.start()
    CLI(net)
    net.stop()

def full():
    topo = FullTopo(k=4,n=2)
    net = Mininet(topo=topo,switch=CustomizedSwitch,controller=None)
    net.start()
    CLI(net)
    net.stop()
    
    
if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser()
    parser.add_argument('--topo', type=str, default='linear',
                        help='specify the topology')
    args = parser.parse_args()
    topo = str(args.topo).lower()
    if topo == "linear":
        linear()
    elif topo == "minimal":
        minimal()
    elif topo == "tree":
        tree()
    elif topo == "torus":
        torus()
    elif topo == "full":
        full()
