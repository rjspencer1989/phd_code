function(doc, req){
    if (doc.collection === 'devices' && doc.action === '' && doc.changed_by === 'user' && doc.hasOwnProperty('_deleted') === false) {
        return true;
    }
    return false;
}
