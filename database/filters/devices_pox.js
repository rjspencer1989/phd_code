function (doc, req) {
    if (doc.collection === 'devices' && doc.action !== '' && doc.action !== doc.state && doc.changed_by === 'user' && !doc.hasOwnProperty('hidden') && !doc.hasOwnProperty('_deleted')) {
        return true;
    }
    return false;
}
