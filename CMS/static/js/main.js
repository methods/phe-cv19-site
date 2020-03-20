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

  function init() {
    var newTabLinks = $('a[target=_blank]');
    for (var i = 0; i < newTabLinks.length; i++) {
      new NewTabLinks(newTabLink[i]);
    }
  }

  $(document).on('page:load', init);
  $(init);

}(jQuery));
