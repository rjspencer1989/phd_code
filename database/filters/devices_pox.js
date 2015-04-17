function (doc, req) {
    if (doc.collection === 'devices' && doc.action !== '' && doc.action !== doc.state) {
        return true;
    }
    return false;
}
