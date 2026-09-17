function copyPassword() {
    const passwordElement = document.getElementById('passwordOutput');
    const passwordText = passwordElement.innerText;
    
    // Copia a senha da página inicial
    navigator.clipboard.writeText(passwordText).then(() => {
        alert("Senha copiada para a área de transferência!");
    }).catch(err => {
        console.error('Erro ao copiar: ', err);
        alert("Falha ao copiar a senha. Tente copiar manualmente.");
    });
}

// Função para copiar a senha diretamente da tabela de histórico
function copiarSenhaTabela(rowId) {
    // A função recebe o ID da linha, constrói o ID completo (ex: 'senha-row-5')
    const idString = 'senha-row-' + rowId; 
    
    // Busca a linha pelo ID e, dentro dela, encontra o SPAN com o texto da senha
    const senhaElement = document.getElementById(idString).querySelector('.senha-cell-text');
    
    if (!senhaElement) {
        alert("Erro: Senha não encontrada para cópia.");
        return;
    }

    const passwordText = senhaElement.innerText.trim();
    
    // Copia o texto para a área de transferência
    navigator.clipboard.writeText(passwordText).then(() => {
        alert("Senha copiada para a área de transferência!");
    }).catch(err => {
        console.error('Erro ao copiar: ', err);
        alert("Falha ao copiar a senha. Tente copiar manualmente.");
    });
}

// Função para aplicar cores de feedback na página inicial
function aplicarCorForca() {
    const forcaElement = document.getElementById('forcaDisplay');
    if (!forcaElement) return;
    
    const forcaTexto = forcaElement.innerText.trim().toLowerCase();
    let classeCor = '';

    // Mapeamento de texto para classe CSS
    if (forcaTexto.includes('muito forte')) {
        classeCor = 'forca-muito-forte';
    } else if (forcaTexto.includes('forte')) {
        classeCor = 'forca-forte';
    } else if (forcaTexto.includes('média')) {
        classeCor = 'forca-media';
    } else {
        classeCor = 'forca-fraca';
    }
    
    forcaElement.classList.add(classeCor);
}

// Garante que a função de cor é chamada na página inicial
document.addEventListener('DOMContentLoaded', aplicarCorForca);
aplicarCorForca();