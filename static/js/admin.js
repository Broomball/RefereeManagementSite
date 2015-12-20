$(document).ready(function(){

    var simpleRangeCalendar = $("#default-calendar").rangeCalendar({
        maxRangeWidth:1,
        changeRangeCallback: changed,
        start: "+1",
        theme: "dark-theme"
    });

    function changed(target, range) {
        console.log(range);
        var date = range.start.split(" ");
        var month = date[1];
        var day = date[2];
        var year = date[3];
        switch(month) {
            case "Jan":
                month = '01';
                break;
            case "Feb":
                month = '02';
                break;
            case "Mar":
                month = '03';
                break;
            case "Apr":
                month = '04';
                break;
            case "May":
                month = '05';
                break;
            case "Jun":
                month = '06';
                break;
            case "Jul":
                month = '07';
                break;
            case "Aug":
                month = '08';
                break;
            case "Sep":
                month = '09';
                break;
            case "Oct":
                month = '10';
                break;
            case "Nov":
                month = '11';
                break;
            case "Dec":
                month = '12';
                break;
        }
        var dateparam = day+month+year;
        $.get("ajax/dateinfo", {date: dateparam}, function(data) {
                $("#dayinfo").html(data);
        });
    }

    $('#loginmodal').on('shown.bs.modal', function () {
      $('#myInput').focus()
    })
});
