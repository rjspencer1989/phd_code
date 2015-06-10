function (doc, req) {
    if (doc.collection === 'devices' && doc.action !== '' && doc.action !== doc.state && doc.changed_by === 'user' && !doc.hasOwnProperty('hidden')) {
        return true;
    }
    return false;
}
