$(function () {

  var response_data;
  $.getJSON($("#url").text(), function (ret) {
    $(".loading").remove();
    response_data = ret;
    $("#sharpe_ratio").text("夏普指標: " + response_data.sharpe_ratio);
    $("#std").text("標準差: " + response_data.std);
    $("#beta").text("beta: " + response_data.beta);
    $("#treynor_ratio").text("Treynor指數: " + response_data.treynor_ratio);
    $("#money").text("期末金額: " + response_data.money);
    $("#profit").text("期末報酬率(%): " + response_data.profit + "%");
    $("#mean_similarity").text("平均距離: " + response_data.mean_similarity);
    $("#profit_img").html(response_data['profit_img'].div + response_data['profit_img'].script);
    $("#mds").html(response_data[response_data["start"]].div + response_data[response_data["start"]].script);
  })

  var temp = ''
  $("#profit_img").mousemove(function () {
    mds_img_idx = $("#profit_img, .bk-canvas-overlays")
    mds_img_idx = mds_img_idx.children().find('span').html()
    mds_img_idx = mds_img_idx.substr(0, 7)
    if (temp != mds_img_idx) {
      $("#mds").html(response_data[mds_img_idx].div + response_data[mds_img_idx].script);
      temp = mds_img_idx;
    }
  })
});
