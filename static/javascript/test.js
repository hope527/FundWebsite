$(function() {
  pre_time = ''
  $("#profit").mousemove(function() {
    start = document.URL;
    start = start.split('/')[4]
    start = start.split('%')[0]
    start = start.split('-')
    start = start[0] + '-' + start[1] + '-01'

    time = $("#profit, .bk-canvas-overlays")
    time = time.children().find('span').html()
    time = time.split('-')
    time = time[0] + '-' + time[1] + '-01'
    start = start + " " + time
    if (pre_time != time) {
      $.getJSON('/ajax_list/' + start, function(ret) {
        $("#mds").html(ret.div + ret.script);
      })
      pre_time = time;
    }
  })
});
