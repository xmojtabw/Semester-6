from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4
from ryu.ofproto import ether


class SimpleRouter13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleRouter13, self).__init__(*args, **kwargs)

        # Router MAC/IP per switch (acting as default gateway)
        self.router_interfaces = {
            1: {'ip': '10.0.0.254', 'mac': '00:00:00:00:01:FE'},
            2: {'ip': '10.0.0.253', 'mac': '00:00:00:00:02:FE'},
            3: {'ip': '10.0.0.252', 'mac': '00:00:00:00:03:FE'},
            4: {'ip': '10.0.0.251', 'mac': '00:00:00:00:04:FE'},
        }

        # Static IP routing table: (src_ip, dst_ip): (in_port, out_port)
        self.routing_table = {
            1: {('10.0.0.1', '10.0.0.2'): (1, 2), ('10.0.0.1', '10.0.0.3'): (1, 3), ('10.0.0.1', '10.0.0.4'): (1, 4)},
            2: {('10.0.0.2', '10.0.0.1'): (2, 1), ('10.0.0.2', '10.0.0.3'): (2, 3), ('10.0.0.2', '10.0.0.4'): (2, 4)},
            3: {('10.0.0.3', '10.0.0.1'): (3, 1), ('10.0.0.3', '10.0.0.2'): (3, 2), ('10.0.0.3', '10.0.0.4'): (3, 4)},
            4: {('10.0.0.4', '10.0.0.1'): (4, 1), ('10.0.0.4', '10.0.0.2'): (4, 2), ('10.0.0.4', '10.0.0.3'): (4, 3)},
        }

        # Static host MACs
        self.host_macs = {
            '10.0.0.1': '00:00:00:00:00:01',
            '10.0.0.2': '00:00:00:00:00:02',
            '10.0.0.3': '00:00:00:00:00:03',
            '10.0.0.4': '00:00:00:00:00:04',
        }

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority,
            match=match, instructions=inst,
            buffer_id=buffer_id if buffer_id != ofproto.OFP_NO_BUFFER else None
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        self.logger.log("packer arrvier in %s in port %s",dpid,in_port)
        if eth.ethertype != ether.ETH_TYPE_IP:
            return  # Skip non-IP

        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        src_ip = ip_pkt.src
        dst_ip = ip_pkt.dst

        self.logger.info("Router %d: IP %s -> %s", dpid, src_ip, dst_ip)

        rule = self.routing_table.get(dpid, {}).get((src_ip, dst_ip))
        if not rule:
            self.logger.warning("No route on s%d for %s -> %s", dpid, src_ip, dst_ip)
            return

        expected_in, out_port = rule
        if in_port != expected_in:
            self.logger.warning("Wrong in_port %s (expected %s)", in_port, expected_in)
            return

        # Rewrite MACs: router MAC as source, host MAC as destination
        router_mac = self.router_interfaces[dpid]['mac']
        dst_mac = self.host_macs.get(dst_ip)

        if not dst_mac:
            self.logger.warning("Unknown dst MAC for IP %s", dst_ip)
            return

        actions = [
            parser.OFPActionSetField(eth_src=router_mac),
            parser.OFPActionSetField(eth_dst=dst_mac),
            parser.OFPActionOutput(out_port)
        ]

        match = parser.OFPMatch(
            in_port=in_port,
            eth_type=ether.ETH_TYPE_IP,
            ipv4_src=src_ip,
            ipv4_dst=dst_ip
        )

        self.add_flow(datapath, 1, match, actions, msg.buffer_id)

        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data
            )
            datapath.send_msg(out)
