from ryu.app.simple_switch_13 import SimpleSwitch13
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import set_ev_cls, MAIN_DISPATCHER
from ryu.lib.packet import packet, ethernet, ipv4
from ryu.ofproto import ether
from time import sleep
from ryu.lib.packet import arp
from ryu.base import app_manager 
from ryu.log import logging

# logging.setLoggerClass()
class CustomRouterWithSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(CustomRouterWithSwitch, self).__init__(*args, **kwargs)

        # Define static IP routing rules
        self.routing_table = {
            1: {  # s1
                ('10.0.0.1', '10.0.0.2'): (1, 2),
                ('10.0.0.1', '10.0.0.3'): (1, 3),
                ('10.0.0.1', '10.0.0.4'): (1, 4),
            },
            2: {  # s2
                ('10.0.0.2', '10.0.0.1'): (2, 1),
                ('10.0.0.2', '10.0.0.3'): (2, 3),
                ('10.0.0.2', '10.0.0.4'): (2, 4),
            },
            3: {  # s3
                ('10.0.0.3', '10.0.0.1'): (3, 1),
                ('10.0.0.3', '10.0.0.2'): (3, 2),
                ('10.0.0.3', '10.0.0.4'): (3, 4),
            },
            4: {  # s4
                ('10.0.0.4', '10.0.0.1'): (4, 1),
                ('10.0.0.4', '10.0.0.2'): (4, 2),
                ('10.0.0.4', '10.0.0.3'): (4, 3),
            }
        }
        

        # Virtual IPs and MACs per switch interface (e.g., towards each host)
        self.router_interfaces = {
            1: {'ip': '10.0.0.251', 'mac': '00:00:00:00:01:FE'},  # s1
            2: {'ip': '10.0.0.252', 'mac': '00:00:00:00:02:FE'},  # s2
            3: {'ip': '10.0.0.253', 'mac': '00:00:00:00:03:FE'},  # s3
            4: {'ip': '10.0.0.254', 'mac': '00:00:00:00:04:FE'},  # s4
        }


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        logging.log("sdfdsf")
        sleep(0.1)
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        dpid = datapath.id
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        self.logger.error("packet")
        print("packet")

        # IPv4 packets → our custom logic
        if eth.ethertype == ether.ETH_TYPE_IP:
            self.logger.info("new ip packet")
            ip_pkt = pkt.get_protocol(ipv4.ipv4)
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst

            self.logger.info("Routing: Switch %s: %s → %s (in_port=%s)",
                             dpid, src_ip, dst_ip, in_port)

            rule_key = (src_ip, dst_ip)

            if rule_key not in self.routing_table.get(dpid, {}):
                self.logger.warning(
                    "No route on s%s for %s → %s", dpid, src_ip, dst_ip)
                return

            expected_in, out_port = self.routing_table[dpid][rule_key]

            if in_port != expected_in:
                self.logger.warning(
                    "Wrong in_port %s (expected %s)", in_port, expected_in)
                return

            match = parser.OFPMatch(
                in_port=in_port,
                eth_type=ether.ETH_TYPE_IP,
                ipv4_src=src_ip,
                ipv4_dst=dst_ip
            )
            actions = [parser.OFPActionOutput(out_port)]
            self.add_flow(datapath, 1, match, actions)

            data = msg.data if msg.buffer_id == ofproto.OFP_NO_BUFFER else None
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=msg.buffer_id,
                in_port=in_port,
                actions=actions,
                data=data
            )
            datapath.send_msg(out)

