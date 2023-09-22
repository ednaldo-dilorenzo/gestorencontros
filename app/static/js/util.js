function getParams(match) {
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
}

function pathToRegex(path) {
  return new RegExp(
    "^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$"
  );
}

async function router() {
  const routes = [
    { path: "/", view: "/dashboard" },
    { path: "/pages/casais", view: "/casais" },
    { path: "/pages/casais/novo", view: "/casais/novo" },
    { path: "/pages/casais/:id", view: "/casais/:id" },
    { path: "/pages/movimentos", view: "/movimentos" },
    { path: "/pages/movimentos/register", view: "/movimentos/register" },
    { path: "/pages/movimentos/:id", view: "/movimentos/:id" },
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
    {
      path: "/pages/movimentos/:id_movimento/encontros/:id_encontro/circulos",
      view: "/movimentos/:id_movimento/encontros/:id_encontro/circulos",
    },
    {
      path: "/pages/movimentos/:id_movimento/encontros/:id_encontro/novo",
      view: "/movimentos/:id_movimento/encontros/:id_encontro/novo",
    },
    {
      path: "/pages/movimentos/:id_movimento/encontros/:id_encontro/circulos/:id_circulo",
      view: "/movimentos/:id_movimento/encontros/:id_encontro/circulos/:id_circulo",
    },
    {
      path: "/pages/movimentos/:id_movimento/encontros/:id_encontro/inscritos/",
      view: "/movimentos/:id_movimento/encontros/:id_encontro/inscritos",
    },
    {
      path: "/pages/movimentos/:id_movimento/encontros/:id_encontro/circulos/montagem",
      view: "/movimentos/:id_movimento/encontros/:id_encontro/circulos/montagem",
    },
    {
      path: "/pages/usuarios",
      view: "/usuarios",
    },
    {
      path: "/pages/usuarios/registrar",
      view: "/usuarios/registrar",
    },
    {
      path: "/pages/usuarios/:id_usuario",
      view: "/usuarios/:id_usuario",
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

  $("#app").load(match.view);
}

function navigateTo(url) {
  history.pushState(null, null, url);
  router();
}

function isEmailValid(email) {
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function isRequired(value) {
  return value && value.trim();
}


function validateField(field, validations) {
  if (!field || !validations) return;

  const validationTypes = {
    required: isRequired,
    email: isEmailValid,
  };

  for (let validation of validations) {
    const parent = field.parentElement;
    const previousErrorMsg = parent.querySelector("small");
    if (previousErrorMsg) {
      previousErrorMsg.remove();
    }
    if (
      validation.handler && validationTypes[validation.handler] &&
      (!field.value || !validationTypes[validation.handler](field.value))
    ) {
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
}

function validateForm(validationList) {
  let result = true;
  for (let validationItem of validationList) {
    const field = document.querySelector(`[name=${validationItem.field}]`);
    field.addEventListener("keyup", () => {
      validateField(field, validationItem.validations);
    });
    if (!validateField(field, validationItem.validations)) {
      result = false;
    }
  }
  return result;
}

function showToastMessage(msg, type) {
  const mainToast = document.getElementById("mainToast");
  mainToast.classList.remove("text-bg-warning");
  mainToast.classList.remove("text-bg-success");
  const msgTypes = {
    success: "text-bg-success",
    warning: "text-bg-warning",
  };
  mainToast.classList.add(msgTypes[type]);
  const mainToastMsg = mainToast.querySelector(".toast-body");
  mainToastMsg.textContent = msg;
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(mainToast);
  toastBootstrap.show();
}

function sendFormData(form, toastMsg = "") {
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
        showToastMessage(toastMsg, "success");
        navigateTo(form.target);
      } else {
        showToastMessage("Falha na validação do formulário", "warning");
      }
    });
}
