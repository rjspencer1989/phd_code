from pox.core import core
import pox.lib.packet as pkt
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ipv4
from pox.lib.addresses import IPAddr, EthAddr
from pyroute2 import IPDB

MAX_ROUTABLE_LEASE = 2400
MAX_NON_ROUTABLE_LEASE = 30
ROUTABLE_SUBNET = "10.2.0.0"
ROUTABLE_NETMASK = 16
NON_ROUTABLE_SUBNET = "10.3.0.0"
NON_ROUTABLE_NETMASK = 16
MULTICAST_SUBNET = "224.0.0.0"
MULTICAST_NETMASK = 4
INIT_SUBNET = "10.4.0.0"
INIT_NETMASK = 16
MAX_IP_LEN = 32
FLOW_TIMEOUT_DURATION = 10
BRIDGE_INTERFACE_NAME = "br0"


class HomeworkRouting(object):
    def __init__(self):
        core.openflow.addListeners(self)
        self.multicast_ip = {}
        ipdb = IPDB()
        br = ipdb.interfaces[BRIDGE_INTERFACE_NAME]
        self.bridge_mac = EthAddr(br['address'])
        self.mac_permit = set()
        self.mac_whitelist = set()
        core.listen_to_dependencies(self)
        vr_all = self.get_DHCP_mapping().get_data()
        for vr in vr_all:
            val = vr['value']
            if val['state'] == 'permit':
                self.permit_mac(EthAddr(val['mac_address']))
            if val['state'] == 'deny':
                self.whitelist_mac(EthAddr(val['mac_address']))

    def _handle_HomeworkMain_DeviceStateChange(self, event):
        for device in event.devices:
            if "permit" == device['action']:
                self.permit_mac(EthAddr(device['mac']))
            elif "deny" == device['action']:
                self.whitelist_mac(EthAddr(device['mac']))

    def handle_ARP(self, event):
        command = of.OFPFC_ADD
        port = of.OFPP_LOCAL
        if event.parsed.src == self.bridge_mac:
            port = of.OFPP_FLOOD
        action = of.ofp_action_output(port=port)
        self.send_flow_modification(event, command, [action])

    def handle_IPPacket(self, event):
        is_src_router = (event.ofp.in_port == of.OFPP_LOCAL)
        if event.parsed.next.srcip.inNetwork(NON_ROUTABLE_SUBNET, NON_ROUTABLE_NETMASK):
            print "source ip is not routable"
            return
        if event.parsed.src != self.bridge_mac and not self.check_access(event.parsed.src):
            print "%s is not permmited" % (str(event.parsed.src))
            return
        if event.parsed.next.dstip.inNetwork(NON_ROUTABLE_SUBNET, NON_ROUTABLE_NETMASK):
            print "destination is not routable"
            return
        is_src_local = event.parsed.next.srcip.inNetwork(ROUTABLE_SUBNET, ROUTABLE_NETMASK) or event.parsed.next.srcip.inNetwork(INIT_SUBNET, INIT_NETMASK)
        if is_src_local and (event.parsed.next.srcip.toUnsigned(networkOrder=False) & 0x3) == 1:
            if not self.get_DHCP_mapping().is_valid_mapping(event.parsed.next.srcip, event.parsed.src) and event.parsed.src != self.bridge_mac:
                print "received packet from unrecorded mac address"
                return

        if event.parsed.next.dstip.inNetwork(MULTICAST_SUBNET, MULTICAST_NETMASK):
            print "multicast"
            if event.parsed.next.dstip in self.multicast_ip:
                action = of.ofp_action_output(port=of.OFPP_FLOOD)
                command = of.OFPFC_ADD
                self.send_flow_modification(event, command, [action], timeout=30)
        # check if broadcast. Change nw_dst to 10.2.255.255
        if event.parsed.next.dstip.inNetwork(ROUTABLE_SUBNET, ROUTABLE_NETMASK) and ((event.parsed.next.dstip.toUnsigned(networkOrder=False) & 0x3) == 0x3):
            print "broadcast IP"
            nw_new = of.ofp_action_nw_addr()
            nw_new.type = of.OFPAT_SET_NW_DST
            nw_new.nw_addr = IPAddr("10.2.255.255")
            out = of.ofp_action_output(port=of.OFPP_IN_PORT if event.ofp.in_port == 0 else 0)
            actions = [out, nw_new]
            command = of.OFPFC_ADD
            self.send_flow_modification(event, command, actions, timeout=30)
        dst_port = 0
        if event.parsed.next.dstip.inNetwork(ROUTABLE_SUBNET, ROUTABLE_NETMASK) and ((event.parsed.next.dstip.toUnsigned(networkOrder=False) & 0x01) == 0x01):
            dst_port = 1
        else:
            dst_port = 0
        actions = []
        is_dst_local = event.parsed.next.dstip.inNetwork(ROUTABLE_SUBNET, ROUTABLE_NETMASK) or event.parsed.next.dstip.inNetwork(INIT_SUBNET, INIT_NETMASK)
        if is_dst_local and is_src_local and (dst_port != 0) and (not is_src_router):
            dst_mac = self.get_DHCP_mapping().get_mac(event.parsed.next.dstip)

            new_dl_src = of.ofp_action_dl_addr()
            new_dl_src.type = of.OFPAT_SET_DL_SRC
            new_dl_src.set_src(self.bridge_mac)
            actions.append(new_dl_src)

            new_dl_dst = of.ofp_action_dl_addr()
            new_dl_dst.type = of.OFPAT_SET_DL_DST
            new_dl_dst.set_dst(dst_mac)
            actions.append(new_dl_dst)

        out = of.ofp_action_output(port=of.OFPP_FLOOD)
        actions.append(out)
        if 0 < event.ofp.in_port and event.ofp.in_port < of.OFPP_MAX:
            out_of_in = of.ofp_action_output(port=of.OFPP_IN_PORT)
            actions.append(out_of_in)

        command = of.OFPFC_ADD
        self.send_flow_modification(event, command, actions, timeout=30)

    def check_access(self, ether):
        return ether in self.mac_permit

    def handle_IGMP(self, ip_packet):
        print "IGMP packet detected"

    def handle_PAE(self, event):
        packet = event.parsed
        action = of.ofp_action_output(port=of.OFPP_LOCAL)
        command = of.OFPFC_ADD
        self.send_flow_modification(event, command, [action])

    def _handle_ConnectionUp(self, event):
        msg = of.ofp_flow_mod()
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
        msg.match.dl_type = pkt.ethernet.IP_TYPE
        msg.match.nw_proto = pkt.ipv4.IGMP_PROTOCOL
        msg.command = of.OFPFC_ADD
        msg.idle_timeout = of.OFP_FLOW_PERMANENT
        msg.priority = of.OFP_DEFAULT_PRIORITY
        event.connection.send(msg)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if packet.type == pkt.ethernet.ARP_TYPE:
            self.handle_ARP(event)
            return

        if packet.type == pkt.ethernet.PAE_TYPE:
            self.handle_PAE(event)
            return

        if packet.type == pkt.ethernet.IP_TYPE:
            ipp = packet.payload
            if ipp.protocol == ipv4.UDP_PROTOCOL:
                udpp = ipp.payload
                if isinstance(udpp.next, pkt.dhcp):
                    return
            elif ipp.protocol == ipv4.IGMP_PROTOCOL and ipp.dstip == pkt.igmp.IGMP_ADDRESS:
                self.handle_IGMP(ipp)
                return
            else:
                self.handle_IPPacket(event)
                return
        # check if device is allowed to send traffic or is br0
        if not self.check_access(packet.src) and packet.src != self.bridge_mac:
            print "blocking non IP traffic from %s" % (str(packet.src))
            return
        elif self.check_access(packet.dst):
            action = of.ofp_action_output(port=of.OFPP_FLOOD)
            act_list = [action]
            if 0 < event.ofp.in_port and event.ofp.in_port < of.OFPP_MAX:
                action_in = of.ofp_action_output(port=of.OFPP_IN_PORT)
                act_list.append(action_in)
            command = of.OFPFC_ADD
            self.send_flow_modification(event, command, act_list, timeout=30)
        elif packet.dst == self.bridge_mac:
            print "to bridge"
            command = of.OFPFC_ADD
            action = of.ofp_action_output(port=of.OFPP_LOCAL)
            self.send_flow_modification(event, command, [action], timeout=30)
        if packet.dst == EthAddr("\xff\xff\xff\xff\xff\xff"):
            print "broadcast"
            action = of.ofp_action_output(port=of.OFPP_ALL)
            command = of.OFPFC_ADD
            self.send_flow_modification(event, command, [action], timeout=30)
        return

    def get_DHCP_mapping(self):
        return core.components['HomeworkDHCP'].instance

    def whitelist_mac(self, ether):
        if ether in self.mac_permit:
            self.mac_permit.remove(ether)
        self.mac_whitelist.add(ether)
        self.add_to_hostapd_blacklist(ether)
        self.get_DHCP_mapping().change_device_state(ether, 'deny')
        self.revoke_mac_access(ether)

    def permit_mac(self, ether):
        print "permit %s" % (str(ether))
        if ether in self.mac_whitelist:
            self.mac_whitelist.remove(ether)
        self.remove_from_hostapd_blacklist(ether)
        self.mac_permit.add(ether)
        self.get_DHCP_mapping().change_device_state(ether, 'permit')

    def revoke_mac_access(self, ether):
        msg = of.ofp_flow_mod()
        msg.match.dl_src = ether
        msg.out_port = of.OFPP_NONE
        msg.command = of.OFPFC_DELETE
        for connection in core.openflow.connections:
            connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_dst = ether
        msg.out_port = of.OFPP_NONE
        msg.command = of.OFPFC_DELETE
        for connection in core.openflow.connections:
            connection.send(msg)

    def add_to_hostapd_blacklist(self, mac):
        mac_str = "%s\n" % (mac)
        with open('/etc/hostapd.deny', 'r+') as hsd:
            lines = hsd.readlines()
            if mac_str in lines:
                return
            lines.append(mac_str)
            hsd.writelines(lines)
        self.reload_hostapd()

    def remove_from_hostapd_blacklist(self, mac):
        mac_str = "%s\n" % (mac)
        with open('/etc/hostapd.deny', 'r+') as hsd:
            lines = hsd.readlines()
            if mac_str not in lines:
                return
            lines.remove(mac_str)
            hsd.writelines(lines)
        self.reload_hostapd()

    def reload_hostapd(self):
        cmd = ['/etc/init.d/hostapd', 'reload']
        res = subprocess.Popen(cmd)

    def send_flow_modification(self, event, command, actions, timeout=of.OFP_FLOW_PERMANENT, priority=of.OFP_DEFAULT_PRIORITY):
        msg = of.ofp_flow_mod()
        match = of.ofp_match()
        match.in_port = event.ofp.in_port
        match.dl_src = event.parsed.src
        match.dl_dst = event.parsed.dst
        match.dl_type = event.parsed.type
        if isinstance(event.parsed, pkt.vlan):
            match.dl_vlan = event.parsed.id
            match.dl_vlan_pcp = event.ofp.vlan_pcp
        else:
            match.dl_vlan = 0xffff
            match.dl_vlan_pcp = 0
        if event.parsed.type == pkt.ethernet.IP_TYPE:
            match.nw_src = event.parsed.next.srcip
            match.nw_dst = event.parsed.next.dstip
            match.nw_proto = event.parsed.next.protocol
            match.nw_tos = event.parsed.next.tos
            if isinstance(event.parsed.next, pkt.tcp) or isinstance(event.parsed.next, pkt.udp):
                match.tp_src = event.parsed.next.tp_port
                match.tp_dst = event.parsed.next.tp_port
            else:
                match.tp_src = None
                match.tp_dst = None
        else:
            match.nw_src = None
            match.nw_dst = None
            match.nw_proto = None
            match.nw_tos = None
        msg.match = match
        msg.cookie = 0
        msg.command = command
        if event.ofp.buffer_id is not None:
            msg.buffer_id = event.ofp.buffer_id
        msg.idle_timeout = timeout
        msg.hard_timeout = of.OFP_FLOW_PERMANENT
        msg.priority = priority
        msg.flags = of.OFPFF_SEND_FLOW_REM
        for act in actions:
            msg.actions.append(act)
        event.connection.send(msg)


def launch():
    core.registerNew(HomeworkRouting)
