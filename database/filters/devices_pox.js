function (doc, req) {
    if (doc.collection === 'devices' && doc.action !== '' && doc.action !== doc.state && doc.changed_by === 'user') {
        return true;
    }
    return false;
}
