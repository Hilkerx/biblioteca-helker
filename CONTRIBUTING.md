# Como Contribuir para o Silva'sRead

Bem-vindo(a) ao projeto Silva'sRead! Sua contribuição é muito valiosa para o aprimoramento desta API.
Este documento descreve as diretrizes para contribuir com o código, reportar problemas e sugerir melhorias.

## Antes de Começar

* Por favor, revise o [Código de Conduta](CODE_OF_CONDUCT.md) do projeto. Esperamos que todos os colaboradores sigam estas diretrizes para manter um ambiente respeitoso e produtivo.
* Certifique-se de que você tem uma conta no GitHub.

## Como Reportar um Problema (Issue)

Se você encontrou um bug, tem uma sugestão de nova funcionalidade ou alguma dúvida, por favor, abra uma nova "Issue" no repositório.

1.  Vá para a aba [Issues](https://github.com/Hilkerx/biblioteca-helker/issues) do repositório.
2.  Clique em "New Issue".
3.  Escolha o template apropriado (se disponível) ou descreva seu problema/sugestão com o máximo de detalhes possível:
    * **Para bugs:** Explique os passos para reproduzir o erro, qual o comportamento esperado e qual o comportamento observado. Inclua mensagens de erro, logs ou prints, se houver.
    * **Para novas funcionalidades:** Descreva a funcionalidade, por que ela seria útil e como ela poderia ser implementada (opcional).

## Como Contribuir com Código

Se você deseja contribuir com código (correções de bugs, novas funcionalidades, melhorias), siga o fluxo de trabalho abaixo:

1.  **Faça um Fork do Repositório:**
    Clique no botão "Fork" no canto superior direito do repositório do Silva'sRead para criar uma cópia em sua conta.

2.  **Clone o seu Fork:**
    Clone o repositório forkado para sua máquina local.
    ```bash
    git clone [https://github.com/](https://github.com/)[SEU_USUARIO_GITHUB]/biblioteca-helker.git
    cd biblioteca-helker
    ```

3.  **Crie uma Nova Branch:**
    Crie uma branch para a sua contribuição. Use um nome descritivo (ex: `feature/nova-funcionalidade` ou `bugfix/correcao-endpoint`).
    ```bash
    git checkout -b nome-da-sua-branch
    ```

4.  **Instale as Dependências:**
    Certifique-se de que todas as dependências do projeto estejam instaladas.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Faça suas Alterações:**
    Implemente suas modificações ou adicione novas funcionalidades. Certifique-se de que seu código siga o estilo do projeto e inclua comentários quando necessário.

6.  **Teste Suas Alterações:**
    Se possível, adicione testes unitários ou de integração para suas mudanças e/ou execute os testes existentes para garantir que nada foi quebrado.

7.  **Commit Suas Alterações:**
    Escreva mensagens de commit claras e concisas que descrevam o que foi feito.
    ```bash
    git add .
    git commit -m "feat: Adiciona nova funcionalidade X"
    # ou "fix: Corrige bug no endpoint Y"
    ```

8.  **Envie para o seu Fork:**
    ```bash
    git push origin nome-da-sua-branch
    ```

9.  **Abra um Pull Request (PR):**
    Vá para a página do seu fork no GitHub. Você verá um botão "Compare & pull request" ao lado da sua nova branch. Clique nele para abrir um Pull Request para o repositório original.
    * Forneça um título descritivo e uma descrição detalhada das suas mudanças.
    * Referencie quaisquer Issues relacionadas (ex: `Closes #123`).

## Revisão do Código

Seu Pull Request será revisado por um mantenedor do projeto. Podemos solicitar alterações ou esclarecimentos. Assim que aprovado, suas mudanças serão integradas à branch principal.

## Dúvidas

Se tiver alguma dúvida sobre como contribuir, não hesite em perguntar abrindo uma [Discussão](https://github.com/Hilkerx/biblioteca-helker/discussions) no repositório.

Agradecemos sua colaboração para tornar o Silva'sRead ainda melhor!
