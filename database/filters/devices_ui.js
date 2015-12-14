function(doc, req){
    if(doc.collection === 'devices' && doc.action === '' && doc.changed_by === 'system' && !doc.hasOwnProperty('hidden') && !doc.hasOwnProperty('_deleted')){
        return true;
    }
    return false;
}
