function logout() {
    $.post("ajax/logout", function(data){
        location.reload();
    });
}