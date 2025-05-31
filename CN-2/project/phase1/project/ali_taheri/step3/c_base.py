import time
import logging

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp, ipv4
from ryu.lib.packet import ether_types

SLEEP_TIME = 0.1
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

class SimpleIPRouter(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    eth_hex_type_mapping = {
        0x800: 'IPv4',
        0x806: 'ARP',
        0x86dd: 'IPv6',
        'IPv4': 0x800,
        'ARP': 0x806,
        'IPv6': 0x86dd
    }

    def __init__(self, *args, **kwargs):
        super(SimpleIPRouter, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.DEBUG)

        self.ip_to_port = {
            1: {'10.0.0.1': 1, '10.0.0.2': 2, '10.0.0.3': 3, '10.0.0.4': 4},
            2: {'10.0.0.1': 1, '10.0.0.2': 2, '10.0.0.3': 3, '10.0.0.4': 4},
            3: {'10.0.0.1': 1, '10.0.0.2': 2, '10.0.0.3': 3, '10.0.0.4': 4},
            4: {'10.0.0.1': 1, '10.0.0.2': 2, '10.0.0.3': 3, '10.0.0.4': 4},
        }

    def add_flow(self, datapath, priority, match, actions, buffer_id=None, inst=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        if inst is None:
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath,
                                    priority=priority, match=match,
                                    instructions=inst)
        datapath.send_msg(mod)
        self.logger.debug(f"{BOLD}{PURPLE}Flow added: Match={match}, Actions={actions}{RESET}")
        time.sleep(SLEEP_TIME)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        self.logger.info(f"Switch connected: DPID={datapath.id}")

        # Drop IPv6
        match = parser.OFPMatch(eth_type=0x86dd)
        self.add_flow(datapath, 0, match, [])

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        self.logger.info(f"{GRAY}[DPID {dpid}] PacketIn on port {in_port}, eth_type={self.eth_hex_type_mapping[eth.ethertype]}{RESET}")
        time.sleep(SLEEP_TIME * 0.5)

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            self.handle_arp(pkt, datapath, in_port, dpid)
        elif eth.ethertype == ether_types.ETH_TYPE_IP:
            self.handle_ip(pkt, datapath, in_port, dpid)

    def handle_arp(self, pkt, datapath, in_port, dpid):
        parser = datapath.ofproto_parser
        arp_pkt = pkt.get_protocol(arp.arp)
        src_ip = arp_pkt.src_ip
        dst_ip = arp_pkt.dst_ip

        self.logger.info(f"{GREEN}[DPID {dpid}] ARP Packet: {src_ip} is asking for {dst_ip}{RESET}")
        time.sleep(SLEEP_TIME)

        out_port = self.ip_to_port.get(dpid, {}).get(dst_ip)

        if out_port:
            self.logger.info(f"{GREEN}[DPID {dpid}] Forwarding ARP to port {out_port}{RESET}")
            actions = [parser.OFPActionOutput(out_port)]

            match = parser.OFPMatch(
                eth_type=ether_types.ETH_TYPE_ARP,
                arp_tpa=dst_ip
            )
            self.add_flow(datapath, 10, match, actions)

            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=datapath.ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=pkt.data
            )
            datapath.send_msg(out)
            time.sleep(SLEEP_TIME)
        else:
            self.logger.warning(f"{YELLOW}[DPID {dpid}] No mapping for ARP IP {dst_ip}, dropping{RESET}")

    def handle_ip(self, pkt, datapath, in_port, dpid):
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        dst_ip = ip_pkt.dst
        src_ip = ip_pkt.src

        self.logger.info(f"{BLUE}[DPID {dpid}] IP Packet: {src_ip} -> {dst_ip}{RESET}")
        time.sleep(SLEEP_TIME)

        out_port = self.ip_to_port.get(dpid, {}).get(dst_ip)
        if out_port:
            self.logger.info(f"{BLUE}[DPID {dpid}] Forwarding IP packet to port {out_port}{RESET}")
            parser = datapath.ofproto_parser
            ofproto = datapath.ofproto

            match = parser.OFPMatch(
                eth_type=ether_types.ETH_TYPE_IP,
                ipv4_dst=dst_ip
            )
            actions = [parser.OFPActionOutput(out_port)]


            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

            self.add_flow(datapath, 10, match, actions, inst=inst)

            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=pkt.data
            )
            datapath.send_msg(out)
            time.sleep(SLEEP_TIME)
        else:
            self.logger.warning(f"[DPID {dpid}] No IP route for {dst_ip}, dropping packet")

