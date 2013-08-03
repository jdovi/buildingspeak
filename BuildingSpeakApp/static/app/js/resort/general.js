/*-----------------------------------------------------------------------------------*/
/* GENERAL SCRIPTS */
/*-----------------------------------------------------------------------------------*/
jQuery(document).ready(function($){

	// Table alt row styling
	jQuery( '.entry table tr:odd' ).addClass( 'alt-table-row' );
	
	// FitVids - Responsive Videos
	jQuery( '.post, .widget, .panel, .page, #featured-slider .slide-media, .entry' ).fitVids();
	
	// Add class to parent menu items with JS until WP does this natively
	jQuery("ul.sub-menu, ul.children").parents('li').addClass('parent');
	
	// Responsive Navigation (switch top drop down for select)
	jQuery('ul#top-nav').mobileMenu({
	    switchWidth: 769,                   //width (in px to switch at)
	    topOptionText: 'Select a page',     //first option text
	    indentString: '&nbsp;&nbsp;&nbsp;'  //string for indenting nested items
	});
  	
  	// Show/hide the main navigation
  	jQuery('.nav-toggle').click(function() {
	  jQuery('#navigation').slideToggle('fast', function() {
	  	return false;
	    // Animation complete.
	  });
	});
	
	// Stop the navigation link moving to the anchor (Still need the anchor for semantic markup)
	jQuery('.nav-toggle a').click(function(e) {
        e.preventDefault();
    });

	if( !/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) { 
	    if (jQuery(window).width() > 767) {

	    	var pos = $('#fixed-header').offset().top;
	    	var height = $('#fixed-header').outerHeight();

	    	var wpadmin = $('#wpadminbar').outerHeight();
	    	if ( ! wpadmin ) { wpadmin = 0; }

	    	var topmenu = $('#top').outerHeight();
	    	if ( ! topmenu ) { topmenu = 0; }

	    	$(window).scroll(function() {
	    		var top = $(document).scrollTop();

				if ( top > pos - wpadmin - topmenu -  10 ){
					$('#fixed-header').addClass('fixed').css('top', wpadmin + topmenu);
					$('#header').css('height', height );
				} else {
					$('#fixed-header').removeAttr('style').removeClass('fixed');
					$('#header').removeAttr('style');
				}

	    	});
	    }
	}
  	
});