"use strict";

const button = document.querySelector("#delete-book");

button.addEventListener("click", () => {
  const book_id = document.querySelector(".book-id");
  const url = `/delete${book_id}`;

  fetch(url)
    .then((response) => response.text())
    .then((msg) => {
      document.querySelector("#deleting-status").innerHTML = msg;
    });
});

// function handleDelete() {
//   const book_id = document.querySelector(".book-id");
//   const url = `/delete${book_id}`;

//   fetch(url)
//   .then(function (response) {
//     return response.text();
//   })
//   .then(function (delete) {
//     document.querySelector()
//   });
// }
