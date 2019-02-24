$(function () {
  pre_end = ''
  $("#profit").mousemove(function () {
    start = document.URL;
    start = start.substr(start.lastIndexOf("test/") + 5, 8) + '01'
    end = $("#profit, .bk-canvas-overlays")
    end = end.children().find('span').html()
    end = end.substr(0, 8) + '01'
    start = start.concat(' ', end)
    if (pre_end != end) {
      $.getJSON('/ajax_list/' + start, function (ret) {
        $("#mds").html(ret.div + ret.script);
      })
      pre_end = end;
    }
  })
});
