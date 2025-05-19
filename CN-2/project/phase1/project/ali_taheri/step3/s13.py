from ryu.app.simple_switch_13 import SimpleSwitch13
from ryu.ofproto import ofproto_v1_3
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, set_ev_cls


class MySDN(SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MySDN, self).__init__(*args, **kwargs)
        self.meter_installed = set()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        dpid = datapath.id

        # Set meter only on s1, port 4
        if dpid == 11 and (dpid, 4) not in self.meter_installed:
            self.add_ingress_limit(datapath, port_no=4,
                                   meter_id=1, rate=64)  # 64 kbps
            self.meter_installed.add((dpid, 4))

        super().switch_features_handler(ev)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Inject meter only if traffic is from port 4
        instructions = []
        if 'in_port' in match and match['in_port'] == 4:
            instructions.append(
                parser.OFPInstructionMeter(1, ofproto.OFPIT_METER)
            )
        instructions.append(
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
        )

        flow_mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions,
            buffer_id=buffer_id if buffer_id else ofproto.OFP_NO_BUFFER
        )
        datapath.send_msg(flow_mod)

    def add_ingress_limit(self, datapath, port_no, meter_id=1, rate=64):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        bands = [parser.OFPMeterBandDrop(rate=rate, burst_size=100)]
        meter_mod = parser.OFPMeterMod(
            datapath=datapath,
            command=ofproto.OFPMC_ADD,
            flags=ofproto.OFPMF_KBPS,
            meter_id=meter_id,
            bands=bands
        )
        datapath.send_msg(meter_mod)
        self.logger.info(
            f"Added meter {meter_id} for port {port_no} at {rate} kbps")
