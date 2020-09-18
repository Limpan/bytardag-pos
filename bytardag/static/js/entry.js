"use strict";
import {sellers} from "./autocomplete.js";

let csrf;
let history;

window.sellers = sellers;
let sellerTag;
let suggestions;

document.addEventListener("DOMContentLoaded", function () {
    console.log('DOM Ready...');

    csrf = document.getElementById('csrf_token').value;

    history = document.getElementById('history');

    // Submit form via AJAX.
    document.getElementById('register').addEventListener('submit', function (evt) {
        evt.preventDefault();
        submitForm(this);
    });

    suggestions = document.getElementById('suggestions');
    sellerTag = document.getElementById('seller');
    sellerTag.addEventListener('keyup', autoComplete);
//    sellerTag.addEventListener('focusout', function(evt) { setTimeout(function () {suggestions.innerHTML = '';}, 100 ) });
});


function submitForm(form, evt) {
    let seller = document.getElementById('seller');
    let amount = document.getElementById('amount');
    let numRows = document.getElementById('num-rows');

    const data = { 
        seller: seller.value, 
        amount: amount.value, 
        csrf_token: csrf
    };

    fetch(form.action, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        form.reset();
        seller.focus();

        let listItem = document.createElement('li');
        listItem.innerHTML = data.rendered_string;
        history.prepend(listItem);
        numRows.innerText = data.num_rows;
        
    })
    .catch((error) => {
      console.error('Error:', error);
      // Update UI with error message
    });
}


function autoComplete(evt) {

  // Add '-' if first character, except when using backspace.
  if (evt.target.value.length == 1 && evt.keyCode != 8) {
    evt.target.value = evt.target.value.toUpperCase() + '-';
  }

  // Show autocomplete list except when matching.
  if (evt.target.value.length > 0 && !sellers.includes(evt.target.value)) {
    let ulTag = document.createElement('ul');

    let elms = sellers.filter(s => s.startsWith(evt.target.value)).slice(0, 10);
  
    elms.forEach(s => {
      let liTag = document.createElement('li');
      liTag.innerHTML = `${s}`;
      liTag.onclick = function(evt) { useACValue(s); };
      ulTag.appendChild(liTag);
    });

    if (suggestions.children.length == 0) {
      suggestions.appendChild(ulTag);
    } else {
      suggestions.innerHTML = '';
      suggestions.appendChild(ulTag);
    }

    console.log(elms);
  } else {
    suggestions.innerHTML = '';
  }
}


function useACValue(value) {
  sellerTag.value = value;
  suggestions.innerHTML = '';
  document.getElementById('amount').focus();
}




/* https://stackoverflow.com/questions/152975/how-do-i-detect-a-click-outside-an-element/3028037#3028037

function hideOnClickOutside(element) {
    const outsideClickListener = event => {
        if (!element.contains(event.target) && isVisible(element)) { // or use: event.target.closest(selector) === null
          element.style.display = 'none'
          removeClickListener()
        }
    }

    const removeClickListener = () => {
        document.removeEventListener('click', outsideClickListener)
    }

    document.addEventListener('click', outsideClickListener)
}

const isVisible = elem => !!elem && !!( elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length ) // source (2018-03-11): https://github.com/jquery/jquery/blob/master/src/css/hiddenVisibleSelectors.js 

*/