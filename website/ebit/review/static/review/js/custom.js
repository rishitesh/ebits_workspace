  wow = new WOW({
    boxClass:     'wow',      // default
    animateClass: 'animate__animated', // default
    offset:       0,          // default
    mobile:       true,       // default
    live:         true        // default
  })
  wow.init();

 $(function() {
    $('.mousey').click(function() {
      if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
          var scrolltop =  target.offset().top; //(($("#header-sticky").hasClass("sticky-menu")) ? target.offset().top - 84 : target.offset().top - 190);
          $('html, body').animate({
            scrollTop: scrolltop
          }, 800);
          return false;
        }
      }
 
    });

    $(document).ready(function(){
      // $('.details-crtique-slider_inner').slick({
      //   dots: false,
      //   infinite: false,
      //   slidesToShow: 4,
      //   slidesToScroll: 1
      // });

      $('.details-trailer-player').on('click',function(e){
        e.preventDefault();

        $iframe = $(this).data('frame');

        $('#details-video-target').empty().html($iframe);
        $('.details-hero-video__wrap').show();
        $("html, body").animate({ scrollTop: 0 });
      });

      console.log($('.home-top-movie-preview-list'));

      $('.home-top-movie-preview-list').slick({
        dots: false,
        infinite: false,
        slidesToShow: 3.2,
        slidesToScroll: 1,
        arrows: true, 
      });

      $home_preview_slider = $('.home-preview-slider__inner')



      console.log($home_preview_slider);

      $home_preview_slider.on('init', function(event, currentSlide){
        // alert();
        console.log('test');
        window.generateGraph1();
      }); 

      $home_preview_slider.slick({
        dots: false,
        infinite: false,
        slidesToShow: 1.05,
        slidesToScroll: 1,
        arrows: true, 
      });
      
      // On before slide change
      // $('.home-preview-slider__inner').on('afterChange', function(event, currentSlide){
      //   console.log(window.myChart1);
      //   setTimeout(() => document.getElementsByClassName("h-myChart-1")[0].reflow(), 0)
      //   ;
      // });

      $('.best-in-story-slider__inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: true, 
      });

      $('.mood-slider-top__inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 7.5,
        slidesToScroll: 1,
        arrows: true, 
        focusOnSelect: true,
      });

      $('.mood-slider-main__inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 5,
        slidesToScroll: 1,
        arrows: true, 
        focusOnSelect: true,
      });

      // $('.ebit-treasure-slider__inner').slick({
      //   speed: 1000,
      //   arrows: true,
      //   dots: false,
      //   focusOnSelect: true,
      //   prevArrow: '<button> prev</button>',
      //   nextArrow: '<button> next</button>',
      //   infinite: true,
      //   centerMode: true,
      //   slidesPerRow: 1,
      //   slidesToShow: 1,
      //   slidesToScroll: 1,
      //   centerPadding: '0',
      //   swipe: true,
      //   customPaging: function(slider, i) {
      //     return '';
      //   },
      //   /*infinite: false,*/
      // });

      var rev = $('.ebit-treasure-slider__inner');
      rev.on('init', function(event, slick, currentSlide) {
        var
          cur = $(slick.$slides[slick.currentSlide]),
          next = cur.next(),
          next2 = cur.next().next(),
          prev = cur.prev(),
          prev2 = cur.prev().prev();
        prev.addClass('slick-sprev');
        next.addClass('slick-snext');  
        prev2.addClass('slick-sprev2');
        next2.addClass('slick-snext2');  
        cur.removeClass('slick-snext').removeClass('slick-sprev').removeClass('slick-snext2').removeClass('slick-sprev2');
        slick.$prev = prev;
        slick.$next = next;
      }).on('beforeChange', function(event, slick, currentSlide, nextSlide) {
        console.log('beforeChange');
        var
          cur = $(slick.$slides[nextSlide]);
        console.log(slick.$prev, slick.$next);
        slick.$prev.removeClass('slick-sprev');
        slick.$next.removeClass('slick-snext');
        slick.$prev.prev().removeClass('slick-sprev2');
        slick.$next.next().removeClass('slick-snext2');
        next = cur.next(),  
        prev = cur.prev();
        //prev2.prev().prev();
        //next2.next().next();
        prev.addClass('slick-sprev');
        next.addClass('slick-snext');
        prev.prev().addClass('slick-sprev2');
        next.next().addClass('slick-snext2');
        slick.$prev = prev;
        slick.$next = next;
        cur.removeClass('slick-next').removeClass('slick-sprev').removeClass('slick-next2').removeClass('slick-sprev2');
      });

      rev.slick({
        speed: 1000,
        arrows: false,
        dots: false,
        focusOnSelect: true,
        prevArrow: '<button> prev</button>',
        nextArrow: '<button> next</button>',
        infinite: true,
        centerMode: true,
        slidesPerRow: 1,
        slidesToShow: 1,
        slidesToScroll: 1,
        centerPadding: '0',
        swipe: true,
        customPaging: function(slider, i) {
          return '';
        },
        /*infinite: false,*/
      });

      $('.home-ebit-stream-slider_inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 6.5,
        slidesToScroll: 1,
        arrows: true, 
        focusOnSelect: true,
      });

      $('.home-upcoming-movies-slider__inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 3.5,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true, 
        focusOnSelect: true,
      });

      $('.home-spotlight-slider__inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        centerMode: true,
        arrows: false, 
        focusOnSelect: true,
      });

      $('.home-blog-explorer-slider__inner').slick({
        dots: false,
        infinite: false,
        slidesToShow: 3.5,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true, 
        focusOnSelect: true,
      });

    })
 });