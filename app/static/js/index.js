const pathToRegex = (path) =>
  new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const getParams = (match) => {
  const values = match.result.slice(1);
  const keys = Array.from(match.path.matchAll(/:(\w+)/g)).map(
    (result) => result[1]
  );

  return keys.length > 0
    ? Object.fromEntries(
        keys.map((key, i) => {
          return [key, values[i]];
        })
      )
    : null;
};

const navigateTo = (url) => {
  history.pushState(null, null, url);
  router();
};

const router = async () => {
  const routes = [
    { path: "/", view: "/" },
    { path: "/pages/casais/", view: "/casais" },
    { path: "/pages/casais/register", view: "/casais/register" },
    { path: "/pages/casais/:id/editar", view: "/casais/:id/editar" },
    { path: "/pages/movimentos/", view: "/movimentos" },
    { path: "/pages/movimentos/register", view: "/movimentos/register" },
    { path: "/pages/movimentos/:id/edit", view: "/movimentos/:id/edit" },
    {
      path: "/pages/movimentos/:id/encontros",
      view: "/movimentos/:id/encontros",
    },
    {
      path: "/pages/movimentos/:id/encontros/register",
      view: "/movimentos/:id/encontros/register",
    },
    {
      path: "/pages/movimentos/:id_movimento/encontros/:id_encontro/edit",
      view: "/movimentos/:id_movimento/encontros/:id_encontro/edit",
    },
    { path: "/pages/movimentos/:id/equipes", view: "/movimentos/:id/equipes" },
    {
      path: "/pages/movimentos/:id/equipes/nova",
      view: "/movimentos/:id/equipes/nova",
    },
    {
      path: "/pages/movimentos/:id/equipes/:id_equipe",
      view: "/movimentos/:id/equipes/:id_equipe",
    },
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
    match.view = match.view + location.search;
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
  const formData = new FormData(form);
  const params = new URLSearchParams(formData);

  if (form.method.toUpperCase() === "GET") {
    navigateTo(form.action + "?" + params);
  } else
    fetch(form.action, {
      body: formData,
      method: form.method,
    }).then((resp) => {
      if (resp.ok) {
        const mainToast = document.getElementById("mainToast");
        mainToast.classList.remove("text-bg-warning");
        mainToast.classList.add("text-bg-success");
        const mainToastMsg = mainToast.querySelector(".toast-body");
        mainToastMsg.textContent = toastMsg;
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(mainToast);

        toastBootstrap.show();
        navigateTo(form.target);
      } else {
        const mainToast = document.getElementById("mainToast");
        mainToast.classList.add("text-bg-warning");
        const mainToastMsg = mainToast.querySelector(".toast-body");
        mainToastMsg.textContent = "Falha na validação do formulário";
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(mainToast);

        toastBootstrap.show();
      }
    });
};
