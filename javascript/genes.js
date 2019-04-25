// if (coordinates['AT1G071600']) {
// 	alert("blabla")
// } AT2G05518
function infosGene(nameGene,length,coord1,coord2) {

	var canvas = document.getElementById("canvas");
	var context = canvas.getContext('2d');

	context.strokeStyle = "rgb(23, 145, 167)";
	context.lineWidth = 1;
	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(100, 100);  // 1er point
	context.lineTo(300, 100); // 2e point
	context.closePath();     // On relie le 5e au 1er
	context.stroke();

	context.strokeRect(300, 60, length/8, 80)

	   // On relie le 5e au 1er

	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(300+length/8, 100);  // 1er point
	context.lineTo(300+length/8+200, 100); // 2e point
	context.closePath();     // On relie le 5e au 1er
	context.stroke();

	context.strokeStyle = "black";
	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(100, 300);
	context.lineTo(300+length/8+200, 300); // 2e point
	context.closePath();     // On relie le 5e au 1er
	context.stroke();

	context.font = "10pt Optima,Arial";
	context.fillText(coord1, 275, 160);
	context.fillText(coord2, 275+length/8, 160);

	context.font = "bold 18pt Optima,Arial";
	context.fillText(nameGene, 30, 40);

}



function retrieveCoordinates(gene,id) {

	for (var i = 0,nb_signals = gene.length; i<nb_signals;i++) {
		if (i == 0) {
			if (gene[i][1]) {

				var nameGene = gene[i][1];
			} else {

				var nameGene = id;
			}
			var length_gene = gene[i][5]-gene[i][4];
			infosGene(nameGene,length_gene,gene[i][4],gene[i][5]);
		}

}
}


var gene = document.getElementById("gene_input"),
	send = document.getElementById("submit_gene");


send.addEventListener('click',function(evt) {

	evt.preventDefault();
	var id = gene.value;

	if (coordinates[id]) {
		retrieveCoordinates(coordinates[id],id);
	} else {
		alert("Gène non ciblé par les chromatines states significatives");
	}
});


























// url = window.location.toString()

// split_url = url.split("/")

// var gene;

// if (url.split("/")[split_url.length - 1] == "genes.html") {
// 	var gene = window.localStorage.getItem('gene');

// 	alert(gene)

// 	if (gene) {
// 		alert('gene')
// 	} else { 
// 		alert('pas gene')
// 	}

// 	var input_form = document.getElementById('gene_input');

// } else {



// 	var elements = document.getElementsByClassName('links');

// 	for(var i = 0, len = elements.length; i < len; i++) {

// 	const element = elements[i];


//     element.addEventListener('click', function() {

//     	window.localStorage.setItem('gene',element.textContent);

    	

    	
//     });


//     }
   
// }



	// var gene = document.getElementById('gene_1').textContent


// var gene = document.getElementById('gene_1').innerHTML;

// var input_form = document.getElementById('gene_input');

// alert(url.split("/")[split_url.length - 1]);


