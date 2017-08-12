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
