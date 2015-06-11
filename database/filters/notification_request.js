function(doc, req){
    if(doc.collection === 'request_notification' && doc.status == 'pending' && !doc.hasOwnProperty('hidden')){
        return true;
    }
    return false;
}
