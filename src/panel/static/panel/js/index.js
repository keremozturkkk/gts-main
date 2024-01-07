import './dark-mode.js'
import './sidebar.js'


if ($('#pp-upload-btn').length > 0) {

    $(document).ready(function () {

        if ($('#dropzone-file').val() == "") {
            $('#pp-upload-btn').hide();
            $('#pp-select-info').hide();
        }

        $('#dropzone-file').on('change', function(){

            if($('#dropzone-file').val() != "")
            {
                $('#pp-upload-btn').show();
                $('#pp-select-info').show();
                
            }                 
        });
    });
}

if ($('#_payment_type').length > 0) {

    $(document).ready(function () {
    
        $('#_payment_type').on('change', function(){
        
            if($('#_payment_type').find(":selected").val() == "M1"){
                $('#amount').val('100₺')
            }
            else if($('#_payment_type').find(":selected").val() == "M2"){
                $('#amount').val('300₺')
            }
            else if($('#_payment_type').find(":selected").val() == "M3"){
                $('#amount').val('1000₺')
            }
        
        });
    
    });

}