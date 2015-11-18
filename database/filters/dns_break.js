function(doc, req){
    if (doc.collection === "dns" && doc.status === "done" && doc.dns_status === "error") {
        return true;
    }
    return false;
}
