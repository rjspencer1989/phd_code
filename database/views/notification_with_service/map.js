function(doc){
	if(doc.collection === "notifications"){
		emit([doc.name, doc.service], doc.user);
	}
}
