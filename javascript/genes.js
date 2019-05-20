
// Variables ////////////
const canvas = document.getElementById("canvas_gene"),
context = canvas.getContext('2d');
/////////////////////////


function generateCanvas() {

	// Si l'utilisateur clique sur un gène via sur une page
	// state.html, l'identifiant du gène est mis valeur par défault dans le formulaire (genes.html)
	// Si ce n'est pas le cas, l'utilisateur est arrivé sur la page via le menu. (pas
	// de valeur par défault.)
	var form = document.getElementById('gene_input'),
	send = document.getElementById("submit_gene");

	if (window.location.hash) { // Si l'utilisateur a cliqué sur un gène, on récupère la valeur via l'URL ..

		gene = window.location.hash.split('=')[1];

		form.value = gene // .. pour la placer en valeur par défault dans le champ du formulaire
	}

	send.addEventListener('click',function(evt) { // Évènement lorsque l'utilisateur envoit le formulaire

	evt.preventDefault();
	var id = form.value; 

	if (coordinates[id]) { // Si le gène entré est ciblé par au moins une marque significative, on récupère les coordonées
						   // du gène ainsi que les segments chromatiniens associés.
						   // Les valeurs des coordonnées sont retrouvées dans javascript/coordinates.js (fichier généré
		retrieveCoordinates(coordinates[id],id);		// en python).
	
	} else {

		alert("Gène non ciblé par les chromatines states significatives");
	}
});
}  

function retrieveCoordinates(gene,id) {
	// Fonction qui récupère soit les coordonnées du gène, soit des segments épigénétiques.
	let states = []

	for (var i = 0,nb_signals = gene.length; i<nb_signals;i++) {
		// La première liste (d'indice 0) donne accès aux informations du gène 
		// entré par l'utilisateur
		if (i == 0) {
			if (gene[i][1]) { // Si le gène possède un nom

				var nameGene = gene[i][1];
			} else {		  // Sinon on garde l'idenfiant TAIR.

				var nameGene = id;
			}
						  // codon stop    codon start
			var length_gene = gene[i][5]-gene[i][4],
			sens = gene[i][6]

			infosGene(nameGene,length_gene,gene[i][4],gene[i][5],sens);
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
	// Pour trier le tableau numériquement
	states = Array.from(new Set(states));

	states.sort((a, b) => a - b); 

	makeLegend(states);
}

function infosGene(nameGene,length,coord1,coord2,sens) {
	// Les régions promotrices et upstreams font toujours 1000 nucléotides,
	// cependant, le gène peut varier de taille, nécessite donc d'utiliser un facteur 
	// qui normalise la taille du gène, afin que le dessin du gène possède toujours
	// la même surface.
	var normFactor = 1000 / (2000 + length),
	startGene = 100 + (1000*normFactor),
	endGene = startGene + length*normFactor
	y = 200;

	canvas.style.width = "1200px";
	canvas.style.height = "800px";
	context.save();
	context.scale(2,2);

	context.clearRect(0, 0, canvas.width, canvas.height);

	context.strokeStyle = "black";
	context.lineWidth = 1;
	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(100, y);  // On commence le dessin du gène en position x = 100 et y = 200
	context.lineTo(startGene, y); // Puis on dessine un trait jusqu'à la poisition start du gène
	context.closePath();     
	context.stroke();

	context.strokeRect(startGene, y-10.5, length*normFactor, 20.5)	// On dessine ensuite un rectangle représentant
																	// la région codante du gène
	context.beginPath();
	context.lineCap = 'round';
	context.moveTo(endGene, y);  // Enfin, on redessine un trait représentant la région upstream
	context.lineTo(1100, y); 	 // On finit en position x = 1100
	context.closePath();    
	context.stroke();

	context.font = "10pt Optima,Arial";		// On écrit la valeur des coordonnées start et end
	context.fillText(coord1, startGene-25, y+32);
	context.fillText(coord2, endGene-25, y+32);

	context.font = "bold 18pt Optima,Arial"; // Pour écrire le nom du gène
	context.fillText(nameGene, 30, 25);

	context.font = "bold 16pt Optima,Arial"; // Pour écrire le brin d'où provient le gène
	context.fillText('brin '+sens,30,65);

}

function infosSignal(startGene,endGene,state,coord1,coord2) {

	var lengthSig = coord2-coord1,
	lengthGene = endGene-startGene,
	normFactor = 1000 / (2000 + lengthGene),
	y = 300

	if (coord1 < startGene) {

		var start = startGene - coord1,
		startSign = 100+ (1000-start) * normFactor;
	} else {

		var start = coord1 - startGene,
		startSign = 100+ (1000+start) * normFactor;
	}

	endSign = startSign + lengthSig * normFactor;

	context.lineWidth = 2;
	context.beginPath();
	context.lineCap = 'round';

	if (results[state][7] == "over") {	// Les états sur-représentés sont indiqués
										// en rectangle pleins
		context.fillStyle = state_to_color[state];	
		context.fillRect(startSign,100+state_to_y[state],endSign - startSign,5)

	} else {							// Les états sous-représentés en rectangles vides.

		context.strokeStyle = state_to_color[state];
		context.strokeRect(startSign,100+state_to_y[state],endSign - startSign,5)
	}


	context.font = "bold 8pt Optima,Arial";
	context.fillStyle = "black";
	context.fillText(state, (startSign+endSign-10)/2, 100+state_to_y[state]+15);

}

function makeLegend(states) {

	var y = 1000;
	var yB = 1000;

	context.lineWidth = 3;

	context.strokeRect(200, 930, 100, 10);

	context.font = "bold 18pt Optima,Arial";

	rect = new Path2D();
	rect.rect(200, 900, 100, 10);

	context.fillText("state over",320,910)
	context.fillText("state under",320,940)
	context.fill(rect);

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
	// Pour annuler le canvas en cours si l'utilisateur entre un autre gène.
	context.restore()
}


generateCanvas()




