from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4
from ryu.lib.packet import ether_types


class IPRouter(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(IPRouter, self).__init__(*args, **kwargs)

        # Static IP routing table: dst_ip → (out_port, dst_mac)
        self.routing_table = {
            '10.0.0.1': (1, '00:00:00:00:00:01'),
            '10.0.0.2': (2, '00:00:00:00:00:02'),
            '10.0.0.3': (3, '00:00:00:00:00:03'),
            '10.0.0.4': (4, '00:00:00:00:00:04'),
        }

        # Our fake router MAC
        self.router_mac = '00:00:00:ff:ff:ff'

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]
        flow_mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                     match=match, instructions=inst, buffer_id=buffer_id or ofproto.OFP_NO_BUFFER)
        datapath.send_msg(flow_mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)

        if not ip:
            return  # only handle IP packets

        dst_ip = ip.dst
        src_ip = ip.src
        in_port = msg.match['in_port']

        if dst_ip not in self.routing_table:
            self.logger.warning("No route for %s", dst_ip)
            return

        out_port, dst_mac = self.routing_table[dst_ip]

        # Install flow
        match = parser.OFPMatch(
            in_port=in_port,
            eth_type=ether_types.ETH_TYPE_IP,
            ipv4_src=src_ip,
            ipv4_dst=dst_ip
        )
        actions = [
            parser.OFPActionSetField(eth_src=self.router_mac),
            parser.OFPActionSetField(eth_dst=dst_mac),
            parser.OFPActionOutput(out_port)
        ]
        self.add_flow(datapath, 1, match, actions)

        # Send this packet too
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data if msg.buffer_id == ofproto.OFP_NO_BUFFER else None
        )
        datapath.send_msg(out)
