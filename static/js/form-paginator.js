$(document).ready(function(){

var q = 1, qMax = 0;

$(function () {
    qMax = $('#ascend_form div.group').length;
    $('#ascend_form div.group').hide();
    $('#ascend_form div.group:nth-child(1)').show();
    $('#btnSubmit').on('click', function (event) {
        event.preventDefault();
        handleClick();
    });
});

function handleClick() {
    if (q < qMax) {
        $('#ascend_form div.group:nth-child(' + q + ')').hide();
        $('#ascend_form div.group:nth-child(' + (q + 1) + ')').show();
        if (q == (qMax - 1)) {
            $('#token').focus();
            $('#btnSubmit').hide();
        }
        q++;
    } else {
        // alert('Submitting'); // Add code to submit your form
        
        // document.ascend_form.submit();

        document.getElementById("ascend_form").submit();

        //if(document.ascend_form.onsubmit &&
        //    !document.ascend_form.onsubmit())
        //    {
        //       return;
        //     }
        // document.ascend_form.submit();
    }
}
});