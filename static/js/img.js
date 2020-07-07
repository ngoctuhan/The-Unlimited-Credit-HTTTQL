$(document).ready(function() {
    var stt = 0;
    startImg = $("img.image:first").attr("stt");
    endImg = $("img.image:last").attr("stt");
    $("img.image").each(function() {
        if ($(this).is(':visible'))
            stt = $(this).attr("stt");
    });
    $("#next").click(function() {
        if (stt == endImg) {
            stt = -1;
        }
        next = ++stt;
        $("img.image").hide();
        $("img.image").eq(next).show();
    });
    $("#prev").click(function() {
        if (stt == 0) {
            stt = endImg;
            prev = stt++;
        }
        prev = --stt;
        $("img.image").hide();
        $("img.image").eq(prev).show();
    });
    setInterval(function() {
        $("#next").click();
    }, 2000)
});