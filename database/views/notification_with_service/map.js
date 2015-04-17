function(doc){
	if(doc.collection === "notifications"){
		emit([doc.name, doc.service], {
			"name" : doc.name,
			"service" : doc.service,
			"user": doc.user
		});
	}
}
