"use strict";

$(function() {
  var authBtn = $("#authenticate");
  var cancelBtn = $("#cancel");
  var usernameField = $("#username");
  var passwordField = $("#password");
  var codeField = $("#code");
  var loginForm = $("#loginform");

  loginForm.on("submit", function(e) {
    e.preventDefault();
    usernameField.removeClass("invalid");
    passwordField.removeClass("invalid");
    codeField.removeClass("invalid");

    var username = usernameField.val();
    var password = passwordField.val();
    var code = codeField.val();

    code = $.trim(code);
    codeField.val(code);
    username = $.trim(username);
    usernameField.val(username);

    var valid = true;
    if (username.length === 0) {
      usernameField.addClass("invalid");
      valid = false;
    }

    if (code.length === 0) {
      codeField.addClass("invalid");
      valid = false;
    }

    if (password.length === 0) {
      passwordField.addClass("invalid");
      valid = false
    }

    if (!valid)
      return false;

    usernameField.attr("readonly", "readonly");
    passwordField.attr("readonly", "readonly");
    codeField.attr("readonly", "readonly");
    authBtn.attr("disabled", "disabled");
    authBtn.text("Checking...");


    var success = function() {
      navigator.id.completeAuthentication();
    };

    var error = function() {
      usernameField.addClass("invalid");
      passwordField.addClass("invalid");
      codeField.addClass("invalid");
      usernameField.removeAttr("readonly");
      passwordField.removeAttr("readonly");
      codeField.removeAttr("readonly");
      authBtn.removeAttr("disabled");
      authBtn.text("Invalid credentials");
      setTimeout(function() { authBtn.text("Authenticate"); }, 1000);
    };

    var req = $.ajax({
      url: "login",
      type: "POST",
      data: {username: username, password: password, code: code},
      success: success,
      error: error
    });

    return false;
  });
});

