	jQuery.noConflict();

	 jQuery(document).ready(function($){
		$.ajaxSetup( {
			type: "POST",
			async: false
		} );

		/* EVENTOS*/

		$('#ft1').change(change_ft)
		$('#ft2').change(change_ft)

		$('#x').change(change_x)
		$('#y').change(change_y)

		$('#dimension').change(change_dimension)
		$('#ft1_dimension').change(change_ft1_dimension)
		$('#ft2_dimension').change(change_ft2_dimension)

		$('#level').change(change_level)
		$('#ft1_level').change(change_ft1_level)
		$('#ft2_level').change(change_ft2_level)

		$('#mf').change(change_mf)

		$('#cf').change(change_cf)

		$('#agregar').click(agregar)
		$('#ft1_agregar').click(ft1_agregar)
		$('#ft2_agregar').click(ft2_agregar)

		$('#aceptar').click(aceptar)

		/* FIN EVENTOS*/


		function _common_dimensions(d1, d2){
			unique_in_1 = _unique_dimensions(d1, d2)

			common = d1
			unique_in_1.each(function(item){
				common = common.without(item)
			})
			return common
		}

		/*
		Devuelve un array con las dimensiones que solo estan en d1
		*/
		function _unique_dimensions(d1, d2){
			unique = d1
			d2.each(function(item){
				unique = unique.without(item)
			})

			return unique
		}

		/*
		Devuelve un array con las dimensiones que solo estan en ft1
		*/
		function _ft1_dimensions(d1, d2){
			return _unique_dimensions(d1, d2)
		}

		/*
		Devuelve un array con las dimensiones que solo estan en ft2
		*/
		function _ft2_dimensions(d1, d2){
			return _unique_dimensions(d2, d1)
		}

		function change_ft(){
			var ft1 = $('#ft1').val()
			jQuery.get("/report/get_dimensions/" + ft1, {}, function(data){	
				dimensions1 = data.split("|")
			})	

			var ft2 = $('#ft2').val()
			jQuery.get("/report/get_dimensions/" + ft2, {}, function(data){
				dimensions2 = data.split("|")
			})

			var common = _common_dimensions(dimensions1, dimensions2)
			var ft1_dimensions = _ft1_dimensions(dimensions1, dimensions2)
			var ft2_dimensions = _ft2_dimensions(dimensions1, dimensions2)

			_add_options("x", common.join("|"))
			_add_options("y", common.join("|"))
			_add_options("dimension", common.join("|"))

			_add_options("ft1_dimension", ft1_dimensions.join("|"))
			_add_options("ft2_dimension", ft2_dimensions.join("|"))

			jQuery.get("/report/get_measures/" + ft1, {}, function(data){
				_add_options("ft1_measures", data)
			})

			jQuery.get("/report/get_measures/" + ft2, {}, function(data){
				_add_options("ft2_measures", data)
			})

			$('#ft1_rest_legend').html(ft1)
			$('#ft2_rest_legend').html(ft2)
			
			set_cf()

			change_x()
			change_y()
			change_dimension()
			change_ft1_dimension()
			change_ft2_dimension()
			change_level()
			change_mf()
		}

		function change_x(){
			var dimension = $('#x').val()
			jQuery.get("/report/get_levels/" + dimension, {}, function(data){
				_add_options("ft1_xl", data)
				_add_options("ft2_xl", data)
			})
		}

		function change_y(){
			var dimension = $('#y').val()
			jQuery.get("/report/get_levels/" + dimension, {}, function(data){
				_add_options("ft1_yl", data)
				_add_options("ft2_yl", data)
			})
		}
		
		function change_dimension(){
			var dimension = $('#dimension').val()
			jQuery.get("/report/get_levels_without_todo/" + dimension, {}, function(data){
				_add_options("level", data)
			})

			change_level()
		}

		function change_ft1_dimension(){
			var dimension = $('#ft1_dimension').val()
			jQuery.get("/report/get_levels_without_todo/" + dimension, {}, function(data){
				_add_options("ft1_level", data)
			})

			change_ft1_level()
		}

		function change_ft2_dimension(){
			var dimension = $('#ft2_dimension').val()
			jQuery.get("/report/get_levels_without_todo/" + dimension, {}, function(data){
				_add_options("ft2_level", data)
			})

			change_ft2_level()
		}

		function change_level(){
			var dimension = $('#dimension').val()
			var level = $('#level').val()
			jQuery.get("/report/get_values/" + dimension + "/" + level, {}, function(data){
				_add_options("val", data)
			})
		}

		function change_ft1_level(){
			var dimension = $('#ft1_dimension').val()
			var level = $('#ft1_level').val()
			jQuery.get("/report/get_values/" + dimension + "/" + level, {}, function(data){
				_add_options("ft1_val", data)
			})
		}

		function change_ft2_level(){
			var dimension = $('#ft2_dimension').val()
			var level = $('#ft2_level').val()
			jQuery.get("/report/get_values/" + dimension + "/" + level, {}, function(data){
				_add_options("ft2_val", data)
			})
		}

		function change_mf(){
			var params_length = $('#mf option:selected').attr('params_length')
	
			var ft1_measures = $('#ft1_measures').html()
			var ft2_measures = $('#ft2_measures').html()

			var aggregations = $('#aggregations').html()		
			
			$('#param_table_body').html('')
			for(var i = 0; i < params_length; i++){
				$('#param_table_body').createAppend(
					'tr', {}, [
					'td', { class: 'params', align: 'center', style: '' }, ['select', {}, ft1_measures + ft2_measures],
					'td', {class: 'aggregations'}, ['select', {}, aggregations]
					]
				);
			}
		}


		function _x_fixed(ft_prefix){
			if( $('#' + ft_prefix + "_x_fixed").attr("checked") ){
				return ":"
			}
			return ""
		}

		function _y_fixed(ft_prefix){
			if( $('#' + ft_prefix + "_y_fixed").attr("checked") ){
				return ":"
			}
			return ""			
		}
		
		function _ft_url(ft_prefix){
			var ft  = $('#' + ft_prefix).val()
			var x   = _x_fixed(ft_prefix) + $('#x').val()
			var y   = _y_fixed(ft_prefix) + $('#y').val()
			var xl  = $('#' + ft_prefix + '_xl').val()
			var yl  = $('#' + ft_prefix + '_yl').val()

			
			
			var xr = _get_x_restriction()
			var yr = _get_y_restriction()

			var ore = _get_ore(ft_prefix)
			
			var ft_url = ft + "/"
			ft_url += x + "/"
			ft_url += y + "/"
			ft_url += xl + "/"
			ft_url += yl + "/"
			ft_url += xr + "/"
			ft_url += yr + "/"
			ft_url += ore

			return ft_url
		}

		function ft1_agregar(){
			_agregar("ft1_")
		}

		function ft2_agregar(){
			_agregar("ft2_")
		}

		function aceptar(){
			var server_and_port = $('#server_and_port').val()

			var ft1_url = _ft_url('ft1')
			var ft2_url = _ft_url('ft2')			

			var mf = $('#mf').val()

			var params = _get_params()

			var cf = $('#cf option:selected').attr('id')

			var cf_params = _get_cf_params()

			var url = "http://" 
			url += server_and_port
			url += "/" + "report2"
			url += "/" + ft1_url
			url += "/" + ft2_url
			url += "/" + mf
			url += "/" + params
			url += "/" + cf
			url += "/" + cf_params
			url += "/"

			$('#url').html(url)

			//window.location.href = url
		}
		

		change_ft()

	 });
