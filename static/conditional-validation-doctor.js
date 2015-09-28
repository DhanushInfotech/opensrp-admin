// jQuery.validator.addMethod('requirediftrue', function (value, element, params) {
// 	debugger;
//     var checkboxId = $(element).attr('data-val-requirediftrue-boolprop');
//     var checkboxValue = $('#' + checkboxId).first().is(":checked");
//     return !checkboxValue || value;
// }, '');

jQuery.validator.addMethod('required-cond', function (value, element, params) {
	debugger;
	var selectid=$(element).attr('data-val-required-cond-value');	
	var select_value=$('#'+selectid).val()=="DOC" ? false : true;   
   
    return !select_value || value;
}, '');

jQuery.validator.unobtrusive.adapters.add('required-cond', {}, function (options) {
    options.rules['required-cond'] = true;
    options.messages['required-cond'] = options.message;
});
