# Aluno API

API em FastAPI para gerenciar alunos de uma instituição de ensino, baseada nos conceitos fundamentais das aulas 01 e 03 do curso **FastAPI do Zero**.

## Requisitos

- Python 3.12+
- [Poetry](https://python-poetry.org/)

## Primeiros passos

```bash
# Instala as dependências do projeto
poetry install

# Inicia o servidor de desenvolvimento com reload automático
poetry run poe serve
```

## API

Os dados são validados estritamente via modelos do **Pydantic** (`AlunoSchema`, `AlunoPublic`, `AlunoDB`, `AlunoList`).

A documentação interativa fica disponível em `/docs` (Swagger UI) e `/redoc` com o servidor rodando.

### Endpoints

| Método | Rota | Código HTTP | Descrição |
| --- | --- | --- | --- |
| `GET` | `/` | 200 OK | Mensagem de boas-vindas (`Olá Mundo!`) |
| `POST` | `/alunos/` | 201 Created | Cadastra um novo aluno |
| `GET` | `/alunos/` | 200 OK | Lista todos os alunos cadastrados |
| `GET` | `/alunos/{aluno_id}` | 200 OK / 404 Not Found | Busca um aluno específico pelo ID |
| `PUT` | `/alunos/{aluno_id}` | 200 OK / 404 Not Found | Atualiza os dados de um aluno |
| `DELETE` | `/alunos/{aluno_id}` | 200 OK / 404 Not Found | Remove um aluno cadastrado |

### Estrutura de Dados do Aluno

- **id**: Identificador numérico único sequencial (`int`)
- **nome**: Nome completo do aluno (`str`)
- **email**: Endereço de e-mail válido com validação de formato (`EmailStr`)
- **matricula**: Matrícula do aluno (`str`)
- **curso**: Nome do curso matriculado (`str`)

## Armazenamento de Dados

O projeto adota uma simulação de banco de dados puramente em memória (`database: list[AlunoDB] = []`), alinhada com as aulas iniciais do curso:

- Os IDs são gerados sequencialmente através de um contador e **nunca são reutilizados** após operações de `DELETE`.
- O estado dos dados é efêmero e volta ao estado inicial ao reiniciar o servidor.

## Tarefas e Qualidade de Código

O projeto utiliza o [Poe the Poet](https://poethepoet.natn.io/) como executor de tarefas:

```bash
# Verificação estática de tipos, regras de lint (Ruff) e ortografia (Typos)
poetry run poe lint

# Formatação automática de código
poetry run poe format

# Execução da suíte completa de testes com relatório de cobertura de código
poetry run poe test
```

### Testes

Os testes são executados com `pytest` utilizando o cliente síncrono `TestClient` do FastAPI, com isolamento completo de estado entre os testes por meio de fixtures automáticas (`autouse=True`) que reiniciam o banco de dados em memória.
