function(doc, req){
    if(doc.collection === 'request_notification' && doc.status == 'pending'){
        return true;
    }
    return false;
}
