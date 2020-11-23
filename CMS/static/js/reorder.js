(function($) {
  var ResourceSort = function(sortToggle, resourcesArea) {
    this.sortToggle = sortToggle;
    this.resourcesArea = resourcesArea;
    this.setup();
  }

  ResourceSort.prototype = {
    setup: function() {
      this.sortToggle.parent().show();
      this.popularResourceList = this.resourcesArea.find('#popular');
      this.newestResourceList = this.resourcesArea.find('#newest');
      this.oldestResourceList = this.resourcesArea.find('#oldest');
      this.startWatcher();
    },

    startWatcher: function() {
      var that = this;
      this.sortToggle.change(function () {
        that.handleReorder();
      })
    },

    handleReorder: function() {
      if (this.sortToggle[0].value === 'popular') {
        this.newestResourceList.hide();
        this.oldestResourceList.hide();
        this.popularResourceList.show();
      } else if (this.sortToggle[0].value === 'newest') {
        this.popularResourceList.hide();
        this.oldestResourceList.hide();
        this.newestResourceList.show();
      } else if (this.sortToggle[0].value === 'oldest') {
        this.popularResourceList.hide();
        this.newestResourceList.hide();
        this.oldestResourceList.show();
      }
    }
  }

  function init() {
    var sortSelector = $('#order-selector__toggle');
    var sortItems = $('#internal-resources');
    if (sortSelector.length > 0 && sortItems.length > 0) {
      new ResourceSort(sortSelector, sortItems);
    }
  }

  $(document).on('page:load', init);
  $(init);

}(jQuery));
