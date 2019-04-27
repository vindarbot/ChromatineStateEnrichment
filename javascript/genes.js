// if (coordinates['AT1G071600']) {
// 	alert("blabla")
// } AT2G05518

function getValueForm() {
	// Fonction qui peremt de récupérer le gène cliqué par l'utilisateur sur une page
	// state.html, pour y mettre en valeur par défault dans le formulaire (genes.html)
	// Si ce n'est pas le cas, l'utilisateur est arrivé sur la page via le menu. (pas
	// de valeur par défault.)
	var form = document.getElementById('gene_input'),
	send = document.getElementById("submit_gene");

	if (window.location.hash) {

		gene = window.location.hash.split('=')[1];

		form.value = gene
	}

	send.addEventListener('click',function(evt) {

	evt.preventDefault();
	var id = form.value;

	if (coordinates[id]) {

		retrieveCoordinates(coordinates[id],id);

	} else {

		alert("Gène non ciblé par les chromatines states significatives");

	}

});
}  



function infosGene(nameGene,length,coord1,coord2) {

	var normFactor = 1000 / (2000 + length),
	startGene = 100 + (1000*normFactor),
	endGene = startGene + length*normFactor
	y = 100;

	var canvas = document.getElementById("canvas"),
	context = canvas.getContext('2d');
	canvas.style.width = "1200px";
	canvas.style.height = "800px";
	context.save();
	context.scale(2,2);

	context.clearRect(0, 0, canvas.width, canvas.height);

	context.strokeStyle = "black";
	context.lineWidth = 1;
	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(100, y);  // 1er point
	context.lineTo(startGene, y); // 2e point
	context.closePath();     // On relie le 5e au 1er
	context.stroke();

	context.strokeRect(startGene, y-10.5, length*normFactor, 20.5)

	   // On relie le 5e au 1er

	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(endGene, y);  // 1er point
	context.lineTo(1100, y); // 2e point
	context.closePath();     // On relie le 5e au 1er
	context.stroke();

	context.font = "10pt Optima,Arial";
	context.fillText(coord1, startGene-25, y+32);
	context.fillText(coord2, endGene-25, y+32);

	context.font = "bold 18pt Optima,Arial";
	context.fillText(nameGene, 30, 25);

}


function infosSignal(startGene,endGene,state,coord1,coord2) {

	// alert(results[state][7])

	var lengthSig = coord2-coord1,
	lengthGene = endGene-startGene,
	normFactor = 1000 / (2000 + lengthGene),
	y = 200

	var canvas = document.getElementById("canvas"),
	context = canvas.getContext('2d');




	if (coord1 < startGene) {

		var start = startGene - coord1,
		startSign = 100+ (1000-start) *normFactor,
		endSign = startSign + lengthSig * normFactor;

	} else {

		var start = coord1 - startGene,
		startSign = 100+ (1000+start) *normFactor,
		endSign = startSign + lengthSig * normFactor;

	}


	context.lineWidth = 2;
	context.beginPath();
	context.lineCap = 'round';

	if (results[state][7] == "over") {

		context.fillStyle = state_to_color[state];
		context.fillRect(startSign,state_to_y[state],endSign - startSign,5)

	} else {

		context.strokeStyle = state_to_color[state];
		context.strokeRect(startSign,state_to_y[state],endSign - startSign,5)
	}
	// context.moveTo(startSign, state_to_y[state]);  // 1er point
	// context.lineTo(endSign, state_to_y[state]); // 2e point
	// context.closePath();     // On relie le 5e au 1er


	context.font = "bold 8pt Optima,Arial";
	context.fillStyle = "black";
	context.fillText(state, (startSign+endSign-10)/2, state_to_y[state]+15);

}

function makeLegend(states) {

	var y = 700;
	var yB = 700;

	var canvas = document.getElementById("canvas"),
	context = canvas.getContext('2d');



	context.lineWidth = 3;

	context.strokeRect(200, 630, 100, 10);
	context.fillRect(200, 600, 100, 10);

	context.font = "bold 18pt Optima,Arial";
	context.fillText("state over",320,610)
	context.fillText("state under",320,640)



	for (index in states) {



		state = states[index];
		context.fillStyle = state_to_color[state];

		if (index > 8) {

			context.fillRect(1200, yB, 80, 40);
			
		} else {

			context.fillRect(200, y, 80, 40);

		}

		context.fillStyle = "black";
		

		if (index > 8) {
			context.fillText(state + "  :  "+ state_to_name[state], 1300, yB+30);

			yB = yB+60;

		} else {

			context.fillText(state + "  :  "+ state_to_name[state], 300, y+30);

			y = y+60;

		}
	}
}


function resetScale() {

	var canvas = document.getElementById("canvas"),
	context = canvas.getContext('2d');
	context.restore()
}



function retrieveCoordinates(gene,id) {

	let states = []

	for (var i = 0,nb_signals = gene.length; i<nb_signals;i++) {
		// La première liste (d'indice 0) donne accès aux informations du gène *
		// entré par l'utilisateur
		if (i == 0) {
			if (gene[i][1]) {

				var nameGene = gene[i][1];
			} else {

				var nameGene = id;
			}
			var length_gene = gene[i][5]-gene[i][4];
			infosGene(nameGene,length_gene,gene[i][4],gene[i][5]);

		// Les autres lignes donnent accès aux informations des différentes 
		// marques épigénétiques.
		} else {
			states.push(gene[i][0])

			infosSignal(gene[0][4],gene[0][5],gene[i][0],gene[i][2],gene[i][3])

			if (i == nb_signals -1) {
				resetScale()
			}

		}
	}

	states = Array.from(new Set(states));

	states.sort((a, b) => a - b); 

	makeLegend(states);
}

// var duplicatedArray = [1, 2, 3, 4, 5, 1, 1, 1, 2, 3, 4];
// var uniqueArray = Array.from(new Set(duplicatedArray));



getValueForm()



























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


