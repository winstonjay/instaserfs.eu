"use strict";

var player, playerImage, bot, botImage, bot_thoughts;
var board = [
    [null,null,null],
    [null,null,null],
    [null,null,null]
]; 

var O = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
            +'<circle class="a" cx="50" cy="50" r="42" />'
        +'</svg>';

var X = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
            +'<line class="a" x1="7.5" y1="7.5" x2="91.58" y2="91.58"/>'
            +'<line class="a b" x1="7.92" y1="92" x2="92" y2="7.92"/>'
        +'</svg>';

var get_svg = (a) => a == "X" ? X : O;

var thoughts_set = true;

var BotThoughts = function()
{
    this.show = function(thoughts)
    {
        $('ul.thoughts').empty();
        $(thoughts).each(function(i, thought) { 
            setTimeout(() => { 
                $('ul.thoughts').append('<li>'+thought+'.</li>');
            }, i * 100); 
        });
    }

    this.toggle = function()
    {
        if (thoughts_set)
        {
            thoughts_set = false;
            $('.bot_thoughts_mode').text("Enable Bot Thoughts");
        }
        else
        {
            thoughts_set = true;
            $('.bot_thoughts_mode').text("Disable Bot Thoughts");
        }
    }

    this.hide = function()
    {
        thoughts_set = false;
        $('.thought-info').removeClass('active');
        $('.bot_thoughts_mode').text("Enable Bot Thoughts");
    }
}

var bot_thoughts = new BotThoughts();

function newSVG(tag, attrs) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    if (attrs)
    {
        for (var k in attrs)
            el.setAttribute(k, attrs[k]);
    }
    return el;
}

Array.prototype.allValuesSame = function() 
{
    for(var i = 1; i < this.length; i++)
    {
        if((this[i] != this[0]) || (this[i] === null))
            return false;
    }
    return true;
}

function generateBoard(board) 
{
    var $row, $square;
    for (var i = 0; i < 3; i++) 
    {
        $row = $("<div>", {"class": "row"});
        for (var j = 0; j < 3; j++) 
        {
            $square = $("<div>", {
                "class": "square", 
                "data-position": "[" + i + "," + j + "]" 
            });
            $row.append($square);
        }
        $(board).append($row);
    }
}

function generateOptions()
{
    if (!$('.option').hasClass('setup')) {
        $('.init_naught').append(O);
        $('.init_cross').append(X);
        $('.option').addClass('setup');
    }
}

function enter_game() {
    $('.welcome').fadeOut();
    setTimeout(() => { 
        $('.options').fadeIn(); 
        generateOptions(); 
    }, 400);
}  


/* winner svg co-ordinates */
/*
    rows 
         y1="50" x2="300" y2="50"
         y1="150" x2="300" y2="150"
         y1="250" x2="300" y2="250"
    cols
         x1="50" y2="300" x2="50"
         x1="150" y2="300" x2="150"
         x1="250" y2="300" x2="250"
    diagonals
         x1="7.5" y1="7.5"  x2="292" y2="292"
         x1="7.5" y1="292"  x2="292" y2="7.5"
    diagonal line length 
         ~ 402.34
*/

function draw_win_line(type, n)
{
    var line, pos = (100*n) + 50;
    var win_SVG = newSVG("svg", { 
        class:"abs", width:"300", height:"300", viewBox:"0 0 300 300" 
    });
    $('.board').prepend(win_SVG);
    pos = pos == 50 ? pos-2 : pos;
    if (type == "horizontal")
    {   
        line = newSVG("line", { class:"a", y1:pos, x2:"300", y2:pos });
    }
    else if (type == "vertical")
    {
        line = newSVG("line", { class:"a", x1:pos, y2:"300", x2:pos });
    }
    else if (type == "diagonal")
    {
        if (n == 1)
            line = newSVG("line", { 
                class:"a", x1:"7.5", y1:"7.5",  x2:"292", y2:"292" 
            });
        if (n == 2)
            line = newSVG("line", { 
                class:"a", x1:"7.5", y1:"292",  x2:"292", y2:"7.5" 
            });
        $(line).addClass('c');
    }
    $('.abs').append(line);
}

function display_win(winner)
{
    var x = [], y = [], xy = [], yx = [];
    var size = board.length - 1;

    for (var i = 0; i <= size; i++)
    {
        x.length = 0; 
        y.length = 0;
        for (var j = 0; j <= size; j++)
        {
            x.push(board[i][j]); 
            y.push(board[j][i]);
        }
        if (x.allValuesSame()) 
            draw_win_line("horizontal", i); 

        if (y.allValuesSame()) 
            draw_win_line("vertical", i); 

        xy.push(board[i][i]); 
        yx.push(board[size-i][i]);
    }
    if (xy.allValuesSame()) 
        draw_win_line("diagonal", 1); 

    if (yx.allValuesSame()) 
        draw_win_line("diagonal", 2); 
}

function pickPlayer(choice) 
{
    player = choice;
    bot = choice == "X" ? "O" : "X";

    playerImage = get_svg(player);
    botImage = get_svg(bot);
}

function start_game()
{
    $('.board').addClass('frozen');
    pickPlayer($(this).data('side'));
    $('.options').fadeOut();
    setTimeout(() => { 
        $('.board').addClass('active'); 
        if (thoughts_set)
            $('.thought-info').addClass('active');

        if (Math.round(Math.random()))
            makeMove();
        else
            $('.board').removeClass('frozen');

    }, 400);
}

function botMove(image, position)
{
    var sqr = '.square[data-position="['+ position +']"]'; 
    if (!$(sqr).hasClass('ocupied')) 
    {
        setTimeout(() => {
            $(sqr).addClass('ocupied');
            $(sqr).html(image);
        }, 500);
    }
}

function increment_counter(winner, count_cls=".draws")
{
    if (winner == bot)
        count_cls = ".computer";
    else if (winner == player)
        count_cls = ".humans";

    console.log(count_cls+": "+$(count_cls).text())
    $(count_cls).text(parseInt($(count_cls).text(), 10)+1)
}

function human_move() 
{
    if (!$(this).hasClass('ocupied') && !$('.board').hasClass('frozen'))
    {
        $('.board').addClass('frozen');
        $(this).html(playerImage);
        $(this).addClass('ocupied');

        var move = $(this).data('position');
        board[move[0]][move[1]] = player;

        makeMove();
    }
}

function makeMove() 
{
    // if ([].concat.apply([], board).includes(null) === false) 
    // {
    //     show_result(null);
    //     return;
    // }
    $.ajax({
        url: 'computer_move/',
        data: JSON.stringify({ 
            gameBoard: board,
            botPlayer: bot
        }, null),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success: function(response) 
        {
            if (response.new_move !== null) 
            {
                var delay = 0;
                if (thoughts_set)
                {
                    bot_thoughts.show(response.thoughts);
                    delay = 100 * response.thoughts.length - 100;
                }
                setTimeout(() => {
                    board = response.new_board;
                    botMove(botImage, response.new_move);
                }, delay);
            }

            if (!response.finished)
                $('.board').removeClass('frozen');
            else
            {
                setTimeout(() => { show_result(response.winner); }, delay);
            }
        },
        error: function(error) 
        {
            console.log("There was a crazy error");
        }
    });
}

function game_end_message(winner)
{
    var message;
    var messages = [
        "Good game!",
        "Well done, good effort.",
        "Pleasure playing with you.",
        "Better luck next time."
    ];
    if (winner !== null) 
        message = "I win.";
    else
        message = "We drew."
    message += " ";
    message += messages[Math.floor(Math.random()*messages.length)];
    return '<li>'+message+'</li>'
}

function show_result(winner)
{
    var final_thought = game_end_message(winner);
    if (winner !== null) 
    {
        var win_image = get_svg(winner);
        setTimeout(() => {
            display_win(winner)
            setTimeout(() => {
                $('ul.thoughts').empty();
                $('.board').removeClass('active');
                $('.winning-player').append(win_image);
                $('ul.thoughts').append(final_thought);
                $('.game-result').append("Winner!");
                $('.result').addClass('active');
                increment_counter(winner);
            }, 1000);
        }, 750);
    }
    else 
    {
        setTimeout(() => {
            $('ul.thoughts').empty();
            $('.board').removeClass('active');
            $('.winning-player').append(X);
            $('.winning-player').append(O);
            $('ul.thoughts').append(final_thought);
            $('.game-result').append("Draw!");
            $('.result').addClass('active'); 
            increment_counter(winner);
        }, 1000);
    }
}

function reset_game()
{
    $('.result').removeClass('active'); 
    $('.thought-info').removeClass('active');
    player = null;
    playerImage = null; 
    bot = null;
    botImage = null;
    board = [
        [null,null,null],
        [null,null,null],
        [null,null,null]
    ]; 
    $('.board').removeClass('frozen');
    $('.square').removeClass('ocupied');
    $('ul.thoughts').empty();
    $('.winning-player').empty();
    $('.game-result').empty();
    $('.square').empty();
    $('.abs').remove();
    enter_game();
}

$(function() { function getCookie(name) {var cookieValue = null; if (document.cookie && document.cookie != '') {var cookies = document.cookie.split(';'); for (var i = 0; i < cookies.length; i++) {var cookie = jQuery.trim(cookies[i]); /* Does this cookie string begin with the name we want? */ if (cookie.substring(0, name.length + 1) == (name + '=')) {cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break; } } } return cookieValue; } var csrftoken = getCookie('csrftoken'); /* The functions below will create a header with csrftoken */ function csrfSafeMethod(method) {/* these HTTP methods do not require CSRF protection */ return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); } function sameOrigin(url) {/* test that a given url is a same-origin URL url could be relative or scheme relative or absolute */ var host = document.location.host; /* host + port */ var protocol = document.location.protocol; var sr_origin = '//' + host; var origin = protocol + sr_origin; /* Allow absolute or scheme relative URLs to same origin */ return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || /* or any other URL that isn't scheme relative or absolute i.e relative. */ !(/^(\/\/|http:|https:).*/.test(url)); } $.ajaxSetup({beforeSend: function(xhr, settings) {if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {/* Send the token to same-origin, relative URLs only. Send the token only if the method warrants CSRF protection Using the CSRFToken value acquired earlier */ xhr.setRequestHeader("X-CSRFToken", csrftoken); } } }); });



$(document).ready(function () 
{
    generateBoard('.board');

    /* init all button listeners */
    $('.entry-btn').on('click', enter_game);
    $('.square').on('click', human_move);
    $('.option').on('click', start_game);
    $('.reset').on('click', reset_game);
    $('.bot_thoughts_mode').on('click', bot_thoughts.toggle)
    $('.close-thoughts').on('click', bot_thoughts.hide)
})
