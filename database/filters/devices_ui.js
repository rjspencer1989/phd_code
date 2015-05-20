function(doc, req){
    if(doc.collection === 'devices' && doc.action === '' && doc.state !== 'pending' && doc.changed_by === 'system'){
        return true;
    }
    return false;
}
