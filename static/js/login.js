function submitLogin() {
    $.ajax({
        method: "POST",
        url: "ajax/login",
        data: $("#loginForm").serialize(), 
        success: function (data) {
            location.reload(true);
        },
        error: function (data) {
            $("#login-failed").addClass("in").removeClass("hidden");
        }
    }); 
}