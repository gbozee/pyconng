let pricings = window.INITIALIZER.pricings
let coupon_url = window.INITIALIZER.coupon_url
let purchase_url = window.INITIALIZER.purchase_url
let public_key = window.INITIALIZER.public_key

function getNumberOfTickets() {
    let result = {}
    Object.keys(pricings).forEach(p => {
        result[p] = document.querySelector(`li#${p} select`).value
    })
    return result
}
document.querySelector('#coc_confirm').addEventListener("change",()=>{
    determineTotal()
})
function determineTotal() {
    let prices = getNumberOfTickets()
    let total = 0
    let ticket_counts = 0
    Object.keys(prices).forEach(i => {
        let prev = pricings[i]
        total += (parseInt(prev) * prices[i])
        ticket_counts += parseInt(prices[i])
    })
    let discount = document.querySelector("#percent-value").textContent
    let discountValue = total * parseInt(discount) / 100
    let checked = document.querySelector('#coc_confirm').checked
    total = total - discountValue
    document.querySelector("#ticket-count").textContent = ticket_counts;
    document.querySelector("#total-fee").textContent = total.toLocaleString()
    if (total > 0 && checked) {
        document.querySelector("#pstackButton").disabled = false
    }else{
        document.querySelector("#pstackButton").disabled = true
    }
    return total
}
determineTotal()
document.querySelectorAll('li select').forEach(node => {
    node.addEventListener("change", determineTotal)
})
var button = document.getElementById("toStep2")
button.addEventListener("click", toNextStep)
document.getElementById('pstackButton').addEventListener('click', payWithPaystack)

function payWithPaystack(e) {
    e.preventDefault()
    Ticketslug((value) => {
        if (value.order) {
            let details = getUserDetails()
            var handler = PaystackPop.setup({
                key: public_key,
                email: details.email,
                amount: value.total * 100,
                ref: value.order, // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
                metadata: {
                    custom_fields: [details]
                },
                callback: function (response) {
                    validateReference(value.order, response.reference, (data) => {
                        if (data.status) {
                            window.location.href = `/tickets/purchase-complete/${value.order}/`
                        } else {
                            alert('Could not verify transaction. Please drop us a message on pythonnigeria.slack.com');

                        }
                    })
                },
                onClose: function () {
                    alert('Click "Pay now" to retry payment.');
                }
            });
            handler.openIframe();
        } else {

        }

    })
}

function toNextStep(e) {
    e.preventDefault()
    let first_name = document.querySelector('#first_name').value
    let last_name = document.querySelector('#last_name').value
    let email = document.querySelector('#email').value
    if (Boolean(first_name) && Boolean(last_name) && Boolean(email)) {
        displayError(false)
        document.querySelector('#payment-link').click()
    } else {
        displayError(true)
    }
}
function getUserDetails(){
    return {
        first_name: document.querySelector('#first_name').value,
        last_name: document.querySelector('#last_name').value,
        email: document.querySelector('#email').value
    }
}

function displayError(status) {
    let err = document.querySelector('#error-section')
    if (status) {
        err.className = err.className.replace('hide-section', "")

    } else {
        err.className = `${err.className.replace('hide-section',"")} hide-section`
    }
}

function InitialDiscountLink(klass) {
    let node = document.querySelector('#initiate-discount')
    node.className = klass
}
document.querySelector('#initiate-discount').addEventListener("click", (e) => {
    let coupon_section = document.querySelector('.coupon-code')
    coupon_section.className = coupon_section.className.replace("hide-section", "")
    InitialDiscountLink("hide-section")
})
document.querySelector("#code_btn").addEventListener("click", e => {
    e.preventDefault()
    let coupon_value = document.querySelector('#coupon_value').value
    validateCoupon(coupon_value, (data) => {
        if (Boolean(data)) {
            if (data.status > 0) {
                let discountDisplay = document.querySelector(".discount_value")
                let coupon_section = document.querySelector('.coupon-code')
                coupon_section.className = `${coupon_section.className} hide-section`
                discountDisplay.className = discountDisplay.className.replace("hide-section", "")
                document.querySelector("#percent-value").textContent = data.status
                determineTotal()
            } else {
                InitialDiscountLink("")
            }
        }
    })
})

function validateCoupon(value, callback) {
    var url = `${coupon_url}?value=${value}`;
    makeGet(url, callback)
}

function makeGet(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            callback(myArr);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function makePost(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            callback(myArr);
        }
    };
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(data));
}

function Ticketslug(callback) {
    var url = `${purchase_url}`;
    makePost(url, {
        coupon: document.querySelector('#coupon_value').value,
        tickets: getNumberOfTickets()
    }, callback)
}

function validateReference(order, ref, callback) {
    var url = `/tickets/paystack/validate/${order}/${ref}`
    makeGet(url, callback)
}
