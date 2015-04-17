function(doc, req){
    if(doc.collection === 'notification-request' && doc.status == 'pending'){
        return true;
    }
    return false;
}
