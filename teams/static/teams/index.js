$(document).ready(function() {
    var show1 = localStorage.getItem('show-1');
    var show2 = localStorage.getItem('show-2');

    if (show1 === 'true') {
        $('#form-1').show();
        $('#btn-1').hide();
    } else {
        $('#form-1').hide();
        $('#btn-1').show();   
    }

    if (show2 === 'true') {
        $('#form-2').show();
        $('#btn-2').hide();
    } else {
        $('#form-2').hide();
        $('#btn-2').show(); 
    }
});

function openForm(num) {
    $("#btn-" + num).hide();
    localStorage.setItem('show-' + num, 'true'); //store state in localStorage
    $("#form-" + num).show();
}

function closeForm(num) {
    $("#form-" + num).hide();
    localStorage.setItem('show-' + num, 'false'); //store state in localStorage
    $("#btn-" + num).show();
}
