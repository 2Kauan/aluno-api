from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from aluno_api.schemas import (
    AlunoDB,
    AlunoList,
    AlunoPublic,
    AlunoSchema,
    Message,
)

app = FastAPI(
    title='Sistema de Gerenciamento de Alunos',
    description='API para gerenciamento de alunos desenvolvida com FastAPI',
)

database: list[AlunoDB] = []
_id_counter = [0]


def get_next_id() -> int:
    _id_counter[0] += 1
    return _id_counter[0]


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/alunos/',
    status_code=HTTPStatus.CREATED,
    response_model=AlunoPublic,
    tags=['alunos'],
)
def create_aluno(aluno: AlunoSchema):
    new_id = get_next_id()
    aluno_db = AlunoDB(
        id=new_id,
        nome=aluno.nome,
        email=aluno.email,
        matricula=aluno.matricula,
        curso=aluno.curso,
    )
    database.append(aluno_db)
    return aluno_db


@app.get(
    '/alunos/',
    status_code=HTTPStatus.OK,
    response_model=AlunoList,
    tags=['alunos'],
)
def read_alunos():
    return {'alunos': database}


@app.get(
    '/alunos/{aluno_id}',
    status_code=HTTPStatus.OK,
    response_model=AlunoPublic,
    tags=['alunos'],
)
def read_aluno(aluno_id: int):
    for aluno in database:
        if aluno.id == aluno_id:
            return aluno

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Aluno não encontrado',
    )


@app.put(
    '/alunos/{aluno_id}',
    status_code=HTTPStatus.OK,
    response_model=AlunoPublic,
    tags=['alunos'],
)
def update_aluno(aluno_id: int, aluno: AlunoSchema):
    for index, current_aluno in enumerate(database):
        if current_aluno.id == aluno_id:
            aluno_atualizado = AlunoDB(
                id=aluno_id,
                nome=aluno.nome,
                email=aluno.email,
                matricula=aluno.matricula,
                curso=aluno.curso,
            )
            database[index] = aluno_atualizado
            return aluno_atualizado

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Aluno não encontrado',
    )


@app.delete(
    '/alunos/{aluno_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    tags=['alunos'],
)
def delete_aluno(aluno_id: int):
    for index, current_aluno in enumerate(database):
        if current_aluno.id == aluno_id:
            del database[index]
            return {'message': 'Aluno deletado'}

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Aluno não encontrado',
    )
