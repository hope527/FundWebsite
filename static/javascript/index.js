$(function () {
    var page = 1
    var change_page = function(){
      $.getJSON("/index/p=" + page, function (ret) {
        var html = ""
        $.each(ret, function (i, item) {
            html += '<tr>\
            <td><a href="' + item.url + '">' + item.fund_id + "</td>\
            <td>" + item.manager_fee + "</td>\
            <td>" + item.custody_fee + "</td>\
            <td>" + item.sales_fee + "</td>\
            <td>" + item.investment_target + "</td>\
            <td>" + item.area + "</td>\
            </tr>"
        });
        $("#items").html(html);
    });


    }
    $("#next_page").click(function () {
        page += 1
        change_page();
    });
    $("#go").click(function () {
      page = $("#page_num").val()
      page = parseInt(page)
      change_page();
    });

    $("#prev_page").click(function () {
        if(page>1){
          page -= 1
        change_page();
      }else if (page<=1) {
          page = 1
        }
    });


    $(".alert").hide();//警告訊息
    var msg = "查無資料！";
    // alert(msg);
    $("#search").click(function () {

      var column = $("#column").val()
      var keyword = $("#keyword").val()
      //if (function (ret)!= null){
      $.getJSON("/index/c=" + column + "&key=" + keyword, function (ret) {
        var html = ""
        $.each(ret, function (i, item) {
            html += '<tr>\
            <td><a href="' + item.url + '">' + item.fund_id + "</td>\
            <td>" + item.manager_fee + "</td>\
            <td>" + item.custody_fee + "</td>\
            <td>" + item.sales_fee + "</td>\
            <td>" + item.investment_target + "</td>\
            <td>" + item.area + "</td>\
            </tr>"
        });
        $("#items").html(html);
    });
  //}else {alert(msg);}
  });
});

// <td>" + item.chinese_name + "</td>\
// <td>" + item.english_name + "</td>\
// <td>" + item.isin_code + "</td>\
// <td>" + item.entry_day + "</td>\
