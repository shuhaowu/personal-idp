"use strict";

$(function() {
  var authBtn = $("#authenticate");
  var cancelBtn = $("#cancel");
  var usernameField = $("#username");
  var passwordField = $("#password");

  authBtn.on("click", function(e) {
    usernameField.removeClass("invalid");
    passwordField.removeClass("invalid");

    var username = usernameField.val();
    var password = passwordField.val();

    username = $.trim(username);
    usernameField.val(username);

    var valid = true;
    if (username.length === 0) {
      usernameField.addClass("invalid");
      valid = false;
    } else {
    }

    if (password.length === 0) {
      passwordField.addClass("invalid");
      valid = false
    }

    if (!valid)
      return false;

    usernameField.attr("readonly", "readonly");
    passwordField.attr("readonly", "readonly");
    authBtn.attr("disabled", "disabled");
    authBtn.text("Checking...");


    var success = function() {
      navigator.id.completeAuthentication();
    };

    var error = function() {
      usernameField.addClass("invalid");
      passwordField.addClass("invalid");
      usernameField.removeAttr("readonly");
      passwordField.removeAttr("readonly");
      authBtn.removeAttr("disabled");
      authBtn.text("Invalid credentials");
      setTimeout(function() { authBtn.text("Authenticate"); }, 1000);
    };

    var req = $.ajax({
      url: "login",
      type: "POST",
      data: {username: username, password: password},
      success: success,
      error: error
    });

  });
});

