function(doc){
	if(doc.collection === "notifications"){
		emit([doc.service, doc.name], doc.user);
	}
}
