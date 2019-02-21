$(function() {
  pre_time = ''
  $("#profit").mousemove(function() {
    time = $("#profit, .bk-canvas-overlays")
    time = time.children().find('span').html()
    time = time.split('-')[1]
    if (pre_time != time) {
      $.getJSON('/ajax_list/' + time, function(ret) {
        $("#mds").html(ret.div + ret.script);
      })
      pre_time = time;
    }
  })
});
