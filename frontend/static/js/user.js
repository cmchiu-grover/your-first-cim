import {
  signupArea,
  signupMessage,
  signinMessage,
  hideSigninDisplaySignup,
  hideSignupDisplaySignin,
  signoutButton,
  closeSignupButton,
  signupForm,
  signinForm,
} from "./variables.js";

async function signup() {
  const username = document.getElementById("signup_name").value;
  const account = document.getElementById("signup_account").value;
  const password = document.getElementById("signup_password").value;
  const position = document.getElementById("signup_position").value;

  try {
    const response = await fetch("/api/user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: username,
        account: account,
        password: password,
        position: position,
      }),
    });
    const data = await response.json();
    // console.log(data);

    if (data.ok) {
      signupMessage.textContent = "註冊成功，";
    } else {
      signupMessage.textContent = data.message + "，";
    }
  } catch (e) {
    console.log("response 失敗...");
    console.log(e);
  }
}

async function signin() {
  const account = document.getElementById("signin_account").value;
  const password = document.getElementById("signin_password").value;

  const response = await fetch("/api/user/auth", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      account: account,
      password: password,
    }),
  });

  const data = await response.json();
  if (data.token) {
    // console.log(data);
    const token = data.token;
    // console.log(token);

    localStorage.setItem("access_token", token);

    window.location.href = "/dashboard";
  } else {
    signinMessage.textContent = data.message + "，";
  }
}

async function showSignInOut() {
  const token = localStorage.getItem("access_token");
  const signInUP = document.querySelector("#sign_in_up");
  const signOut = document.querySelector("#sign_out");

  if (token) {
    const response = await fetch("/api/user/auth", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const JSON = await response.json();
    const userData = JSON.data;

    if (userData) {
      signInUP.style.display = "none";
      signOut.style.display = "flex";
    }
  } else {
    signOut.style.display = "none";
    signInUP.style.display = "flex";
  }
}

function signout() {
  if (signoutButton) {
    signoutButton.addEventListener("click", () => {
      localStorage.removeItem("access_token");
      window.location.href = "/";
    });
  }
}

function divEventListeners() {
  if (hideSigninDisplaySignup) {
    hideSigninDisplaySignup.addEventListener("click", () => {
      signupArea.showModal();
      signupArea.focus();
    });
  }

  if (hideSignupDisplaySignin) {
    hideSignupDisplaySignin.addEventListener("click", () => {
      signupArea.close();
    });
  }

  if (closeSignupButton) {
    closeSignupButton.addEventListener("click", () => {
      signupArea.close();
    });
  }

  if (signinForm) {
    signinForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await signin();
    });
  }

  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await signup();
    });
  }
}

divEventListeners();

export { signout };
