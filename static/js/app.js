"use strict";

// remove book from bookshelf

const forms = document.querySelectorAll(".delete-book");

for (const form of forms) {
  form.addEventListener("submit", (evt) => {
    evt.preventDefault();
    const book_id = evt.target["book-id"].value;
    const url = `/delete_book/${book_id}`;

    fetch(url)
      .then((response) => response.text())
      .then((result) => {
        const row_id = document.querySelector(`#book-${book_id}`);
        console.log(row_id);
        row_id.remove();
      });
  });
}

// create account show/hide password

document.addEventListener("click", function (event) {
  if (event.target.classList.contains("toggle-password")) {
    event.target.classList.toggle("fa-eye");
    event.target.classList.toggle("fa-eye-slash");

    var input = document.getElementById("password");
    input.getAttribute("type") === "password"
      ? (input.setAttribute("type", "text"),
        (event.target.style.color = "##fcfcfc"))
      : (input.setAttribute("type", "password"),
        (event.target.style.color = "#fcfcfc"));
  }
});

// login show/hide password

document.addEventListener("click", function (event) {
  if (event.target.classList.contains("toggle-login-password")) {
    event.target.classList.toggle("fa-eye");
    event.target.classList.toggle("fa-eye-slash");

    var input = document.getElementById("password");
    input.getAttribute("type") === "password"
      ? (input.setAttribute("type", "text"),
        (event.target.style.color = "##fcfcfc"))
      : (input.setAttribute("type", "password"),
        (event.target.style.color = "#fcfcfc"));
  }
});

// remember me

const rmCheck = document.getElementById("rememberMe"),
  usernameInput = document.getElementById("username");

if (localStorage.checkbox && localStorage.checkbox !== "") {
  rmCheck.setAttribute("checked", "checked");
  usernameInput.value = localStorage.username;
} else {
  rmCheck.removeAttribute("checked");
  usernameInput.value = "";
}

function lsRememberMe() {
  if (rmCheck.checked && emailInput.value !== "") {
    localStorage.username = usernameInput.value;
    localStorage.checkbox = rmCheck.value;
  } else {
    localStorage.username = "";
    localStorage.checkbox = "";
  }
}
