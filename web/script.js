	let stocks_count = 1;
async function add_stock() {
	stocks_count++;
	let htmlcode = '<div class="stock"><input id="name'+stocks_count+'" type="text" placeholder="Название инструмента" required=""><input id="part'+stocks_count+'" class="part" type="text" placeholder="Доля" required=""></div>'
	stocks.insertAdjacentHTML('beforeend', htmlcode);
	}

async function set_stocks() {
	eel.clear_stocks();
	for (var i = 1; i <= stocks_count; i++) {
		let name = document.getElementById('name'+i).value;
		let part = document.getElementById('part'+i).value;
		eel.set_stocks(name, part);
	}
}
async function let_calc() {
	document.getElementById('result').innerHTML = await eel.let_calc()();
}
async function save_index() {
	let new_index_name = document.getElementById('NewIndexName').value;
	eel.save_index(new_index_name);
}
async function saved_indexes_init() {
	let el = document.getElementById('savedIndexes');
	el.innerHTML = " ";
	let get = await eel.saved_indexes_init()();
	for (var k = 1; k <= get.length; k++) {
		let saved_index_name = get[k-1];
		let htmlcode2 = '<option class="savedIndex" value="'+saved_index_name+'"></option>'
		savedIndexes.insertAdjacentHTML('beforeend', htmlcode2);
	}
}
async function get_saved_index() {
	eel.clear_stocks();
	let selected_index = document.getElementById('select_saved_index').value;
	eel.get_saved_index(selected_index);
}
jQuery().ready(function() {
	saved_indexes_init();
});

jQuery('#add_stock').on('click', function() {
	add_stock();
});
jQuery('#let_calc').on('click', function() {
	set_stocks();
	let_calc();
});
jQuery('#SaveIndex').on('click', function() {
	set_stocks();
	save_index();
	saved_indexes_init();
});
jQuery('#get_index').on('click', function() {
	get_saved_index();
	let_calc();
});