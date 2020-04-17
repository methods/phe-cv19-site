(function($) {
  var SUBSCRIPTION_URL = "{{url_address}}";

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

  var SubscriptionForm = function(form) {
    this.form = $(form);
    this.emailVaildationRegex = /^[a-zA-Z0-9\-_]+(\.[a-zA-Z0-9\-_]+)*@[a-z0-9]+(\-[a-z0-9]+)*(\.[a-z0-9]+(\-[a-z0-9]+)*)*\.[a-z]{2,4}$/;
    this.nameValidationRegex = /^[A-Za-z]+$/;
    this.setup();
  }

  SubscriptionForm.prototype = {
    setup: function() {
      this.firstNameField = this.form.find('#firstname');
      this.firstNameErrorSpace = this.firstNameField.siblings().filter('.subscription-form__error');
      this.lastNameField = this.form.find('#lastname');
      this.lastNameErrorSpace = this.lastNameField.siblings().filter('.subscription-form__error');
      this.emailField = this.form.find('#email');
      this.emailErrorSpace = this.emailField.siblings().filter('.subscription-form__error');
      this.termsField = this.form.find('#terms');
      this.termsErrorSpace = this.termsField.siblings().filter('.subscription-form__error');
      this.signUpSuccessMessage = this.form.find('.subscription-form__success');
      this.signUpFailMessage = this.form.find('.subscription-form__fail');
      this.errors = {};
      this.startWatcher();
    },

    clearErrors: function() {
      this.errors = {};
      this.firstNameErrorSpace.text('');
      this.firstNameErrorSpace.hide();
      this.firstNameErrorSpace.parent().removeClass('error');
      this.lastNameErrorSpace.text('');
      this.lastNameErrorSpace.hide();
      this.lastNameErrorSpace.parent().removeClass('error');
      this.emailErrorSpace.text('');
      this.emailErrorSpace.hide();
      this.emailErrorSpace.parent().removeClass('error');
      this.termsErrorSpace.text('');
      this.termsErrorSpace.hide();
      this.termsErrorSpace.parent().removeClass('error');
      this.signUpFailMessage.hide();
      this.signUpSuccessMessage.hide();
    },

    startWatcher: function() {
      var that = this;
      this.form.submit(function(evt) {
        evt.preventDefault();
        that.clearErrors();
        if (that.validateForm()){
          var formData = {
            "ProductToken": "C17E9070-417E-44FF-8F98-C0ADB81507A8",
            "Email": that.emailField.val(),
            "Firstname": that.firstNameField.val(),
            "Lastname": that.lastNameField.val()
          }
          $.post(SUBSCRIPTION_URL, formData, function(data, status) {
            if (status === 'success') {
              that.signUpSuccessMessage.show();
            } else {
              that.signUpFailMessage.show();
            }
          })
          .fail(function(response) {
            that.signUpFailMessage.show();
          });
        } else {
          that.showErrors();
        }
      });
    },

    validateForm: function() {
      var validNames = this.validateNameFields();
      var validEmails = this.validateEmailField();
      var validTerms = this.validateTermsField();
      return validNames && validEmails && validTerms;
    },

    validateNameFields: function() {
      var firstNameValid = true;
      var lastNameValid = true;
      if (this.firstNameField.val() === '') {
        this.errors.firstName = 'Please enter your first name';
        firstNameValid = false;
      } else if (!this.nameValidationRegex.test(this.firstNameField.value)) {
        this.errors.firstName = 'An invalid character has been entered';
        firstNameValid = false;
      }

      if (this.lastNameField.val() === '') {
        this.errors.lastName = 'Please enter your last name';
        lastNameValid = false;
      } else if (!this.nameValidationRegex.test(this.lastNameField.value)) {
        this.errors.lastName = 'An invalid character has been entered';
        lastNameValid = false;
      }

      return firstNameValid && lastNameValid;
    },

    validateEmailField: function() {
      if (this.emailField.val() === '') {
        this.errors.email = 'Please enter an email address';
        return false;
      } else if (!this.emailVaildationRegex.test(this.emailField.val())) {
        this.errors.email = 'Please enter a valid email address';
        return false;
      }
      return true;
    },

    validateTermsField: function() {
      if (!this.termsField[0].checked) {
        this.errors.terms = 'You must accept the terms and conditions to subscribe';
        return false;
      }
      return true;
    },

    showErrors: function() {
      if (this.errors.firstName) {
        this.firstNameErrorSpace.text(this.errors.firstName);
        this.firstNameErrorSpace.show();
        this.firstNameErrorSpace.parent().addClass('error');
      }
      if (this.errors.lastName) {
        this.lastNameErrorSpace.text(this.errors.lastName);
        this.lastNameErrorSpace.show();
        this.lastNameErrorSpace.parent().addClass('error');
      }
      if (this.errors.email) {
        this.emailErrorSpace.text(this.errors.email);
        this.emailErrorSpace.show();
        this.emailErrorSpace.parent().addClass('error');
      }
      if (this.errors.terms) {
        this.termsErrorSpace.text(this.errors.terms);
        this.termsErrorSpace.show();
        this.termsErrorSpace.parent().addClass('error');
      }
    }
  }

  function init() {
    var newTabLinks = $('a[target=_blank]');
    for (var i = 0; i < newTabLinks.length; i++) {
      new NewTabLinks(newTabLink[i]);
    }

    var subscriptionFormElements = $('.subscription-form');
    for (var i = 0; i < subscriptionFormElements.length; i++) {
      new SubscriptionForm(subscriptionFormElements[i]);
    }

    new NavBar();
  }

  $(document).on('page:load', init);
  $(init);

}(jQuery));
