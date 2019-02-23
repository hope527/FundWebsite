$(function () {
  pre_time = ''
  $("#profit").mousemove(function () {
    start = document.URL;
    start = start.substr(start.lastIndexOf("test/") + 5, 8) + '01'
    time = $("#profit, .bk-canvas-overlays")
    time = time.children().find('span').html()
    time = time.substr(0, 8) + '01'
    start = start.concat(' ', time)
    if (pre_time != time) {
      $.getJSON('/ajax_list/' + start, function (ret) {
        $("#mds").html(ret.div + ret.script);
      })
      pre_time = time;
    }
  })
});
