const signinArea = document.querySelector("#signin_area");
const signupArea = document.querySelector("#signup_area");

const hideSigninDisplaySignup = document.querySelector(
  "#hide_signin_display_signup"
);
const hideSignupDisplaySignin = document.querySelector(
  "#hide_signup_display_signin"
);

const signinButton = document.querySelector("#signin_button");
const signupButton = document.querySelector("#signup_button");
const signoutButton = document.querySelector("#signout_button");

const signupMessage = document.querySelector("#signupAreaMsg");
const signinMessage = document.querySelector("#signinAreaMsg");

const closeSignupButton = document.querySelector("#close_dialog_icon");

const signupForm = document.querySelector("#signup_form");
const signinForm = document.querySelector("#signin_form");

const userNameP = document.querySelector("#username");
const userNameStrong = document.querySelector("#dashboard_username");

const funcNavUl = document.querySelector("#function_nav_ul");

const notificationList = document.querySelector("#notification_list");

export {
  signinArea,
  signupArea,
  hideSigninDisplaySignup,
  hideSignupDisplaySignin,
  signinButton,
  signupButton,
  signupMessage,
  signinMessage,
  closeSignupButton,
  signupForm,
  signinForm,
  userNameP,
  userNameStrong,
  funcNavUl,
  signoutButton,
  notificationList,
};
