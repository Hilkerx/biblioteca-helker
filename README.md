# Silva'sRead

<img alt="Capa do Projeto Silva'sRead" src="https://github.com/user-attachments/assets/07b1a49f-f835-42bc-b740-43d80e28982b" />

Silva'sRead é uma API back-end desenvolvida em Python com Flask, criada para o gerenciamento de uma biblioteca ou lista de leitura. Este projeto permite que outras aplicações interajam com um catálogo de livros para operações essenciais como criação, leitura, atualização e exclusão de registros.

Este repositório foi configurado conforme as diretrizes da atividade de organização de projetos, aplicando boas práticas de documentação e governança no GitHub para a disciplina de **D.s**.

---

## O que é o projeto?

Silva'sRead é uma API RESTful construída em Python, utilizando o microframework Flask. O objetivo principal é fornecer um conjunto de endpoints para a manipulação de dados de livros, atuando como o núcleo de um sistema de gerenciamento de leitura.

As funcionalidades da API incluem:

* **Criar (Create):** Adicionar novos registros de livros ao sistema.
* **Ler (Read):** Recuperar a lista completa de livros ou detalhes de um livro específico.
* **Atualizar (Update):** Modificar informações de um livro existente.
* **Deletar (Delete):** Remover um livro do catálogo.

A arquitetura visa a separação de responsabilidades, permitindo que a API se concentre na lógica de negócios e persistência de dados, enquanto outras aplicações podem consumir seus serviços.

---

## Visual

(Imagens que demonstram o funcionamento da API. Podem ser prints de ferramentas como Postman ou Insomnia mostrando uma requisição e sua resposta, ou prints do terminal interagindo com a API.)

<img alt="Visual da API em ação" src="https://github.com/user-attachments/assets/339f992e-ee3d-4bcf-804d-9be4b10fa46b" />
<img alt="Exemplo de requisição" src="https://github.com/user-attachments/assets/15668bda-43cc-4613-a4d1-26c6785dcab1" />
<img alt="Exemplo de resposta da API" src="https://github.com/user-attachments/assets/7f5bdef2-b9ea-4656-93c1-e026379791cd" />
<img alt="Outro exemplo de uso da API" src="https://github.com/user-attachments/assets/b4c6f58d-664a-4aab-a9f5-ef0864f60d60" />

**Exemplo de requisição GET (Listar Livros):**
<img alt="Requisição GET para listar livros" src="https://github.com/user-attachments/assets/0ed1b0b8-2a51-41ee-823d-8629af862d2a" />

**Exemplo de requisição POST (Adicionar Livro):**
<img alt="Requisição POST para adicionar livro" src="https://github.com/user-attachments/assets/dd0bc1f2-5ffb-40ca-8131-949d718fe4b9" />
<img alt="Resposta de requisição POST" src="https://github.com/user-attachments/assets/0070a21e-a957-4e02-ad3e-c3cb029f2636" />

---

## Como Rodar (Guia de Início Rápido)

Para executar o projeto localmente, siga os passos abaixo.

**Pré-requisitos:** É necessário ter o Python 3.x e o `pip` instalados no seu sistema.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Hilkerx/biblioteca-helker.git](https://github.com/Hilkerx/biblioteca-helker.git)
    cd biblioteca-helker
    ```

2.  **Instale as dependências:**
    Certifique-se de que o arquivo `requirements.txt` com as dependências do Flask e outras bibliotecas esteja presente na raiz do projeto.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação Flask:**
    Defina a variável de ambiente `FLASK_APP` para o seu arquivo principal da aplicação e inicie o servidor.
    ```bash
    # No macOS/Linux
    export FLASK_APP=app.py # ou o nome do seu arquivo principal
    flask run
    
    # No Windows (Prompt de Comando)
    set FLASK_APP=app.py
    flask run
    ```

4.  **Acesse a API:**
    A aplicação estará disponível em `http://127.0.0.1:5000/`. Utilize seu navegador ou uma ferramenta de teste de API para interagir com os endpoints.

---

## Links Úteis

* **Acesse a Documentação da API (GitHub Pages):** [https://Hilkerx.github.io/biblioteca-helker/](https://Hilkerx.github.io/biblioteca-helker/)
    (Este link é destinado a uma documentação estática sobre a API, como descrição de endpoints, exemplos de uso, etc., e não para a execução da aplicação Flask, que é um back-end.)

* **Link para o Repositório no GitHub:** [https://github.com/Hilkerx/biblioteca-helker](https://github.com/Hilkerx/biblioteca-helker)

---

## Como Contribuir

Contribuições para o projeto Silva'sRead são bem-vindas.

* Para um guia sobre como contribuir, consulte o arquivo [**CONTRIBUTING.md**](CONTRIBUTING.md).
* As diretrizes de conduta para a comunidade estão detalhadas no [**CODE_OF_CONDUCT.md**](CODE_OF_CONDUCT.md).
* Para reportar vulnerabilidades de segurança, siga as instruções em [**SECURITY.md**](SECURITY.md).

Para discussões ou sugestões, utilize as [Issues](https://github.com/Hilkerx/biblioteca-helker/issues) ou as [Discussions](https://github.com/Hilkerx/biblioteca-helker/discussions) do repositório.

---

*Desenvolvido por Helker Silva Chaves Filho*
