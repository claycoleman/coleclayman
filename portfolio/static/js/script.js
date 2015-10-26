///////////////////////////////
// One page Smooth Scrolling
///////////////////////////////






$(document).ready(function() {
    var offset = 75;

    $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
            $('html,body').animate({
                scrollTop: target.offset().top - offset
            }, 700);
            return false;
        }
    }
});

    // static navigationbar
    var changeStyle = $('#navigation-bar');
    var portfolio = $('#portfolio_link')
    var contact = $('#contact_link')
    var home = $('#home_link')
    var team = $('#team_link')

    function scroll() {
        if ($(window).scrollTop() < 635 -offset) {
            home.addClass('active');
            portfolio.removeClass('active');
            contact.removeClass('active');
            team.removeClass('active');
        } else if ($(window).scrollTop() < 1701-offset) {
            home.removeClass('active');
            portfolio.addClass('active');
            contact.removeClass('active');
            team.removeClass('active');
        } else if ($(window).scrollTop() < 2861-offset) {
            home.removeClass('active');
            portfolio.removeClass('active');
            team.addClass('active');
            contact.removeClass('active');
        } else  {
            home.removeClass('active');
            portfolio.removeClass('active');
            team.removeClass('active');
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