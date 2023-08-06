(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery', 'slider'], factory);
    } else {
        // Browser globals
        factory(root.jQuery, root.Slider);
    }
}(typeof self !== 'undefined' ? self : this, function ($, Slider) {
  $(function() {
    var sliders = {
      sliders: {},

      customPaging: function(slider, index) {
        var title = $(slider.$slides[index]).find('.title').text();
        var alttext = $(slider.$slides[index]).find('.sliderImage img').attr('alt');
        var buttonText = title || alttext || index;
        var button = $('<button type="button" data-index="' + (index + 1) + '" />').text(buttonText);
        return button[0].outerHTML
      },

      init: function() {
        var self = this;
        $(".sliderWrapper").each(function() {
          var settings = $(this).data("settings");
          settings['customPaging'] = self.customPaging;
          self.sliders[this.id] = new Slider($(".sliderPanes", this), settings);
        });
      },
      update: function() {
        var self = this;
        $(".sliderWrapper > :not(.slick-initialized)").each(function() {

          var sliderPane = $(this);
          var sliderId = sliderPane.parent().attr("id");
          var settings = sliderPane.parent().data("settings");
          settings.customPaging = self.customPaging;

          if (sliderId in self.sliders) {
            self.sliders[sliderId].update(sliderPane, settings);
          } else {
            self.sliders[sliderId] = new Slider(sliderPane, settings);
          }

        });
      }
    };

    sliders.init();

    $(document).on("blockContentReplaced", function() { sliders.update(); });

    $(document).on("sortstop", ".sl-column", function() { sliders.update(); });
  });
}));
