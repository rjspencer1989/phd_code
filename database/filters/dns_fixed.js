function(doc, req){
    if(doc.collection === "dns" and doc.status === "active"){
        return true;
    }
    return false;
}
