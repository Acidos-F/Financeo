tailwind.config = {
  theme: {
    fontFamily: {
      montserrat: ["Montserrat", "sans-serif"],
      gotu: ["Gotu", "sans-serif"],
    },
  },
};

/**
 * Toggles the visibility of a password field
 * @param {string} id - The ID of the password input field
 */
function togglePasswordVisibility(id) {
  const passwordInput = document.getElementById(id);
  const eyeIcon = document.getElementById(`${id}-eye`);

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    eyeIcon.setAttribute("data-feather", "eye-off");
  } else {
    passwordInput.type = "password";
    eyeIcon.setAttribute("data-feather", "eye");
  }
  feather.replace();
}

/**
 * Shows a toast notification
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, warning, info)
 * @param {number} duration - How long to display the notification in milliseconds
 */
function showToast(message, type = "info", duration = 3000) {
  const toast = document.createElement("div");
  toast.className = `fixed bottom-4 right-4 px-4 py-2 rounded-md text-white shadow-lg ${
    type === "success"
      ? "bg-green-500"
      : type === "error"
      ? "bg-red-500"
      : type === "warning"
      ? "bg-yellow-500"
      : "bg-blue-500"
  }`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("opacity-0", "transition-opacity", "duration-300");
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

document.addEventListener("DOMContentLoaded", function () {
  feather.replace();
  initLoginForm();
});

function initLoginForm() {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitButton = loginForm.querySelector('button[type="submit"]');
    setButtonLoading(submitButton, true);

    try {
      const payload = await submitLoginForm(loginForm);

      if (!payload.success) {
        showToast(payload.message || "Unable to sign in", "error");
        return;
      }

      showToast(payload.message || "Signed in successfully", "success");

      const redirectTarget =
        payload.redirect || loginForm.dataset.redirect || window.location.href;

      setTimeout(() => {
        window.location.href = redirectTarget;
      }, 800);
    } catch (error) {
      showToast(error.message || "Something went wrong", "error");
    } finally {
      setButtonLoading(submitButton, false);
    }
  });
}

async function submitLoginForm(form) {
  const endpoint = form.getAttribute("action") || window.location.href;
  const formData = new FormData(form);

  const response = await fetch(endpoint, {
    method: "POST",
    body: formData,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      Accept: "application/json",
    },
  });

  const responseText = await response.text();
  let payload;

  try {
    payload = JSON.parse(responseText);
  } catch (_error) {
    payload = {
      success: response.ok,
      message: responseText || "Login processed",
    };
  }

  payload.success = payload.success ?? response.ok;
  return payload;
}

function setButtonLoading(button, isLoading) {
  if (!button) return;

  if (isLoading) {
    button.dataset.originalText = button.textContent;
    button.textContent = "Signing in...";
    button.disabled = true;
    button.classList.add("opacity-75", "cursor-not-allowed");
  } else {
    button.textContent = button.dataset.originalText || "Sign in";
    button.disabled = false;
    button.classList.remove("opacity-75", "cursor-not-allowed");
  }
}
