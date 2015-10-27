///////////////////////////////
// One page Smooth Scrolling
///////////////////////////////






$(document).ready(function() {
    var offset = 75;
    var first_level = $('.firstLevel');

    $('.firstLevel').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
            $('html,body').animate({
                scrollTop: target.offset().top - offset
            }, 700);
            return false;
        }    

    first_level.removeClass('active');
    this.addClass('active');

    }
});

    // static navigationbar
    var changeStyle = $('#navigation-bar');
    var portfolio = $('#portfolio_link');
    var contact = $('#contact_link');
    var home = $('#home_link');
    var team = $('#team_link');

    function scroll() {
        if ($(window).scrollTop() < 635 -offset) {
            first_level.removeClass('active');
            home.addClass('active');
        } else if ($(window).scrollTop() < 1701-offset) {
            first_level.removeClass('active');
            portfolio.addClass('active');
        } else if ($(window).scrollTop() < 2661-offset) {
            first_level.removeClass('active');
            team.addClass('active');
        } else  {
            first_level.removeClass('active');
            contact.addClass('active');
        }
    }

    document.onscroll = scroll;

    $('.testimonial-owl').owlCarousel({
        items: 1
    });

    $('.add-owl').owlCarousel({
        items: 4,
        nav: true,
        navText: false,
        dots: false,
        loop: true
    });

    $('.twitter-owl').owlCarousel({
        items: 1,
        nav: true,
        navText: false,
        dots: false,
        loop: true
    });

});