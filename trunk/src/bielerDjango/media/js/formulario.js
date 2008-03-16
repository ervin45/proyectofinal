function ajax_beforeSend(){
	jQuery('#ajax_loading').show()
}

function ajax_complete(){
	jQuery('#ajax_loading').hide()
}

function agregar(){
	_agregar('')
}

/*
Agrega una restriccion a un grupo de dependiendo del prefijo (vacio, "ft1_", "ft2")
*/
function _agregar(ft_prefix){
	var dimension = jQuery('#' + ft_prefix + 'dimension').val()
	var level     = jQuery('#' + ft_prefix + 'level').val()
	var val       = jQuery('#' + ft_prefix + 'val').val()

	jQuery('#' + ft_prefix + 'restriction_table_body').createAppend(
		'tr', { class: ft_prefix + 'restriction'}, [
		'td', { align: 'center', style: '' }, dimension,
		'td', { align: 'center', style: '' }, level,
		'td', { align: 'center', style: '' }, val,
		'td', { align: 'center', style: '' }, ['input', {type: 'button', value:'Borrar', class:'borrar'}, 'Borrar']
		]
	);

	alternate_colors(ft_prefix)
	jQuery('.borrar').click(borrar)
	
}

/*
Funcion auxiliar de _get_x_restriction y de _get_y_restriction
*/
function _get_main_restriction(level_hash, prefijo){
	temp = prefijo + "={"
	if(level_hash){
		level_hash.each(function(level){
			temp += "'" + level.key + "': ["

			level.value.each(function(item){
				temp += "'" + item + "', "
			})
			temp = temp.substring(0, temp.length - 2)
			temp += "], "
		})
		temp = temp.substring(0, temp.length - 2)
		

	}
	temp += "}"
	return temp
}

/*
Devuelve un STRING con las restricciones del eje x
*/
function _get_x_restriction(){
	var r = _get_restriction_hash('restriction')
	var x   = jQuery('#x').val()
	return _get_main_restriction(r.get(x), "xr")
}

/*
Devuelve un STRING con las restricciones del eje y
*/
function _get_y_restriction(){
	var r = _get_restriction_hash('restriction')
	var y   = jQuery('#y').val()
	return _get_main_restriction(r.get(y), "yr")
}

/*
Devuelve un HASH con las restricciones de un determinado grupo dependiendo de una determinada clase
("restriction", "ft1_restriction", "ft2_restriction")
*/
function _get_restriction_hash(class){
	var r = new Hash({})

	jQuery('.'+class).each(function(){
		var dimension = jQuery(this).children()[0].innerHTML
		var level     = jQuery(this).children()[1].innerHTML
		var val       = jQuery(this).children()[2].innerHTML
		if(!r.get(dimension)){
			r.set(dimension, new Hash({}))
		}
		if(!r.get(dimension).get(level)){
			r.get(dimension).set(level, [])
		} 
		
		var next_index = r.get(dimension).get(level).length
		r.get(dimension).get(level)[next_index] = val

	})
	return r
}

/*
Devuelve un string con la combinacion de las ore comunes para todas las ft con las particulares de la ft
*/
function _merge_ores(common_ore, ft_ore){
	if(common_ore == "")
		return "ore=[" + ft_ore + "]"

	if(ft_ore == "")
		return "ore=[" + common_ore + "]"

	return "ore=[" + ft_common + ", " + ft_ore + "]"
}

/*
Devuelve un string con la forma de las ore que espera el DWP a partir de un HASH de dimensiones. Ejemplo "[ ['proveedor', 'TODO', {}], ['tiempo', 'mes', {'anio': ['2001']}] ]" 
*/
function _get_restriction_array(r_hash){

	ore_temp = ""
	r_hash.each(function(dimension){
		ore_temp += "["
		ore_temp += "'" + dimension.key + "', "
		ore_temp += "'TODO', "
		ore_temp += "{"
		dimension.value.each(function(level){
			ore_temp += "'" + level.key + "': ["

			level.value.each(function(item){
				ore_temp += "'" + item + "', "
			})
			ore_temp = ore_temp.substring(0, ore_temp.length - 2)
			ore_temp += "], "
		})
		ore_temp = ore_temp.substring(0, ore_temp.length - 2)
		ore_temp += "}], "
	})
	ore_temp = ore_temp.substring(0, ore_temp.length - 2)

	return ore_temp
}


/*
Devuelve las ore de un determinado grupo segun un prefijo. VACIO: para el caso de una ft y "ft1", "ft2" para el caso de 2 ft
*/
function _get_ore(ft_prefix){
	var r_hash = _get_restriction_hash("restriction")
	var x   = jQuery('#x').val()
	var y   = jQuery('#y').val()				
	r_hash.unset(x)
	r_hash.unset(y)
	var common_ore = _get_restriction_array(r_hash)

	var r_ft_hash = _get_restriction_hash(ft_prefix + "_restriction")
	var ft_ore = _get_restriction_array(r_ft_hash)
	
	var ore = _merge_ores(common_ore, ft_ore)

	return ore
}

/*
Apartir de una string con elementos separados por "|" agrega elementos OPTION a un determinado elemento SELECT
*/
function _add_options(select, data){
		var values = data.split("|");
		jQuery('#' + select).html('')
		values.each(function(val){
			jQuery('#' + select).createAppend(
				'option', {}, val
			);
		})
}


function change_cf(){
	var cf_name = jQuery('#cf option:selected').attr('id')
	cf_params = jQuery('#params_' + cf_name).html()
	jQuery('#cube_param_table_body').html(cf_params)
	
}

function _add_param_type(param){
	if(param['type'] == "text"){

		jQuery('#td_' + param['label']).createAppend(
			'input', {type: 'text', class: 'param'}, ''
		)	
	}else if(param['type'] == "select"){
		jQuery('#td_' + param['label']).createAppend(
			'select', {id: 'select_' + param['label'], class: 'param'}, ''
		)

		jQuery.each(param['sequence'], function(i, v){
			jQuery('#select_' + param['label']).createAppend(
				'option', {}, v
			)					
		})	
	}	
}

function set_cf(){
	jQuery.getJSON("/report/get_cf/", function(json){
		jQuery.each(json, function(k, v){

			jQuery('#cf').createAppend(
				'option', {id: k}, v['label']
			);

			jQuery('body').createAppend(
				'table', {id: "params_" + k, style:'display:none'},''
			)
			jQuery.each(v['params'], function(i, param){
				



				jQuery("#params_" + k).createAppend(
					'tr', {},[
					'td', {}, ['label', {}, param['label']],
					'td', {id: 'td_' + param['label']},''
					]
				)

				
				_add_param_type(param)

			})
		})
	});

	change_cf()
}

/*
Devuelve un STRING que representa la lista de parametros para la member_function que espera el DWP
*/
function _get_params(){
	var temp = ''

	var size = jQuery('#param_table_body td.params select').size()
	for(var i = 0; i < size; i++){
		temp += '['
		p = jQuery('#param_table_body td.params select').get()
		ft_and_measure = p[i].value.split(".")
		ft = ft_and_measure[0]
		measure = ft_and_measure[1]
		
		temp += "'" + ft + "', "
		temp += "'" + measure + "', "

		a = jQuery('#param_table_body td.aggregations select').get()
		agregation = "'" + a[i].value + "'"
		temp += agregation
		temp += "], "
	}
	
	temp = temp.substring(0, temp.length - 2)
	temp = 'params=[' + temp + ']'

	return temp
}


/*
Devuelve un STRING que representa la lista de parametros para la cube_function que espera el DWP
*/
function _get_cf_params(){
	var temp = ''

	var size = jQuery('#cube_param_table_body .param').size()
	for(var i = 0; i < size; i++){
		p = jQuery('#cube_param_table_body .param').get()
		cube_param = p[i].value
		temp += "'" + cube_param + "', "
	}
	
	temp = temp.substring(0, temp.length - 2)
	temp = 'params=[' + temp + ']'

	return temp	
}

function borrar(){
	jQuery(this).parent().parent().remove()
	alternate_colors()
}

function alternate_colors(ft_prefix){
	jQuery('table.' + ft_prefix + 'restriction_table tr:even td').removeClass().addClass('even');
	jQuery('table.' + ft_prefix + 'restriction_table tr:odd td').each(function(i){
		if(!jQuery(this).children().is('input')){
			jQuery(this).removeClass().addClass('odd');
		}
	})
}
