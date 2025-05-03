
$(function() {
  $("form[name='registro']").validate({
    rules: {
      nombre: "required",
      usuario: "required",
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
        minlength: 10
      }
    },
    messages: {
      nombre: "Por favor, introduzca su nombre",
      usuario: "Por favor, introduzca su usuario",
      password: {
        required: "Por favor proporcione una contraseña",
        minlength: "Su contraseña debe tener al menos 10 caracteres."
      },
      email: {
       required: "Por favor, complete este campo con su correo",
       email: "Por favor, introduce una dirección de correo electrónico válida",
    }
    },
    submitHandler: function(form) {
      form.submit();
    }
  });
});