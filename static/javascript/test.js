$(function() {
  $("#mds_1").mouseover(function() {
    $.getJSON('/ajax_list/1', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_2").mouseover(function() {
    $.getJSON('/ajax_list/2', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_3").mouseover(function() {
    $.getJSON('/ajax_list/3', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_4").mouseover(function() {
    $.getJSON('/ajax_list/4', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_5").mouseover(function() {
    $.getJSON('/ajax_list/5', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_6").mouseover(function() {
    $.getJSON('/ajax_list/6', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_7").mouseover(function() {
    $.getJSON('/ajax_list/7', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_8").mouseover(function() {
    $.getJSON('/ajax_list/8', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_9").mouseover(function() {
    $.getJSON('/ajax_list/9', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_10").mouseover(function() {
    $.getJSON('/ajax_list/10', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_11").mouseover(function() {
    $.getJSON('/ajax_list/11', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
  $("#mds_12").mouseover(function() {
    $.getJSON('/ajax_list/12', function(ret) {
      $("#mds").html(ret.div + ret.script);
    })
  })
});
