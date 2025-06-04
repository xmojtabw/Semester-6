from mininet.net import Mininet
from mininet.nodelib import LinuxBridge
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')


def torus():
    net = Mininet(switch=OVSSwitch)
    # c0 = net.addController('c0')

    info('*** Adding switches and hosts\n')
    hosts, switches = [], []
    for i in range(3):
        hosts.append([])
        switches.append([])
        for j in range(3):
            sw_name, h_name = f's{i+1}{j+1}', f'h{i+1}{j+1}'
            sw = net.addSwitch(sw_name, failMode='standalone', stp=True)
            h = net.addHost(h_name)
            hosts[i].append(h)
            switches[i].append(sw)

    info('*** connecting the switches and hosts\n')
    for i in range(3):
        for j in range(3):
            net.addLink(switches[i][j], switches[(i+1) % 3][j]) # connect to row under it (if last row => connects to first row)
            net.addLink(switches[i][j], switches[i][(j+1) % 3]) # connect to col after it (if last col => connects to first col)
            net.addLink(switches[i][j], hosts[i][j])


    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    torus()
