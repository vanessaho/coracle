$(function() {
    var $form = $('#form');
    $('button').click(function() {
        var user = $('#txtUsername').val();
        var pass = $('#txtPassword').val();
        $.ajax({
            url: '/signupuser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $form.append('<p>' + response + '</p>');
                $form.append('<p>' + response.andy + '</p>');
                console.log(response.andy);
                console.log(response.status);
                console.log(response.user);
                console.log(response.pass);
            },
            error: function(error) {
                console.log("error");
                console.log(error);
            }
        });
    });
});