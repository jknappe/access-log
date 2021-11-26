$(document).ready(function(){

var q = 1, qMax = 0;

$(function () {
    qMax = $('#login_form div.group').length;
    $('#login_form div.group').hide();
    $('#login_form div.group:nth-child(1)').show();
    $('#btnSubmit').on('click', function (event) {
        event.preventDefault();
        handleClick();
    });
});

function handleClick() {
    if (q < qMax) {
        $('#login_form div.group:nth-child(' + q + ')').hide();
        $('#login_form div.group:nth-child(' + (q + 1) + ')').show();
        if (q == (qMax - 1)) {
            $('#token').focus();
            $('#btnSubmit').hide();
        }
        q++;
    } else {
        // alert('Submitting'); // Add code to submit your form
        
        // document.login_form.submit();

        document.getElementById("login_form").submit();

        //if(document.login_form.onsubmit &&
        //    !document.login_form.onsubmit())
        //    {
        //       return;
        //     }
        // document.login_form.submit();
    }
}
});

