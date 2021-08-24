$(document).ready(function(){

var q = 1, qMax = 0;

$(function () {
    qMax = $('#acces_form div.group').length;
    $('#acces_form div.group').hide();
    $('#acces_form div.group:nth-child(1)').show();
    $('#btnNext').on('click', function (event) {
        event.preventDefault();
        handleClick();
    });
});

function handleClick() {
    if (q < qMax) {
        $('#acces_form div.group:nth-child(' + q + ')').hide();
        $('#acces_form div.group:nth-child(' + (q + 1) + ')').show();
        if (q == (qMax - 1)) {
            $('#btnNext').html('Submit Answers');
        }
        q++;
    } else {
        // alert('Submitting'); // Add code to submit your form
        
        // document.acces_form.submit();

        document.getElementById("acces_form").submit();

        //if(document.acces_form.onsubmit &&
        //    !document.acces_form.onsubmit())
        //    {
        //       return;
        //     }
        // document.acces_form.submit();
    }
}
});