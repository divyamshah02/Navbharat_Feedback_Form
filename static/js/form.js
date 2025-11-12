let otp_id = null
let mobile = null


// Declare bootstrap variable or import it
const bootstrap = window.bootstrap

// OTP Input Handling
const otpInputs = document.querySelectorAll(".otp-input")

otpInputs.forEach((input, index) => {
  input.addEventListener("input", (e) => {
    const value = e.target.value

    // Only allow numbers
    if (!/^\d*$/.test(value)) {
      e.target.value = ""
      return
    }

    // Move to next input if value entered
    if (value && index < otpInputs.length - 1) {
      otpInputs[index + 1].focus()
    }
  })

  input.addEventListener("keydown", (e) => {
    // Move to previous input on backspace if current is empty
    if (e.key === "Backspace" && !e.target.value && index > 0) {
      otpInputs[index - 1].focus()
    }
  })

  // Handle paste
  input.addEventListener("paste", (e) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text").slice(0, 6)

    if (!/^\d+$/.test(pastedData)) return

    pastedData.split("").forEach((char, i) => {
      if (otpInputs[i]) {
        otpInputs[i].value = char
      }
    })

    // Focus last filled input or last input
    const lastIndex = Math.min(pastedData.length, otpInputs.length - 1)
    otpInputs[lastIndex].focus()
  })
})

const otpModal = new bootstrap.Modal(document.getElementById("otpModal"))

// Send OTP
document.getElementById("sendOtp").onclick = async () => {
  mobile = document.getElementById("mobile").value.trim()
  const name = document.getElementById("name").value.trim()

  if (!name) {
    alert("Please enter your name")
    return
  }

  if (mobile.length !== 10 || !/^\d+$/.test(mobile)) {
    alert("Enter valid 10-digit mobile number")
    return
  }

  const [success, res] = await callApi("POST", "/api/otp-api/", { mobile })

  if (success && res.success) {
    otp_id = res.data.otp_id

    otpModal.show()

    // Focus first OTP input
    setTimeout(() => {
      otpInputs[0].focus()
    }, 300)

    alert("OTP sent via WhatsApp!")
  } else {
    alert("Failed to send OTP. Please try again.")
  }
}

// Verify OTP
document.getElementById("verifyOtp").onclick = async () => {
  // Collect OTP from all inputs
  const otp = Array.from(otpInputs)
    .map((input) => input.value)
    .join("")

  if (otp.length !== 6) {
    alert("Please enter complete 6-digit OTP")
    return
  }

  const [success, res] = await callApi("PUT", `/api/otp-api/${otp_id}/`, { otp })

  if (success && res.data.otp_verified) {
    const name = document.getElementById("name").value.trim()
    const email = document.getElementById("email").value.trim()

    const [ok, resp] = await callApi("POST", "/api/form-submit/", { name, email, mobile })

    if (ok && resp.success) {
      otpModal.hide()

      document.getElementById("form-step1").classList.add("d-none")

      document.getElementById("successMessage").classList.remove("d-none")

      // Clear OTP inputs
      otpInputs.forEach((input) => (input.value = ""))
    } else {
      alert("Error processing your request. Please try again.")
    }
  } else {
    alert(res.data.message || "OTP verification failed. Please try again.")
    // Clear OTP inputs and focus first
    otpInputs.forEach((input) => (input.value = ""))
    otpInputs[0].focus()
  }
}
