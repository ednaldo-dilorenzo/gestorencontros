const pathToRegex = (path) =>
  new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const navigateTo = (url) => {
  history.pushState(null, null, url);
  router();
};

const router = async (uri) => {
  const routes = [
    { path: "/", view: "/" },
    { path: "/pages/encontros/", view: "/encontros" },
    { path: "/pages/encontros/register", view: "/encontros/register" },
    { path: "/pages/encontros/teams", view: "/encontros/teams" },
    { path: "/alunos", view: "/alunos" },
    { path: "/alunos/add", view: "/alunos/add" },
    { path: "/alunos/:id", view: "/alunos/add-ajax" },
  ];

  const resolvedLocation = uri ? uri : location.pathname;

  const potentialMatches = routes.map((route) => {
    return {
      ...route,
      result: resolvedLocation.match(pathToRegex(route.path)),
    };
  });

  const match = potentialMatches.find((value) => value.result !== null);

  const request = new XMLHttpRequest();
  request.open("GET", match.view);
  request.onload = () => {
    const response = request.responseText;
    const loadedContent = document.getElementById("app");
    loadedContent.innerHTML = response;
    const scripts = loadedContent.getElementsByTagName("script");
    const body = document.querySelector("body");
    for (var i = 0; i < scripts.length; ++i) {
      var script = scripts[i];
      body.appendChild(script);
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

const sendFormData = (form) => {
  let formData = new FormData(form);

  fetch(form.action, {
    body: formData,
    method: form.method,
  }).then((resp) => {
    if (resp.ok) {
      navigateTo(form.target);
    } else {
      const toastLiveExample = document.getElementById("liveToast");
      const toastBootstrap =
        bootstrap.Toast.getOrCreateInstance(toastLiveExample);

      toastBootstrap.show();
    }
  });
};
