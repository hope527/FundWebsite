$(function () {

  var response_data;
  $.getJSON($("#url").text(), function (ret) {
    $(".loading").remove();
    response_data = ret;
    $("#sharpe_ratio").text("夏普指標: " + response_data.sharpe_ratio);
    $("#market_sharpe").text("市場夏普指標: " + response_data.market_sharpe);
    $("#std").text("標準差: " + response_data.std);
    $("#market_std").text("市場標準差: " + response_data.market_std);
    $("#beta").text("beta: " + response_data.beta);
    $("#treynor_ratio").text("Treynor指數: " + response_data.treynor_ratio);
    $("#money").text("期末金額: " + response_data.money);
    $("#profit").text("期末報酬率(%): " + response_data.profit + "%");
    $("#market_revenue").text("市場期末報酬率(%): " + response_data.market_revenue + "%");
    // $("#simulation").text("預估五年後報酬率(%): " + response_data.simulation + "%");
    $("#mean_similarity").text("平均距離: " + response_data.mean_similarity);
    $("#profit_img").html(response_data['profit_img'].div + response_data['profit_img'].script);
    $("#distance").html(response_data['distance'].div + response_data['distance'].script);
    $("#mds").html(response_data[response_data["start"]].div + response_data[response_data["start"]].script);
    $("#table").show()
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
