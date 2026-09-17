# 🔒 Gerador de Senhas Seguras Web (Python/Flask)

Este é um projeto Full-Stack básico construído com **Python e Flask** para gerar, analisar e gerenciar senhas de forma segura e organizada. É um ótimo exemplo de aplicação CRUD (Create, Read, Update, Delete) com persistência de dados.

## 🚀 Funcionalidades Chave

* **Geração de Senhas:** Gera senhas aleatórias com base em parâmetros customizáveis (tamanho, inclusão de maiúsculas, números e símbolos).
* **Análise de Força:** Fornece feedback instantâneo e visual (cores) sobre a força da senha gerada.
* **Persistência de Dados (CRUD):** Salva as senhas geradas em um banco de dados **SQLite** com o nome do serviço/site.
* **Histórico Completo:** Permite **visualizar, copiar** e **excluir** registros de senhas salvas.
* **Usabilidade:** Mantém o estado do formulário após a submissão e usa código **modular** (Python, HTML, CSS e JavaScript separados).

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Backend** | Python 3 | Linguagem principal do servidor. |
| **Framework** | Flask | Micro-framework leve para roteamento e servidor. |
| **Banco de Dados** | SQLite3 | Banco de dados relacional leve e nativo do Python. |
| **Frontend** | HTML5, CSS3, JavaScript | Interface de usuário e lógica de cópia/cores. |

## ⚙️ Como Rodar o Projeto Localmente

1.  **Clone o Repositório:**
    ```bash
    git clone [COLE O LINK DO SEU REPOSITÓRIO AQUI]
    cd gerador-de-senhas-web
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # (Mac/Linux)
    # .\venv\Scripts\activate  # (Windows PowerShell)
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a Aplicação:**
    ```bash
    python3 -m flask run
    ```

5.  **Acesse:** Abra seu navegador em `http://127.0.0.1:5000/`.

---

Com o `.gitignore` e o `README.md` criados, seu projeto está totalmente pronto para o último passo: **enviar para o GitHub** (Passo 4 da instrução anterior)! Siga aqueles comandos e seu projeto estará online!