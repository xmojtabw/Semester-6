from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, arp
from ryu.controller.handler import DEAD_DISPATCHER
from ryu.topology import event
from ryu.topology.api import get_switch
from collections import defaultdict

class SimpleStaticRouter(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleStaticRouter, self).__init__(*args, **kwargs)
        self.mac_to_port = {}  # {dpid: {mac: port}}
        self.arp_table = {}    # {ip: mac}
        self.routing_table = {
            # destination_subnet : (next_hop_ip, out_port)
            '10.0.1.0/24': ('10.0.1.10', 1),
            '10.0.2.0/24': ('10.0.2.10', 2),
            '10.0.3.0/24': ('10.0.3.10', 3),
            '10.0.4.0/24': ('10.0.4.10', 4),
        }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port
        self.logger.info("switch %s src:%s dst:%s port:%s ",dpid,src,dst,in_port)
        if eth.ethertype == 0x0806:  # ARP
            self.handle_arp(datapath, pkt, in_port)
            return
        elif eth.ethertype == 0x0800:  # IPv4
            self.handle_ipv4(datapath, pkt, in_port)
            return

        # Fallback to simple switching
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
        self.add_flow(datapath, 1, match, actions)
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=msg.buffer_id,
                                  in_port=in_port,
                                  actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)

    def handle_arp(self, datapath, pkt, in_port):
        arp_pkt = pkt.get_protocol(arp.arp)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)

        if arp_pkt.opcode != arp.ARP_REQUEST:
            return

        dst_ip = arp_pkt.dst_ip
        src_ip = arp_pkt.src_ip
        src_mac = eth_pkt.src
        self.arp_table[src_ip] = src_mac

        if dst_ip not in self.arp_table:
            return

        target_mac = self.arp_table[dst_ip]

        arp_reply = packet.Packet()
        arp_reply.add_protocol(ethernet.ethernet(
            ethertype=0x0806,
            dst=src_mac,
            src=target_mac
        ))
        arp_reply.add_protocol(arp.arp(
            opcode=arp.ARP_REPLY,
            src_mac=target_mac,
            src_ip=dst_ip,
            dst_mac=src_mac,
            dst_ip=src_ip
        ))
        arp_reply.serialize()

        datapath.send_msg(datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=datapath.ofproto.OFP_NO_BUFFER,
            in_port=datapath.ofproto.OFPP_CONTROLLER,
            actions=[datapath.ofproto_parser.OFPActionOutput(in_port)],
            data=arp_reply.data
        ))

    def handle_ipv4(self, datapath, pkt, in_port):
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
        dst_ip = ipv4_pkt.dst
        src_ip = ipv4_pkt.src

        self.logger.info("IPv4 packet from %s to %s", src_ip, dst_ip)
        # TODO: Add static routing logic here (based on self.routing_table)
        # For now, it just floods or acts like a learning switch


