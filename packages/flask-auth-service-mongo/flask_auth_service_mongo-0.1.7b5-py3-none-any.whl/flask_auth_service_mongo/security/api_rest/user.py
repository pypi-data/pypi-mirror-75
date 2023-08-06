from flask import request
from .. import auth
from ..use_cases import EditPasswordUser


def edit_password_user():
    """Edit password :obj:`User` for API Rest

    Request example
    ::
        {
            'current_password': 'pass',
            'new_password': 'new_pass',
            'password_confirmed': 'new_pass'
        }

    Returns:
        (dict, int): (data, http_code)
    """
    user = auth.current_user()
    data = request.get_json()
    data['id'] = str(user.id)

    use_case = EditPasswordUser()
    result = use_case.handle(data)

    response = {
        'message': result.message
    }
    if result.errors:
        response['errors'] = result.errors

    return response, result.http_code
