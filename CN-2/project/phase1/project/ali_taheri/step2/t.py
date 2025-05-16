from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.topolib import TorusTopo
from mininet.log import setLogLevel 

setLogLevel('info')


def torus():
    # Use OVSBridge to enable STP
    class OVSSwitchWithSTP(OVSSwitch):
        def __init__(self, *args, **kwargs):
            kwargs['stp'] = True
            kwargs['failMode'] = "standalone"
            super(OVSSwitchWithSTP, self).__init__(*args, **kwargs)

    topo = TorusTopo(x=3, y=3, n=1)
    net = Mininet(topo=topo, switch=OVSSwitchWithSTP,controller=None)
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    torus()
