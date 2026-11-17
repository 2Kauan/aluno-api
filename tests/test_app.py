from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_aluno(client):
    response = client.post(
        '/alunos/',
        json={
            'nome': 'João Silva',
            'email': 'joao@example.com',
            'matricula': '2024001',
            'curso': 'Engenharia de Software',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'João Silva',
        'email': 'joao@example.com',
        'matricula': '2024001',
        'curso': 'Engenharia de Software',
    }


def test_create_aluno_com_email_invalido(client):
    response = client.post(
        '/alunos/',
        json={
            'nome': 'João Silva',
            'email': 'email-invalido',
            'matricula': '2024001',
            'curso': 'Engenharia de Software',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_read_alunos_vazio(client):
    response = client.get('/alunos/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'alunos': []}


def test_read_alunos_com_dados(client):
    client.post(
        '/alunos/',
        json={
            'nome': 'Maria Souza',
            'email': 'maria@example.com',
            'matricula': '2024002',
            'curso': 'Ciência da Computação',
        },
    )

    response = client.get('/alunos/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'alunos': [
            {
                'id': 1,
                'nome': 'Maria Souza',
                'email': 'maria@example.com',
                'matricula': '2024002',
                'curso': 'Ciência da Computação',
            }
        ]
    }


def test_read_aluno_por_id_sucesso(client):
    client.post(
        '/alunos/',
        json={
            'nome': 'Lucas Pereira',
            'email': 'lucas@example.com',
            'matricula': '2024003',
            'curso': 'Sistemas de Informação',
        },
    )

    response = client.get('/alunos/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'nome': 'Lucas Pereira',
        'email': 'lucas@example.com',
        'matricula': '2024003',
        'curso': 'Sistemas de Informação',
    }


def test_read_aluno_por_id_nao_encontrado(client):
    response = client.get('/alunos/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Aluno não encontrado'}


def test_update_aluno_sucesso(client):
    client.post(
        '/alunos/',
        json={
            'nome': 'Ana Lima',
            'email': 'ana@example.com',
            'matricula': '2024004',
            'curso': 'Engenharia',
        },
    )

    response = client.put(
        '/alunos/1',
        json={
            'nome': 'Ana Lima Atualizada',
            'email': 'ana.atualizada@example.com',
            'matricula': '2024004',
            'curso': 'Engenharia de Software',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'nome': 'Ana Lima Atualizada',
        'email': 'ana.atualizada@example.com',
        'matricula': '2024004',
        'curso': 'Engenharia de Software',
    }


def test_update_aluno_nao_encontrado(client):
    response = client.put(
        '/alunos/999',
        json={
            'nome': 'Inexistente',
            'email': 'inexistente@example.com',
            'matricula': '0000',
            'curso': 'Nenhum',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Aluno não encontrado'}


def test_delete_aluno_sucesso(client):
    client.post(
        '/alunos/',
        json={
            'nome': 'Carlos Eduardo',
            'email': 'carlos@example.com',
            'matricula': '2024005',
            'curso': 'Design',
        },
    )

    response = client.delete('/alunos/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Aluno deletado'}

    # Verifica que não reutiliza id
    expected_next_id = 2
    post_novo = client.post(
        '/alunos/',
        json={
            'nome': 'Fernanda Alves',
            'email': 'fernanda@example.com',
            'matricula': '2024006',
            'curso': 'Física',
        },
    )
    assert post_novo.json()['id'] == expected_next_id


def test_delete_aluno_nao_encontrado(client):
    response = client.delete('/alunos/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Aluno não encontrado'}
