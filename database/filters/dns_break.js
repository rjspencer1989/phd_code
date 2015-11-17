function(doc, req){
    if (doc.collection === "dns" && doc.status === "error") {
        return true;
    }
    return false;
}
