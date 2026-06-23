# Sistema Academia

Projeto final de Banco de Dados desenvolvido com Flask, SQLAlchemy e PostgreSQL Neon.

## Funcionalidades

- Dashboard com estatísticas
- CRUD completo de Alunos
- CRUD completo de Planos
- Cadastro e listagem de Matrículas
- Pesquisa de alunos em tempo real
- Máscara automática de CPF e telefone com JavaScript
- Layout responsivo com HTML e CSS
- Conexão com banco PostgreSQL Neon

## Tecnologias

- Python
- Flask
- SQLAlchemy
- PostgreSQL Neon
- HTML
- CSS
- JavaScript

## Como rodar o projeto

1. Crie e ative o ambiente virtual:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sua_string_do_neon
SECRET_KEY=sua_chave_secreta
```

4. Execute o sistema:

```bash
python app.py
```

5. Acesse no navegador:

```txt
http://127.0.0.1:5000
```

## Autor

- Vinícius
