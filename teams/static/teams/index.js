$(document).ready(function() {
    /*
     * Controls whether the query forms are displayed in the schedule tool
     */
    // Get bools from html/localstorage
    var show1 = localStorage.getItem('show-1');
    var show2 = localStorage.getItem('show-2');

    // Determines whether form-1 is displayed when page is opened
    if (show1 == 'true') {
        $('#form-1').show();
        $('#btn-1').hide();
    } else {
        $('#form-1').hide();
        $('#btn-1').show();   
    }

    // Determines whether form-2 is displayed when page is opened
    if (show2 == 'true') {
        $('#form-2').show();
        $('#btn-2').hide();
    } else {
        $('#form-2').hide();
        $('#btn-2').show(); 
    }
});

function openForm(num) {
    /*
     * Function for when one opens another query form
     */
    $("#btn-" + num).hide();
    localStorage.setItem('show-' + num, 'true'); //store state in localStorage
    $("#form-" + num).show();
}

function closeForm(num) {
    /*
     * Function for when one closes one of the query forms
     */
    $("#form-" + num).hide();
    localStorage.setItem('show-' + num, 'false'); //store state in localStorage
    $("#btn-" + num).show();
}
