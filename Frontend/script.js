document.addEventListener('DOMContentLoaded', function () {
    const notificationElement = document.getElementById('notification');
    const paymentclass = document.querySelector('.payment');

    function showNotification(message) {
        notificationElement.textContent = message;
        notificationElement.style.backgroundColor = '#f8d7da';
        notificationElement.style.borderColor = '#f5c6cb';
        notificationElement.style.display = 'block';

        setTimeout(function () {
            notificationElement.style.display = 'none';
        }, 2000);
    }

    function showNotificationOk(message) {
        notificationElement.textContent = message;
        notificationElement.style.backgroundColor = '#d4edda';
        notificationElement.style.borderColor = '#c3e6cb';
        notificationElement.style.color = '#155724';
        notificationElement.style.display = 'block';
        
        setTimeout(function () {
            notificationElement.style.display = 'none';
        }, 2000);
    }

    paymentclass.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fullname = document.getElementById("fullname").value;
        const nameoncard = document.getElementById("nameoncard").value;
        const emailaddress = document.getElementById("emailaddress").value;
        const address = document.getElementById("address").value;
        const city = document.getElementById("city").value;
        const daybirth = document.getElementById("daybirth").value;
        const monthbirth = document.getElementById("monthbirth").value;
        const yearbirth = document.getElementById("yearbirth").value;
        const gender = document.querySelector('input[name="gender"]:checked').value;
        const payment = document.querySelector('input[name="pay"]:checked').value;
        const cardnumber = document.getElementById("cardnumber").value;
        const cardcvv = document.getElementById("cardcvv").value;
        const expmonth = document.getElementById("expmonth").value;
        const expyear = document.getElementById("expyear").value;
        const amount = document.getElementById("amount").value;

        const formData = new FormData();
        formData.append("fullname", fullname);
        formData.append("nameoncard", nameoncard);
        formData.append("emailaddress", emailaddress);
        formData.append("address", address);
        formData.append("city", city);
        formData.append("daybirth", daybirth);
        formData.append("monthbirth", monthbirth);
        formData.append("yearbirth", yearbirth);
        formData.append("gender", gender);
        formData.append("payment", payment);
        formData.append("cardnumber", cardnumber);
        formData.append("cardcvv", cardcvv);
        formData.append("expmonth", expmonth);
        formData.append("expyear", expyear);
        formData.append("amount", amount);
        try {
            const response = await fetch("http://127.0.0.1:8000/payment", {
                method: "POST",
                headers: {
                    // Change Content-Type to "application/x-www-form-urlencoded"
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams(formData),
            });
            if (response.ok) {
                // User registered successfully, show success message
                showNotificationOk("Payment Process Success!");
                // Redirect to sign-in page
                window.location.href = "success.html";

                //clear input value
                // document.getElementById("fullname").value = "";
                // document.getElementById("nameoncard").value = "";
                // document.getElementById("emailaddress").value = "";
                // document.getElementById("address").value = "";
                // document.getElementById("city").value = "";
                // document.getElementById("daybirth").value = "";
                // document.getElementById("monthbirth").value = "";
                // document.getElementById("yearbirth").value = "";
                // document.getElementById("cardnumber").value = "";
                // document.getElementById("cardcvv").value = "";
                // document.getElementById("expmonth").value = "";
                // document.getElementById("expyear").value = "";
                // document.getElementById("amount").value = "";
            } else {
                // Registration failed, show error message
                showNotification("Payment failed. Please try again.");
            }
        } catch (error) {
            showNotification("Error during payment");
            console.error("Error during payment:", error.message);
        }
    });
});