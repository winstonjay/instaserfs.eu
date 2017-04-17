$(function() {/* This function gets cookie with a given name */ function getCookie(name) {var cookieValue = null; if (document.cookie && document.cookie != '') {var cookies = document.cookie.split(';'); for (var i = 0; i < cookies.length; i++) {var cookie = jQuery.trim(cookies[i]); /* Does this cookie string begin with the name we want? */ if (cookie.substring(0, name.length + 1) == (name + '=')) {cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break; } } } return cookieValue; } var csrftoken = getCookie('csrftoken'); /* The functions below will create a header with csrftoken */ function csrfSafeMethod(method) {/* these HTTP methods do not require CSRF protection */ return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); } function sameOrigin(url) {/* test that a given url is a same-origin URL url could be relative or scheme relative or absolute */ var host = document.location.host; /* host + port */ var protocol = document.location.protocol; var sr_origin = '//' + host; var origin = protocol + sr_origin; /* Allow absolute or scheme relative URLs to same origin */ return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || /* or any other URL that isn't scheme relative or absolute i.e relative. */ !(/^(\/\/|http:|https:).*/.test(url)); } $.ajaxSetup({beforeSend: function(xhr, settings) {if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {/* Send the token to same-origin, relative URLs only. Send the token only if the method warrants CSRF protection Using the CSRFToken value acquired earlier */ xhr.setRequestHeader("X-CSRFToken", csrftoken); } } }); });

// AJAX for posting
function create_post() {

    var message_div = document.createElement('div');
    message_div.className = "message user-message";
    var message = $('#user_message').val()
    $(message_div).text(message);
    $(".messages").append(message_div);

    var post_url = "/demo/eeb4ff8a206697973ce757_create_post_b5b3c6d7aeb8845decf26e85117f/"
    //console.log("create post is working!") // sanity check
    $.ajax({
        url : post_url, // the endpoint
        type : "POST", // http method
        data : { the_post : $('#user_message').val() }, // data sent with the post request


        // handle a successful response
         success : function(json) {

            $('#user_message').val(''); // remove the value from the input
                 // log the returned json to the console

            // var replyTime = Math.floor((Math.random() * 1000) + 1000);

            setTimeout(function () {
                var reply_div = document.createElement('div');
                reply_div.className = "message bot-message";
                $(reply_div).text(json.message_reply);
                $(".messages").append(reply_div);
                $('.messages-inner-container').scrollTop($('.messages-inner-container')[0].scrollHeight);
                message_div = null;
                reply_div = null;
            }, 0);


            $('#inner').text(JSON.stringify(json, null, 2));

            highlight_text();

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


function highlight_text() {
    str = $( "#inner" ).text();
    str = str.replace(/(\"(.*?)+\"+)/g,"<span class='quotes'>$1</span>");
    $( "#inner" ).html( str );
}

$(document).ready( function() {

    highlight_text();

    $('.messages-inner-container').scrollTop($('.messages-inner-container')[0].scrollHeight);

    $('#user_message').keypress(function (event) 
    {
        if (event.which == 13) {
            event.preventDefault();
            $('form.message-form').submit(); 
        }
    });

    $('.links').click(function () {
        var page_content = '#'+$(this).data("item");
        $('.content').removeClass('active');
        $(page_content).addClass('active');
    }); 

    $(".fake-icon").click(function () {
        if( $('.inner-utils').hasClass('open') ) {
            $('.inner-utils').removeClass('open');
        } else {
            $('.inner-utils').addClass('open');
        }
    });

    $('#message-form').on('submit', function (event) {
        event.preventDefault();
        //console.log("form submitted!")  // sanity check
        create_post();
        $('.messages-inner-container').scrollTop($('.messages-inner-container')[0].scrollHeight);
    });
});
