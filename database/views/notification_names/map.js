function(doc){
	if(doc.collection === "notifications"){
		emit(doc.name, null);
	}
}
