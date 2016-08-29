import './libs/jquery-easing';
import './libs/retina';
import './libs/jquery-stellar';
import './libs/jquery-scrollto';
import './libs/jquery-countdown';
import './libs/owl-carousel';
import './libs/jquery-appear';
import './libs/jquery-vide';
import './libs/jquery-magnific-popup';
import './libs/jquery-flexslider';
import './libs/waypoint';
import './libs/jquery-ajaxchimp';
import './libs/register_form';
import './libs/jquery-validate';

const $ = window.$;
const jQuery = window.jQuery;

$(window).on('load', function() {

  $('.loader').delay(100).fadeOut();
  $('.animationload').delay(100).fadeOut('fast');
  $(window).stellar({});
});
$(window).on('scroll', function() {

  const b = $(window).scrollTop();
  if (b > 60) {
    $('.header .navbar.navbar-fixed-top').addClass('scroll');
  } else {
    $('.header .navbar.navbar-fixed-top').removeClass('scroll');
  }
});
$(document).ready(function() {

  $('.navbar-nav li a').on('click', function() {
    $('#navigation-menu').css('height', '1px').removeClass('in').addClass('collapse');
    $('#navigation-menu').removeClass('open');
  });
  $('#clock').countdown('2016/10/11 20:00:00', function(event) {
    $(this).html(event.strftime('' + '<div class="cbox-1 clearfix"><span class="cbox-1-digit">%D</span> <span class="cbox-1-txt">Days</span></div>' + '<div class="cbox-1 clearfix"><span class="cbox-1-digit">%H</span> <span class="cbox-1-txt">Hrs</span></div>' + '<div class="cbox-1 clearfix"><span class="cbox-1-digit">%M</span> <span class="cbox-1-txt">Min</span></div>' + '<div class="cbox-1 clearfix"><span class="cbox-1-digit">%S</span> <span class="cbox-1-txt">Sec</span></div>'));
  });
  $('.header a[href^="#"], .page-wrapper a.internal-link[href^="#"]').on('click', function(e) {
    e.preventDefault();
    const target = this.hash
          , $target = jQuery(target);
    $('html, body').stop().animate({
      'scrollTop': $target.offset().top - 60,
    }, 'slow', 'easeInSine', function() {
      window.location.hash = '1' + target;
    });
  });
  $.scrollUp = function(options) {
    const defaults = {
      scrollName: 'scrollUp',
      topDistance: 600,
      topSpeed: 800,
      animation: 'fade',
      animationInSpeed: 200,
      animationOutSpeed: 200,
      scrollText: '',
      scrollImg: false,
      activeOverlay: false,
    };
    const o = $.extend({}, defaults, options)
          , scrollId = '#' + o.scrollName;
    $('<a/>', {
      id: o.scrollName,
      href: '#top',
      title: o.scrollText,
    }).appendTo('body');
    if (!o.scrollImg) {
      $(scrollId).text(o.scrollText);
    }
    $(scrollId).css({
      display: 'none',
      position: 'fixed',
      'z-index': '2147483647',
    });
    if (o.activeOverlay) {
      $('body').append("<div id='" + o.scrollName + "-active'></div>");
      $(scrollId + '-active').css({
        'position': 'absolute',
        'top': o.topDistance + 'px',
        'width': '100%',
        'border-top': '1px dotted ' + o.activeOverlay,
        'z-index': '2147483647',
      });
    }
    $(window).scroll(function() {
      switch (o.animation) {
        case 'fade':
          $(($(window).scrollTop() > o.topDistance) ? $(scrollId).fadeIn(o.animationInSpeed) : $(scrollId).fadeOut(o.animationOutSpeed));
          break;
        case 'slide':
          $(($(window).scrollTop() > o.topDistance) ? $(scrollId).slideDown(o.animationInSpeed) : $(scrollId).slideUp(o.animationOutSpeed));
          break;
        default:
          $(($(window).scrollTop() > o.topDistance) ? $(scrollId).show(0) : $(scrollId).hide(0));
      }
    });
    $(scrollId).click(function(event) {
      $('html, body').animate({
        scrollTop: 0,
      }, o.topSpeed);
      event.preventDefault();
    });
  }
    ;
  $.scrollUp();
  $('.video-play').vide('images/video/video', {
    posterType: 'jpg',
  });
  $('.image-link').magnificPopup({
    type: 'image',
  });
  $('.gallery-item').magnificPopup({
    type: 'image',
    gallery: {
      enabled: true,
    },
  });
  $('.video-popup').magnificPopup({
    type: 'iframe',
    iframe: {
      patterns: {
        youtube: {
          index: 'youtube.com',
          src: 'https://www.youtube.com/embed/kuceVNBTJio',
        },
      },
    },
  });
  $('.flexslider').flexslider({
    animation: 'fade',
    controlNav: true,
    directionNav: false,
    slideshowSpeed: 6000,
    animationSpeed: 2000,
    start: function(slider) {
      $('body').removeClass('loading');
    },
  });
  $('#blog-posts-holder').owlCarousel({
    autoPlay: true,
    slideSpeed: 800,
    items: 3,
    itemsDesktop: [1199, 2],
    itemsDesktopSmall: [991, 2],
    itemsTablet: [768, 1],
    itemsMobile: [480, 1],
    navigation: false,
    pagination: true,
    navigationText: false,
  });
  $('#register-form').validate({
    rules: {
      name: {
        required: true,
        minlength: 1,
        maxlength: 16,
      },
      email: {
        required: true,
        email: true,
      },
      ticket: {
        required: true,
      },
    },
    messages: {
      name: {
        required: 'Please enter no more than (1) characters',
      },
      email: {
        required: 'We need your email address to contact you',
        email: 'Your email address must be in the format of name@domain.com',
      },
      ticket: {
        required: 'This field is required',
      },
    },
  });
  $('.newsletter-form').ajaxChimp({
    language: 'cm',
    url: 'http://dsathemes.us3.list-manage.com/subscribe/post?u=af1a6c0b23340d7b339c085b4&id=344a494a6e',
  });
  $.ajaxChimp.translations.cm = {
    'submit': 'Submitting...',
    0: 'We have sent you a confirmation email',
    1: 'Please enter a value',
    2: 'An email address must contain a single @',
    3: 'The domain portion of the email address is invalid (the portion after the @: )',
    4: 'The username portion of the email address is invalid (the portion before the @: )',
    5: 'This email address looks fake or invalid. Please enter a real email address',
  };
});
