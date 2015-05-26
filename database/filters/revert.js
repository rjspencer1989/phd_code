function (doc, req){
    if(doc.collection === "request_revert"){
        return true;
    }
    return false;
}
