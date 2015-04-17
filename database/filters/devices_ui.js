function(doc, req){
    if(doc.collection === 'devices' && doc.action === '' && doc.state !== 'pending'){
        return true;
    }
    return false;
}
