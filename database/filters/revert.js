function (doc, req){
    if(doc.collection === "request_revert" && doc.status === 'pending'){
        return true;
    }
    return false;
}
