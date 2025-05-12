from mininet.topo import LinearTopo , MinimalTopo 
from mininet.topolib import TreeTopo , TorusTopo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

import argparse

def linear():
    topo = LinearTopo(k=4,n=1)  # k swtiches and 1 host for each one
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()

def minimal():
    topo = MinimalTopo()  # 2 switches 2 hosts
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()

def tree():
    topo = TreeTopo(depth= 2, fanout = 2 )  # 
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()
    
def torus():
    topo = TorusTopo(x=3,y=3,n=1)  
    net = Mininet(topo=topo, build=False)
    for sw in topo.switches():
        net.addSwitch(sw, stp=True)
    net.build()
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
