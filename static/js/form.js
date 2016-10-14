function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
  // test that a given url is a same-origin URL
  // url could be relative or scheme relative or absolute
  var host = document.location.host; // host + port
  var protocol = document.location.protocol;
  var sr_origin = '//' + host;
  var origin = protocol + sr_origin;
  // Allow absolute or scheme relative URLs to same origin
  return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
      // Send the token to same-origin, relative URLs only.
      // Send the token only if the method warrants CSRF protection
      // Using the CSRFToken value acquired earlier
      var csrftoken = $.cookie('csrftoken');
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});



$(document).ready(function() {
  $('#comment_submit_btn').click(function(evt) {
    if ($("#comment_form").valid()) {
      console.log("Fired2");
      $('#comment_submit_btn').attr('disabled', 'disabled');
      $(".loader").show();
      var data = new FormData($('#comment_form').get(0));

      var root_url = window.location.origin;
      var post_url = root_url + '/comment/'

      $.ajax({
        url: post_url,
        type: "POST",
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
          console.log("Successfull");
          $(".loader").hide();
          $("#comment_form").get(0).reset()
          $('#comment_submit_btn').removeAttr('disabled');

        },
        error: function(data) {
          console.log("Error Happend");
          $(".loader").hide();
          $("#comment_form").get(0).reset();
          $('#comment_submit_btn').removeAttr('disabled');
        }
      });
      return false;
    }
  });
});
