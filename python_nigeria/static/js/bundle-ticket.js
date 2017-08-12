/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

var currency = "₦";
$(function() {
  function toggleBusiness(status) {
    if (status) {
      $('td[data-fare="TRSC"]').addClass("disabled");
    } else {
      $('td[data-fare="TRSC"]').removeClass("disabled");
    }
    $('input[name="TRSC"]').attr("disabled", status);
  }
  //   toggleBusiness(true);
  $("select[name='order_type']").change(e => {
    let student_price = $('td[data-fare="TRSS"]');
    let personal_price = $('td[data-fare="TRSP"]');
    let company_price = $('td[data-fare="TRSC"]');
    let selected_option = e.target.value;
    console.log(selected_option);
  });
  function updateTotal(qty = 0, sel_text) {
    let selected = $(`#fare-${sel_text}`).attr("data-amount");
    let total = parseFloat(selected) * qty;
    return total;
  }
  let total = 0;
  let grand_total = 0;
  $("td.fare input").change(function(e) {
    const prices = $.map($("td.fare input"), node => {
      const qty = $(node).val() || 0;
      let qty_price = $(node).parent().attr("data-fare");
      console.log(qty);
      console.log(qty_price);
      return updateTotal(qty, qty_price);
    });
    total = prices.reduce((sum, value) => {
      return sum + value;
    }, 0);
    $(".total b").text(`${currency} ${total}`);
    $(".total.grand b").text(`${currency} ${total}`);
    $('#id_coupon').trigger('blur');
  });
  $("#id_coupon").on("blur", function(e) {
    var text = e.target.value;
    if (text.length > 0) {
      $.get(`/tickets/coupons?value=${text}`).then(data => {
        console.log(data);
        grand_total = total * (100 - data.status) / 100;
        $(".total.grand b").text(`${currency} ${grand_total}`);
      });
    }
  });
  
});


/***/ })
/******/ ]);