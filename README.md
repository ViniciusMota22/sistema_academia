# Sistema Academia — Versão Premium

Sistema web para gerenciamento de academia, desenvolvido com Flask, SQLAlchemy e PostgreSQL.

## Funcionalidades

- Dashboard moderno com indicadores, gráficos e registros recentes
- CRUD completo de alunos
- CRUD completo de planos
- Listagem e cadastro manual de matrículas
- Matrícula gerada automaticamente ao cadastrar um aluno
- Bloqueio de matrícula manual duplicada
- Pesquisa de alunos em tempo real
- Máscaras automáticas de CPF e telefone
- Modal personalizado para confirmar exclusões
- Tema claro e escuro
- Layout responsivo para computador e celular
- Pronto para GitHub e Render

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- HTML5
- CSS3
- JavaScript
- Gunicorn
- Render

## Estrutura principal

```text
sistema_academia/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── Procfile
├── render.yaml
├── .env.example
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   ├── img/
│   └── media/
└── templates/
```

## Como executar localmente

### 1. Criar o ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 3. Criar o arquivo `.env`

Copie o `.env.example` e renomeie a cópia para `.env`.

```env
DATABASE_URL=sua_string_de_conexao_postgresql
```

### 4. Executar

```powershell
python app.py
```

Acesse:

```text
http://127.0.0.1:5000
```

## Deploy no Render

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Environment Variables:
  - `DATABASE_URL`

O arquivo `.env` e a pasta `venv` já estão protegidos pelo `.gitignore` e não devem ser enviados ao GitHub.

## Autor

Vinícius Costa

## Pacote visual WebP

Esta versão utiliza imagens WebP otimizadas em `static/img/webp/` para o banner do dashboard, cards, telas vazias e planos Básico, Premium e VIP. Os arquivos foram preparados com transparência quando necessário para reduzir o peso sem perder o visual.
