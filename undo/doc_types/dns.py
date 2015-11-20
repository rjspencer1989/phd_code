from base_doc import BaseDoc
import subprocess

class Dns(BaseDoc):
    def get_rev_list(self):
        rl = super(Dns, self)
        rev_list = []
        for rev in rl:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['status'] == "done":
                rev_list.append(rev)
        return rev_list

    def fix_dns(self):
        lines = []
        with open("/etc/dnsmasq.conf", "r") as dc:
            lines = dc.readlines()
            if "no-resolv\n" in lines:
                lines.remove("no-resolv\n")

        with open("/etc/dnsmasq.conf", "w") as dcw:
            dcw.seek(0)
            dcw.writelines(lines)
            dcw.truncate()
        cmd = ["/etc/init.d/dnsmasq", "restart"]
        subprocess.call(cmd)


    def undo(self):
        rev_list = self.get_rev_list()
        if len(rev_list) == 0:
            return None
        rev = rev_list[0]
        doc = self.db.get(self.doc['_id'], rev=rev)
        self.doc = doc
        res = self.db.save_doc(self.doc, force_update=True)
        return res
