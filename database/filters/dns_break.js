function(doc, req){
    if (doc.collection === "dns" && doc.status === "pending" && doc.dns_status === "error") {
        return true;
    }
    return false;
}
