// JavaScript to slide between forms
$('#signin-btn').on('click', function () {
    $('#form-container').css('transform', 'translateX(0%)');
});

$('#signup-btn').on('click', function () {
    $('#form-container').css('transform', 'translateX(-50%)');
});

$('#show-signup').on('click', function (e) {
    e.preventDefault();
    $('#form-container').css('transform', 'translateX(-50%)');
});

$('#show-signin').on('click', function (e) {
    e.preventDefault();
    $('#form-container').css('transform', 'translateX(0%)');
});