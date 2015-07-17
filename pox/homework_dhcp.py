from pox.core import core
import pox.lib.packet as pkt  # @UnresolvedImport
from pox.lib.addresses import EthAddr, IPAddr, IP_BROADCAST
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
import time
from couchdbkit import Server
from pyroute2 import IPRoute  # @UnresolvedImport
import socket
from process_config import couchdb_config_parser

MAX_LEASE = 43200
ROUTABLE_SUBNET = "10.2.0.0"
ROUTABLE_NETMASK = 16
BRIDGE_INTERFACE_NAME = "br0"


def ip_for_event(event):
    """
    Use a switch's DPID as an EthAddr
    """
    eth = dpid_to_str(event.dpid, True).split("|")[0].replace("-", ":")
    return EthAddr(eth)


class HomeworkDHCP(object):
    instance = None
    """docstring for HomeworkDHCP"""
    def __init__(self):
        core.openflow.addListeners(self)
        self.hostname = None
        self.req_ip = ""
        self.ip_mapping = {}
        self.mac_mapping = {}
        self.dhcp_msg_type = 0
        self.connections = []
        self.clean_leases()
        HomeworkDHCP.instance = self

        self.selected_db = couchdb_config_parser.get_db()

        vr_all = self.get_data()
        for result in vr_all:
            v = result['value']
            dm = Lease(IPAddr(v['ip_address']), EthAddr(v['mac_address']), 0)
            if (v['lease_action'] == 'add' and
                    v['timestamp'] + MAX_LEASE > time.time()):
                self.add_addr(str(self.increment_ip(IPAddr(v['ip_address']),
                                                    networkOrder=True)))
            self.mac_mapping[EthAddr(v['mac_address'])] = dm
            self.ip_mapping[IPAddr(v['ip_address'])] = dm

    def get_data(self, ether=None):
        vr = None
        if ether is None:
            vr = self.selected_db.view('homework-remote/dhcp')
        else:
            vr = self.selected_db.view('homework-remote/dhcp', key=str(ether))
        vr_all = vr.all()
        return vr_all

    def increment_ip(self, ip, networkOrder=False):
        return IPAddr(ip.toUnsigned(networkOrder=networkOrder) + 1)

    def get_dhcp_mapping(self):
        v = []
        for i in self.mac_mapping:
            if self.mac_mapping[i] is None:
                continue
            v.append(str(self.mac_mapping[i]))
        return v

    def clean_leases(self):
        for k in self.ip_mapping:
            if self.ip_mapping[k].lease_end == 0:
                continue
            if self.ip_mapping[k].lease_end <= time.time() + 0.2 * MAX_LEASE:
                self.ip_mapping[k].lease_end = 0
                self.insert_couchdb("del",
                                    self.ip_mapping[k].ip,
                                    self.ip_mapping[k].mac, None, None)
        core.callDelayed(60, self.clean_leases)

    def change_device_state(self, mac, state):
        vr_all = self.get_data(mac)
        if len(vr_all) == 1:
            current_doc = vr_all[0]['value']
            current_doc['state'] = state
            current_doc['action'] = ''
            current_doc['changed_by'] = 'system'
            self.selected_db.save_doc(current_doc, force=True)

    def insert_couchdb(self, lease_action, ip, mac, hostname, port):
        known_devices = self.get_data()
        vr_all = self.get_data(mac)
        if len(vr_all) == 1:
            current_doc = vr_all[0]['value']
            current_doc['lease_action'] = lease_action
            current_doc['ip_address'] = str(ip)
            current_doc['host_name'] = hostname
            current_doc['timestamp'] = time.time()
            if lease_action == 'add':
                current_doc['connection_event'] = 'connect'
            else:
                current_doc['connection_event'] = 'disconnect'
            current_doc['port'] = port
            current_doc['changed_by'] = 'system'
        elif len(vr_all) == 0:
            current_doc = {}
            current_doc['_id'] = str(mac)
            current_doc['collection'] = 'devices'
            current_doc['host_name'] = hostname
            current_doc['device_name'] = ""
            current_doc['ip_address'] = str(ip)
            current_doc['lease_action'] = lease_action
            current_doc['mac_address'] = str(mac)
            current_doc['name'] = ''
            current_doc['state'] = 'pending'
            current_doc['device_type'] = ""
            if len(known_devices) == 0:
                current_doc['action'] = 'permit'
                current_doc['changed_by'] = 'user'
            else:
                current_doc['action'] = ''
                current_doc['changed_by'] = 'system'
            current_doc['notification_service'] = ""
            current_doc['timestamp'] = time.time()
            current_doc['connection_event'] = 'connect'
            current_doc['port'] = port
        else:
            print "MAC Address has more than one lease. stopping"
            return
        self.selected_db.save_doc(current_doc)

    def is_valid_mapping(self, ip, mac):
        if ip not in self.ip_mapping:
            return False
        return mac == self.ip_mapping[ip].mac

    def get_mac(self, ip):
        if ip in self.ip_mapping:
            return self.ip_mapping[ip].mac

    def generate_dhcp_reply(self, dhcp, send_ip, dhcp_msg_type, lease):
        reply_pkt = pkt.dhcp()
        reply_pkt.op = pkt.dhcp.BOOTREPLY
        reply_pkt.htype = 0x01
        reply_pkt.hlen = 0x6
        reply_pkt.xid = dhcp.xid

        if dhcp_msg_type != pkt.dhcp.NAK_MSG:
            reply_pkt.yiaddr = send_ip
            reply_pkt.siaddr = self.increment_ip(send_ip)

        reply_pkt.chaddr = dhcp.chaddr
        reply_pkt.options[pkt.dhcp.MSG_TYPE_OPT] = pkt.DHCP.DHCPMsgTypeOption(dhcp_msg_type)
        reply_pkt.options[pkt.dhcp.SUBNET_MASK_OPT] = pkt.DHCP.DHCPSubnetMaskOption(0xFFFFFFFC)
        reply_pkt.options[pkt.dhcp.REQUEST_LEASE_OPT] = pkt.DHCP.DHCPIPAddressLeaseTimeOption(lease)
        reply_pkt.options[pkt.dhcp.SERVER_ID_OPT] = pkt.DHCP.DHCPServerIdentifierOption(str(self.increment_ip(send_ip)))
        if dhcp_msg_type == pkt.dhcp.NAK_MSG:
            return reply_pkt

        reply_pkt.options[pkt.dhcp.GATEWAY_OPT] = pkt.DHCP.DHCPRoutersOption(str(self.increment_ip(send_ip)))
        reply_pkt.options[pkt.dhcp.DNS_SERVER_OPT] = pkt.DHCP.DHCPDNSServersOption(str(self.increment_ip(send_ip)))
        return reply_pkt

    def check_exists(self, ip, route, br):
        addrs = route.get_addr(socket.AF_INET)
        addr_li = []
        for addr in addrs:
            if addr['index'] == br:
                addr_li.append(addr['attrs'][0][1])

        return ip in addr_li

    def add_addr(self, ip):
        iproute = IPRoute()
        br = iproute.link_lookup(ifname=BRIDGE_INTERFACE_NAME)[0]
        if not self.check_exists(ip, iproute, br):
            iproute.addr('add', br, address=ip, mask=30)
        iproute.close()
        iproute = None

    def del_addr(self, ip):
        iproute = IPRoute()
        br = iproute.link_lookup(ifname=BRIDGE_INTERFACE_NAME)[0]
        if not self.check_exists(ip, iproute, br):
            iproute.addr('delete', br, address=ip, mask=30)
        iproute.close()
        iproute = None

    def find_free_ip(self, subnet, netmask):
        inc = 4
        ip = subnet.toUnsigned(networkOrder=False)
        while (ip & (0xFFFFFFFF << netmask)) == subnet.toUnsigned(networkOrder=False):
            if IPAddr(ip + 1) not in self.ip_mapping:
                break
            ip += inc
        if (ip & (0xFFFFFFFF << netmask)) != subnet.toUnsigned(networkOrder=False):
            print "none available"
            return 0
        return ip

    def select_ip(self, mac_address, msg_type):
        lease_end = time.time() + MAX_LEASE
        if mac_address in self.mac_mapping:
            state = self.mac_mapping[mac_address]
            ip = state.ip.toUnsigned()
            state.lease_end = lease_end
        else:
            ip = self.find_free_ip(IPAddr(ROUTABLE_SUBNET, networkOrder=True),
                                   ROUTABLE_NETMASK)
            if ip is None:
                return
            ip += 1
            state = Lease(IPAddr(ip), mac_address, lease_end)
            self.ip_mapping[IPAddr(ip)] = state
            self.mac_mapping[mac_address] = state
        return IPAddr(ip)

    def parse_dhcp(self, dhcp_packet, event):
        print "dhcp packet handler"
        if len(dhcp_packet.options) == 0:
            return
        if pkt.dhcp.HOST_NAME_OPT in dhcp_packet.options:
            self.hostname = dhcp_packet.options[pkt.dhcp.HOST_NAME_OPT].data
        if pkt.dhcp.REQUEST_IP_OPT in dhcp_packet.options:
            self.req_ip = dhcp_packet.options[pkt.dhcp.REQUEST_IP_OPT].addr
        if pkt.dhcp.MSG_TYPE_OPT in dhcp_packet.options:
            mt = dhcp_packet.options[pkt.dhcp.MSG_TYPE_OPT]
            self.dhcp_msg_type = mt
            if mt == pkt.dhcp.INFORM_MSG:
                return
            elif mt == pkt.dhcp.DECLINE_MSG:
                return
        ip = self.select_ip(dhcp_packet.chaddr, mt)

        if mt == pkt.dhcp.RELEASE_MSG:
            # find mapping and delete it
            self.insert_couchdb("del", ip, dhcp_packet.chaddr, None, None)
            return

        reply_msg_type = pkt.dhcp.OFFER_MSG if self.dhcp_msg_type.type == pkt.dhcp.DISCOVER_MSG else pkt.dhcp.ACK_MSG
        if self.req_ip != 0 and self.dhcp_msg_type == pkt.dhcp.REQUEST_MSG and self.req_ip != int(ip):
            reply_msg_type = pkt.dhcp.nak
            ip = self.req_ip
            print "not allowed that address"
        reply = self.generate_dhcp_reply(dhcp_packet, ip, reply_msg_type, MAX_LEASE)
        if reply_msg_type == pkt.dhcp.ACK_MSG:
            self.add_addr(str(self.increment_ip(ip)))
            print self.connections[0].ports[event.port].name
            self.insert_couchdb("add", ip, dhcp_packet.chaddr, self.hostname, self.connections[0].ports[event.port].name)

        eth = pkt.ethernet(src=ip_for_event(event), dst=event.parsed.src)
        eth.type = pkt.ethernet.IP_TYPE

        ipp = pkt.ipv4(srcip=self.increment_ip(ip))
        ipp.dstip = event.parsed.find('ipv4').srcip
        broadcast = (dhcp_packet.ciaddr == 0)
        if broadcast:
            ipp.dstip = IP_BROADCAST
            eth.dst = pkt.ETHERNET.ETHER_BROADCAST
        ipp.protocol = ipp.UDP_PROTOCOL
        udpp = pkt.udp()
        udpp.srcport = pkt.dhcp.SERVER_PORT
        udpp.dstport = pkt.dhcp.CLIENT_PORT
        udpp.payload = reply
        ipp.payload = udpp
        eth.payload = ipp
        msg = of.ofp_packet_out(data=eth.pack())
        msg.actions.append(of.ofp_action_output(port=event.port))
        event.connection.send(msg)

    def _handle_ConnectionUp(self, event):
        self.connections.append(event.connection)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if packet.type != pkt.ethernet.IP_TYPE:
            return
        ip_packet = packet.payload
        if ip_packet.protocol != pkt.ipv4.UDP_PROTOCOL:
            return
        udp_packet = ip_packet.payload
        if not isinstance(udp_packet.next, pkt.dhcp):
            return
        dhcp_packet = udp_packet.payload
        self.parse_dhcp(dhcp_packet, event)


def launch():
    core.registerNew(HomeworkDHCP)


class Lease(object):
    """Represents DHCP Mapping"""
    def __init__(self, ip, mac, lease_end):
        self.ip = ip
        self.mac = mac
        self.lease_end = lease_end
