function(doc){
	if(doc.collection === "notifications" && doc.hasOwnProperty('hidden') === false){
		emit([doc.service, doc.name], doc.user);
	}
}
