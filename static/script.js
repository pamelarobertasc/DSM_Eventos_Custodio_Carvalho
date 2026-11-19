// Localiza o botão e o formulário na página.
const alternar = document.querySelector("#alternar");
const formulario = document.querySelector("#cadastro-evento");

// Executa somente nas páginas que possuem o formulário de eventos.
if (formulario) {

    // Localiza os elementos usados para atualizar a página.
    const atualizar = document.querySelector("#atualizar");
    const resultados = document.querySelector("#resultados");
    const retorno = document.querySelector("#retorno");

    // Lê o token da sessão e o endereço da API.
    const token = document.querySelector('meta[name="csrf-token"]').content;
    const api = formulario.dataset.api;

    // Mostra os botões que dependem do JavaScript.
    alternar.hidden = false;
    atualizar.hidden = false;

    // Alterna a visibilidade do formulário.
    alternar.addEventListener("click", () => {
        formulario.hidden = !formulario.hidden;
    });


    // Faz uma requisição e devolve os dados recebidos em JSON.
    async function requisitar(url, opcoes = {}) {
        let resposta;

        try {
            // Espera até dez segundos pela resposta do servidor.
            resposta = await fetch(url, {
                ...opcoes,
                signal: AbortSignal.timeout(10000)
            });
        } catch {
            throw new Error(
                "Sem resposta do servidor. Confira a conexão."
            );
        }

        let dados;

        try {
            // Converte a resposta JSON em dados do JavaScript.
            dados = await resposta.json();
        } catch {
            throw new Error(
                "O servidor enviou uma resposta inesperada."
            );
        }

        // Status como 400 ou 401 são tratados como falhas.
        if (!resposta.ok) {
            throw new Error(
                dados.erro || "O servidor recusou a operação."
            );
        }

        return dados;
    }


    // Reconstrói somente a área da lista de eventos.
    function desenhar(eventos) {
        resultados.replaceChildren();

        // Mostra uma mensagem quando a lista está vazia.
        if (eventos.length === 0) {
            resultados.textContent = "Nenhum evento cadastrado.";
            return;
        }

        // Cria o texto com a quantidade de eventos.
        const quantidade = document.createElement("p");
        quantidade.textContent = `Total de eventos: ${eventos.length}`;

        // Cria a lista que receberá os eventos.
        const lista = document.createElement("ul");

        for (const evento of eventos) {
            const item = document.createElement("li");

            // textContent exibe os valores como texto.
            // O operador ?? preserva zero como quantidade válida.
            item.textContent =
                `${evento.nome} — ${evento.data} — ` +
                `${evento.local || "Local não informado"} — ` +
                `Vagas: ${evento.vagas ?? "Não informadas"} `;

            // Monta o link de edição com o ID do evento.
            const editar = document.createElement("a");
            editar.textContent = "Editar";
            editar.href = formulario.dataset.editar.replace(
                /0$/,
                String(evento.id)
            );

            item.append(editar);

            // O HTML fornece esse endereço somente para admin.
            if (formulario.dataset.excluir) {
                const excluir = document.createElement("form");
                excluir.method = "post";
                excluir.action = formulario.dataset.excluir.replace(
                    /0$/,
                    String(evento.id)
                );

                // Mantém o token no formulário de exclusão.
                const campoToken = document.createElement("input");
                campoToken.type = "hidden";
                campoToken.name = "csrf_token";
                campoToken.value = token;

                const botaoExcluir = document.createElement("button");
                botaoExcluir.type = "submit";
                botaoExcluir.textContent = "Excluir";

                excluir.append(campoToken, botaoExcluir);
                item.append(excluir);
            }

            lista.append(item);
        }

        resultados.append(quantidade, lista);
    }


    // Consulta a API ao clicar em Atualizar.
    atualizar.addEventListener("click", async () => {
        atualizar.disabled = true;
        retorno.textContent = "Atualizando...";

        try {
            const eventos = await requisitar(api);
            desenhar(eventos);
            retorno.textContent = "Lista atualizada.";
        } catch (erro) {
            retorno.textContent = erro.message;
        } finally {
            // Libera o botão mesmo quando ocorre um erro.
            atualizar.disabled = false;
        }
    });


    // Intercepta o envio do cadastro para usar fetch.
    formulario.addEventListener("submit", async (evento) => {
        // Impede a navegação tradicional do formulário.
        evento.preventDefault();

        const botaoCadastrar = formulario.querySelector(
            'button[type="submit"]'
        );

        // Evita um segundo envio enquanto o primeiro está em andamento.
        if (botaoCadastrar.disabled) {
            return;
        }

        botaoCadastrar.disabled = true;
        retorno.textContent = "Cadastrando...";

        try {
            // Reúne os campos do formulário em um objeto.
            const dados = Object.fromEntries(
                new FormData(formulario)
            );

            // O token será enviado no cabeçalho.
            delete dados.csrf_token;

            // Envia o cadastro como JSON.
            await requisitar(api, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": token
                },
                body: JSON.stringify(dados)
            });

            // Limpa os campos após a confirmação do cadastro.
            formulario.reset();

            try {
                // Consulta a lista atualizada após gravar.
                const eventos = await requisitar(api);
                desenhar(eventos);
                retorno.textContent = "Evento cadastrado!";
            } catch {
                // Informa que a gravação ocorreu mesmo se a consulta falhar.
                retorno.textContent =
                    "Evento salvo. Clique em Atualizar para consultar a lista.";
            }
        } catch (erro) {
            // Mantém os campos preenchidos para permitir correção.
            retorno.textContent = erro.message;
        } finally {
            botaoCadastrar.disabled = false;
        }
    });
}