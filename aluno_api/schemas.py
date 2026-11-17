from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class AlunoSchema(BaseModel):
    nome: str
    email: EmailStr
    matricula: str
    curso: str


class AlunoPublic(AlunoSchema):
    id: int


class AlunoDB(AlunoSchema):
    id: int


class AlunoList(BaseModel):
    alunos: list[AlunoPublic]
