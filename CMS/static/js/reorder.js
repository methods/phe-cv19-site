(function($) {
  var ResourceSort = function(popularButton, newestButton, resourcesArea) {
    this.popularButton = popularButton;
    this.newestButton = newestButton;
    this.resourcesArea = resourcesArea;
    this.setup();
  }

  ResourceSort.prototype = {
    setup: function() {
      this.popularResourceList = this.resourcesArea.find('#popular');
      this.newestResourceList = this.resourcesArea.find('#newest');
      this.startWatcherPopularButton();
      this.startWatcherNewestButton();
    },

    startWatcherPopularButton: function() {
      var that = this;
      this.popularButton.click(function () {
        that.handleReorder('popular');
      })
    },

    startWatcherNewestButton: function() {
      var that = this;
      this.newestButton.click(function () {
        that.handleReorder('newest');
      })
    },

    handleReorder: function(sortType) {
      if (sortType === 'popular') {
        this.newestResourceList.hide();
        this.popularResourceList.show();
        this.newestButton.removeClass('sort-button--selected')
        this.popularButton.addClass('sort-button--selected')
      } else if (sortType === 'newest') {
        this.popularResourceList.hide();
        this.newestResourceList.show();
        this.popularButton.removeClass('sort-button--selected')
        this.newestButton.addClass('sort-button--selected')
      }
    }
  }

  function init() {
    var popularButton = $('#order-selector__popular-button')
    var newestButton = $('#order-selector__newest-button')
    var sortItems = $('#internal-resources');
    if (popularButton.length > 0 && newestButton.length > 0 && sortItems.length > 0) {
      new ResourceSort(popularButton, newestButton, sortItems);
    }
  }

  $(document).on('page:load', init);
  $(init);

}(jQuery));
