from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, arp
from ryu.lib.packet import ether_types
from ryu.lib.mac import haddr_to_bin
from ryu.lib import mac

class SimpleIPRouter(app_manager.RyuApp):
    OFP_VERSION = [ofproto_v1_3.OFP_VERSION]

    # Static mapping of IP to MAC and switch/port
    host_table = {
        '10.0.0.1': {'mac': '00:00:00:00:00:01', 'dpid': 1, 'port': 1},
        '10.0.0.2': {'mac': '00:00:00:00:00:02', 'dpid': 2, 'port': 1},
        '10.0.0.3': {'mac': '00:00:00:00:00:03', 'dpid': 3, 'port': 1},
        '10.0.0.4': {'mac': '00:00:00:00:00:04', 'dpid': 4, 'port': 1},
    }

    def __init__(self, *args, **kwargs):
        super(SimpleIPRouter, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        self.datapaths[dp.id] = dp

        # Install table-miss flow
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        self.add_flow(dp, 0, match, actions)

    def add_flow(self, dp, priority, match, actions):
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=dp, priority=priority, match=match, instructions=inst
        )
        dp.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        parser = dp.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            self.handle_arp(pkt, dp, in_port)
        elif eth.ethertype == ether_types.ETH_TYPE_IP:
            self.handle_ip(pkt, dp, in_port)

    def handle_arp(self, pkt, dp, in_port):
        arp_pkt = pkt.get_protocol(arp.arp)

        if arp_pkt.opcode != arp.ARP_REQUEST:
            return

        dst_ip = arp_pkt.dst_ip
        if dst_ip not in self.host_table:
            return

        target = self.host_table[dst_ip]
        src_mac = target['mac']
        dst_mac = pkt.get_protocol(ethernet.ethernet).src

        arp_reply = packet.Packet()
        arp_reply.add_protocol(ethernet.ethernet(
            src=src_mac, dst=dst_mac, ethertype=ether_types.ETH_TYPE_ARP))
        arp_reply.add_protocol(arp.arp(
            opcode=arp.ARP_REPLY,
            src_mac=src_mac,
            src_ip=dst_ip,
            dst_mac=arp_pkt.src_mac,
            dst_ip=arp_pkt.src_ip
        ))
        arp_reply.serialize()

        actions = [dp.ofproto_parser.OFPActionOutput(in_port)]
        out = dp.ofproto_parser.OFPPacketOut(
            datapath=dp,
            buffer_id=dp.ofproto.OFP_NO_BUFFER,
            in_port=dp.ofproto.OFPP_CONTROLLER,
            actions=actions,
            data=arp_reply.data)
        dp.send_msg(out)

    def handle_ip(self, pkt, dp, in_port):
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        dst_ip = ip_pkt.dst

        if dst_ip not in self.host_table:
            return

        dst_info = self.host_table[dst_ip]
        dst_dp = self.datapaths[dst_info['dpid']]
        dst_mac = dst_info['mac']
        dst_port = dst_info['port']

        # install flows in both directions
        match = dp.ofproto_parser.OFPMatch(
            eth_type=ether_types.ETH_TYPE_IP,
            ipv4_dst=dst_ip
        )
        actions = [
            dp.ofproto_parser.OFPActionSetField(eth_dst=dst_mac),
            dp.ofproto_parser.OFPActionOutput(dst_port)
        ]
        self.add_flow(dp, 10, match, actions)

        # Forward this packet
        actions = [
            dp.ofproto_parser.OFPActionSetField(eth_dst=dst_mac),
            dp.ofproto_parser.OFPActionOutput(dst_port)
        ]
        out = dp.ofproto_parser.OFPPacketOut(
            datapath=dp,
            buffer_id=dp.ofproto.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=pkt.data)
        dp.send_msg(out)

