function verifyForm() {
    if ($("#first-name").val() == "") {
        $("#first-name").popover({content: "Please enter your first name"}).popover('show');
        return false;
    }
    if ($("#last-name").val() == "") {
        $("#last-name").popover({content: "Please enter your last name"}).popover('show');
        return false;
    }
    if ($("#mtuid").val() == "") {
        $("#mtuid").popover({content: "Please enter your MTU ID"}).popover('show');
        return false;
    }
    if ($("#password").val() != $("#confirm-password").val()) {
        $("#confirm-password").popover({content: "Passwords do not match!"}).popover('show');
        return false;
    }
    if ($("#email").val() == "") {
        $("#email").popover({content: "Please enter your email"}).popover('show');
        return false;
    }

    if ($("#email").val() != $("#confirm-email").val()) {
        $("#confirm-email").popover({content: "Emails do not match!"}).popover('show');
        return false;
    }
    return true;
}

function submitClicked() {
    if (verifyForm()) {
        $.ajax({
            method: "POST",
            url: "ajax/registersubmit", 
            data: $("#registerForm").serialize(),
            success: function(data) {
                window.location.replace('/');   
            },
            error: function(data) {
                $("#registration-failed").addClass("in").removeClass("hidden");
                if (data.responseText == "User exists") {
                    $("#error-message").html("There already exists a user with that username.");
                }
                else if (data.responseText == "Email exists") { 
                    $("#error-message").html("There is already an account associated with that email address.");
                }
            }
        });
    }
}
