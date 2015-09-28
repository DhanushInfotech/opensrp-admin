jQuery.validator.addMethod('required-cond', function (value, element, params) {
	debugger;
	var selectid=$(element).attr('data-val-required-cond-value');	
	var select_value=$('#'+selectid).val()=="Country" ? false : true;   
   
    return !select_value || value;
}, '');

jQuery.validator.unobtrusive.adapters.add('required-cond', {}, function (options) {
    options.rules['required-cond'] = true;
    options.messages['required-cond'] = options.message;
});
