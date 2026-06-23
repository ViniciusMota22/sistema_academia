document.addEventListener("DOMContentLoaded", function () {
    const cpfInputs = document.querySelectorAll('input[name="cpf"]');
    const telefoneInputs = document.querySelectorAll('input[name="telefone"]');
    const busca = document.getElementById("busca");

    cpfInputs.forEach(input => {
        input.addEventListener("input", function () {
            let valor = input.value.replace(/\D/g, "");
            valor = valor.substring(0, 11);
            valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
            valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
            valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
            input.value = valor;
        });
    });

    telefoneInputs.forEach(input => {
        input.addEventListener("input", function () {
            let valor = input.value.replace(/\D/g, "");
            valor = valor.substring(0, 11);
            valor = valor.replace(/(\d{2})(\d)/, "($1) $2");
            valor = valor.replace(/(\d{5})(\d)/, "$1-$2");
            input.value = valor;
        });
    });

    if (busca) {
        busca.addEventListener("keyup", function () {
            const texto = busca.value.toLowerCase();
            const linhas = document.querySelectorAll("tbody tr");

            linhas.forEach(linha => {
                linha.style.display = linha.innerText.toLowerCase().includes(texto) ? "" : "none";
            });
        });
    }
});
