(function($) {
  // add you javascript here

  var NewTabLink = function(link) {
    this.link = link;
    this.setup();
  }

  NewTabLink.prototype = {
    setup: function() {
      var imgNode = document.createElement('img');
      imgNode.classList.add('logo');
      imgNode.setAttribute('src', "/static/images/new_tab_icon.png");
      imgNode.setAttribute('alt', "");
      this.link.appendChild(imgNode);
      this.link.setAttribute('aria-label', this.link.innerText + ', opens in new tab');
    }
  }

  var NavBar = function() {
    this.setup();
  }

  NavBar.prototype = {
    setup: function() {
      this.navToggleBtn = $('.navbar-toggle');
      this.navList = $('#top-navbar');
      this.startWatcher();
    },

    startWatcher: function() {
      var that = this;
      this.navToggleBtn.click(function() {
        console.log(that.navToggleBtn.attr('aria-expanded'));
        if (!that.navToggleBtn.attr('aria-expanded') || that.navToggleBtn.attr('aria-expanded') === 'False') {
          that.navToggleBtn.attr('aria-expanded', 'True');
        } else {
          that.navToggleBtn.attr('aria-expanded', 'False');
        }
        that.navToggleBtn.toggleClass('collapsed');
        that.navList.toggleClass('in');
      });
    }
  }

  function init() {
    var newTabLinks = $('a[target=_blank]');
    for (var i = 0; i < newTabLinks.length; i++) {
      new NewTabLinks(newTabLink[i]);
    }
    new NavBar();
  }

  $(document).on('page:load', init);
  $(init);

}(jQuery));
