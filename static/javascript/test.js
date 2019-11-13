$(function () {
    $("#form").validate();

    $("#comprehensive").click(function () {
        $("#risk_value").hide();
        $("#comprehensive_value").show();
    })

    $("#risk").click(function () {
        $("#comprehensive_value").hide();
        $("#risk_value").show();
    })

    $("#single").click(function () {
        $("#strategy2").hide();
        $("#strategy1").show();
    })

    $("#regular").click(function () {
        $("#strategy1").hide();
        $("#strategy2").show();
    })
});
