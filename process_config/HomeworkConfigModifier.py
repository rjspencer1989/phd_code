from couchdbkit import *
import os


def getConfigOption(option):
    with(open("%s/homework.conf" % (os.getenv("HOME")))) as fileHandle:
        lineList = fileHandle.readlines()
        for line in lineList:
            if(line.startswith(option)):
                return line


def extractValueFromLine(line):
    components = line.split("=")
    if len(components) == 2:
        value = components[1].strip()
        if value.startswith("\""):
            value = value[1:-1]
        return value


def updateConfig(doc, db):
    if doc['status'] == "pending":
        configuration = doc['configuration']
        interface = extractValueFromLine(getConfigOption("WLESS_IF"))
        lineList = []
        lineList.append("interface=%s\n" % (interface))
        lineList.append("driver=nl80211\n")
        lineList.append("logger_syslog=-1\n")
        lineList.append("logger_syslog_level=2\n")
        lineList.append("logger_stdout=-1\n")
        lineList.append("logger_stdout_level=2\n")
        lineList.append("debug=0\n")
        lineList.append("dump_file=/tmp/hostapd.dump\n")
        lineList.append("ctrl_interface=/var/run/hostapd\n")
        lineList.append("ctrl_interface_group=0\n")
        lineList.append("hw_mode=g\n")
        if configuration[4]['value'] == "n":
            lineList.append("ieee80211n=1\n")
        lineList.append("channel=%s\n" % (configuration[5]['value']))
        lineList.append("beacon_int=100\n")
        lineList.append("dtim_period=2\n")
        lineList.append("max_num_sta=255\n")
        lineList.append("rts_threshold=2347\n")
        lineList.append("fragm_threshold=2346\n")
        lineList.append("macaddr_acl=0\n")
        lineList.append("auth_algs=3\n")
        lineList.append("ignore_broadcast_ssid=0\n")
        lineList.append("wme_enabled=0\n")
        lineList.append("wme_ac_bk_cwmin=4\n")
        lineList.append("wme_ac_bk_cwmax=10\n")
        lineList.append("wme_ac_bk_aifs=7\n")
        lineList.append("wme_ac_bk_txop_limit=0\n")
        lineList.append("wme_ac_bk_acm=0\n")
        lineList.append("wme_ac_be_aifs=3\n")
        lineList.append("wme_ac_be_cwmin=4\n")
        lineList.append("wme_ac_be_cwmax=10\n")
        lineList.append("wme_ac_be_txop_limit=0\n")
        lineList.append("wme_ac_be_acm=0\n")
        lineList.append("wme_ac_vi_aifs=2\n")
        lineList.append("wme_ac_vi_cwmin=3\n")
        lineList.append("wme_ac_vi_cwmax=4\n")
        lineList.append("wme_ac_vi_txop_limit=94\n")
        lineList.append("wme_ac_vi_acm=0\n")
        lineList.append("wme_ac_vo_aifs=2\n")
        lineList.append("wme_ac_vo_cwmin=2\n")
        lineList.append("wme_ac_vo_cwmax=3\n")
        lineList.append("wme_ac_vo_txop_limit=47\n")
        lineList.append("wme_ac_vo_acm=0\n")
        lineList.append("eapol_key_index_workaround=0\n")
        lineList.append("eap_server=0\n")
        lineList.append("own_ip_addr=127.0.0.1\n")
        lineList.append("#original_network")
        lineList.append("#new_network")
        lineList.append("bss=new_net")
        lineList.append("ssid=%s\n" % (configuration[0]['value']))
        if configuration[1]['value'] == "wpa":
            lineList.append("wpa=3\n")
            lineList.append("wpa_passphrase=%s\n" % (configuration[3]['value']))
            lineList.append("wpa_key_mgmt=WPA-PSK\n")
            lineList.append("wpa_pairwise=CCMP")
        elif configuration[1]['value'] == "wep":
            lineList.append("wep_default_key=0\n")
            if configuration[2]['value'] == "txt":
                lineList.append("wep_key0=\"%s\"" % (configuration[3]['value']))
            elif configuration[2]['value'] == "hex":
                lineList.append("wep_key0=%s" % (configuration[3]['value']))
        db.put_attachment(doc, "".join(lineList), "hostapd.conf", "text/plain")
        status = "error"
        with(db.fetch_attachment(doc, "hostapd.conf", stream=True)) as f:
            with(open(extractValueFromLine(getConfigOption('HOSTAPD_CONFIG_FILE')), 'w')) as hc:
                hc.writelines(f.readlines)

                subprocess.Popen(['touch', 'hostapd'], cwd='.')
                hostapdStatus = subprocess.Popen("/etc/init.d/hostapd reload", shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
                if hostapdStatus.count("done") == 2:
                    status = "done"
                subprocess.Popen(['rm', 'hostapd'], cwd='.')
        return status
