function(doc){
	if(doc.collection === "notifications" && !doc.hasOwnProperty('hidden')){
		emit([doc.service, doc.name], doc.user);
	}
}
