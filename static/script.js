// Encontra o botão e o formulário pelos IDs definidos no HTML.
const alternar = document.querySelector("#alternar");
const formulario = document.querySelector("#cadastro-evento");

// Configura o comportamento quando os dois elementos existem.
if (alternar && formulario) {

    // Mostra o botão que estava com o atributo hidden.
    alternar.hidden = false;

    // Executa esta função a cada clique no botão.
    alternar.addEventListener("click", () => {

        // Inverte a visibilidade do formulário.
        formulario.hidden = !formulario.hidden;
    });
}