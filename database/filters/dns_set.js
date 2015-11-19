function(doc, req){
    if(doc.collection === "dns" && doc.dns_status === "active" && doc.status==="pending"){
        return true;
    }
    return false;
}
