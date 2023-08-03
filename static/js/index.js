const pathToRegex = (path) =>
  new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const getParams = (match) => {
  const values = match.result.slice(1);
  const keys = Array.from(match.path.matchAll(/:(\w+)/g)).map(
    (result) => result[1]
  );

  return keys.length > 0 ? Object.fromEntries(
    keys.map((key, i) => {
      return [key, values[i]];
    })
  ) : null;
};

const navigateTo = (url) => {
  history.pushState(null, null, url);
  router();
};

const router = async (uri) => {
  const routes = [
    { path: "/", view: "/" },
    { path: "/pages/encontros/", view: "/encontros" },
    { path: "/pages/encontros/register", view: "/encontros/register" },
    { path: "/pages/encontros/edit/:id", view: "/encontros/edit/:id" },
    { path: "/pages/encontros/:id/eventos", view: "/encontros/:id/eventos" },
    { path: "/pages/encontros/:id/eventos/register", view: "/encontros/:id/eventos/register" },
    { path: "/pages/encontros/teams", view: "/encontros/teams" },
  ];

  const potentialMatches = routes.map((route) => {
    return {
      ...route,
      result: location.pathname.match(pathToRegex(route.path)),
    };
  });

  const match = potentialMatches.find((value) => value.result !== null);
  if (match) {
    const params = getParams(match);
    if (params) {
      for (const [key, value] of Object.entries(params)) {
        match.view = match.view.replace(`:${key}`, value);
      }      
    }
  }

  const request = new XMLHttpRequest();
  request.open("GET", match.view);
  request.onload = () => {
    const response = request.responseText;
    const loadedContent = document.getElementById("app");
    loadedContent.innerHTML = response;
    const scripts = loadedContent.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; ++i) {
      var script = scripts[i];
      eval(script.innerHTML);
    }
  };
  request.send();
};

document.addEventListener("DOMContentLoaded", () => {
  document.body.addEventListener("click", (e) => {
    if (
      e.target.matches("[data-link]") ||
      e.target.parentElement.matches("[data-link]")
    ) {
      const link = e.target.href ?? e.target.parentElement.href;
      e.preventDefault();
      navigateTo(link);
    }
  });

  document.body.addEventListener("submit", (e) => {
    if (e.target.matches(".needs-validation")) {
      e.preventDefault();
      e.stopPropagation();

      if (!e.target.checkValidity()) {
        e.target.classList.add("was-validated");
        return false;
      }

      var formData = new FormData(e.target);

      fetch(e.target.action, {
        body: formData,
        method: e.target.method,
      }).then((resp) => {
        if (resp.ok) {
          navigateTo(e.target.target);
        } else {
          const toastLiveExample = document.getElementById("liveToast");
          const toastBootstrap =
            bootstrap.Toast.getOrCreateInstance(toastLiveExample);

          toastBootstrap.show();
        }
      });

      return false;
    }
  });
  router();
});

const isEmailValid = (email) => {
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};

const isRequired = (value) => (value === "" ? false : true);

const validateField = (field, validations) => {
  if (!field || !validations) return;

  for (let validation of validations) {
    const parent = field.parentElement;
    const previousErrorMsg = parent.querySelector("small");
    if (previousErrorMsg) {
      previousErrorMsg.remove();
    }
    if (!field.value || !validation.handler(field.value.trim())) {
      field.setCustomValidity("Invalid field");
      let errorMsg = document.createElement("small");
      errorMsg.classList.add("invalid-feedback");
      errorMsg.textContent = validation.message;
      parent.appendChild(errorMsg);
      return false;
    } else {
      field.setCustomValidity("");
    }
  }
  return true;
};

const validateForm = (validationList) => {
  let result = true;
  for (let validationItem of validationList) {
    const field = document.querySelector(validationItem.selector);
    field.addEventListener("keyup", () => {
      validateField(field, validationItem.validations);
    });
    if (!validateField(field, validationItem.validations)) {
      result = false;
    }
  }
  return result;
};

const sendFormData = (form, toastMsg = "") => {
  let formData = new FormData(form);

  fetch(form.action, {
    body: formData,
    method: form.method,
  }).then((resp) => {
    if (resp.ok) {
      const mainToast = document.getElementById("mainToast");
      const mainToastMsg = mainToast.querySelector(".toast-body");
      mainToastMsg.textContent = toastMsg;
      const toastBootstrap = bootstrap.Toast.getOrCreateInstance(mainToast);

      toastBootstrap.show();
      navigateTo(form.target);
    } else {
      const toastLiveExample = document.getElementById("myToast");
      const toastBootstrap =
        bootstrap.Toast.getOrCreateInstance(toastLiveExample);

      toastBootstrap.show();
    }
  });
};
