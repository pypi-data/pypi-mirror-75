from unittest import TestCase
from unittest.mock import patch, Mock
from ....use_cases.user import (
    LoginResponse,
    Login,
    Logout,
    CreateUser,
    SaveUserResponse,
    EditUser,
    DeleteUser,
    Response
)
from ....models import User


def resolve_patch(path: str) -> str:
    return 'flask_auth_service_mongo.security.use_cases.user.{}'.format(path)


class TestLogin(TestCase):

    def test_request_not_valid(self):
        use_case = Login()
        request = dict(
            key='value'
        )
        result = use_case.handle('role', request)
        expected = {'key': ['unknown field'],
                    'password': ['required field'],
                    'username': ['required field']
                    }

        self.assertIsInstance(result, LoginResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, expected)
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find_one'))
    def test_user_not_found(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = None

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle('role', request)

        # asserts
        mock_user_find.assert_called_with(
            username=request['username'].lower()
        )
        self.assertIsInstance(result, LoginResponse)
        self.assertEqual(result.message, 'bad_credentials')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find_one'))
    def test_incorrect_role(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = Mock(name='other_role')

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle('role', request)

        # asserts
        mock_user_find.assert_called_with(
            username=request['username'].lower()
        )
        self.assertIsInstance(result, LoginResponse)
        self.assertEqual(result.message, 'bad_credentials')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_incorrect_password(self, mock_user_find, mock_password_match):
        # Mocks
        user = Mock(password='pass')
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = False

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle('role', request)

        # asserts
        mock_user_find.assert_called_with(
            username=request['username'].lower()
        )
        mock_password_match.assert_called_with(request['password'], 'pass')
        self.assertIsInstance(result, LoginResponse)
        self.assertEqual(result.message, 'bad_credentials')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('WhitelistToken'))
    @patch(resolve_patch('token_generate'))
    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_ok(
        self,
        mock_user_find,
        mock_password_match,
        mock_token_generate,
        mock_whitelist
    ):
        # Mocks
        user = Mock(password='hash_pass')
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = True
        mock_token_generate.return_value = 'the_token'

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle('role', request)

        # asserts
        _, kwargs = mock_whitelist.call_args
        self.assertEqual(kwargs['token'], 'the_token')
        self.assertIsNotNone(kwargs['created_at'])
        mock_user_find.assert_called_with(
            username=request['username'].lower()
        )
        mock_password_match.assert_called_with('test_pass', 'hash_pass')
        self.assertIsInstance(result, LoginResponse)
        self.assertEqual(result.message, 'ok')
        self.assertEqual(result.http_code, 200)
        self.assertEqual(result.token, 'the_token')


class TestLogout(TestCase):

    @patch(resolve_patch('WhitelistTokenRepository.find_one'))
    def test_ok(self, mock_find):
        # Mocks
        mock_token = Mock()
        mock_token.delete.return_value = True
        mock_find.return_value = mock_token

        use_case = Logout()
        result = use_case.handle('a_token')

        # Asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.http_code, 200)
        self.assertEqual(result.message, 'ok')
        mock_find.assert_called_with(token='a_token')
        mock_token.delete.assert_called_with()


class TestCreateUser(TestCase):

    def test_request_not_valid(self):
        use_case = CreateUser()
        result = use_case.handle({'key': 'value'})

        expected = {'key': ['unknown field'],
                    'password': ['required field'],
                    'password_confirmed': ['required field'],
                    'role': ['required field'],
                    'username': ['required field']}

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, expected)
        self.assertEqual(result.http_code, 400)

    def test_username_not_valid(self):
        use_case = CreateUser()
        request = {
            'username': '12',
            'password': '1234',
            'password_confirmed': '1234',
            'role': 'any'
        }
        result = use_case.handle(request)

        expected = {'username': [
            'min length is 3']
        }

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, expected)
        self.assertEqual(result.http_code, 400)

    def test_passwords_not_match(self):
        request = dict(
            username='str',
            role='str',
            password='pass',
            password_confirmed='1234'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Passwords don't match")
        self.assertEqual(result.http_code, 406)

    @patch(resolve_patch('Role'))
    def test_rol_not_found(self, mock_role):
        # Mocks
        mock_first = Mock()
        mock_first.first = Mock(return_value=None)
        mock_role.objects = Mock(return_value=mock_first)

        request = dict(
            username='str',
            role='notExists',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Role does not exist")
        self.assertEqual(result.http_code, 406)
        mock_role.objects.assert_called()

    @patch(resolve_patch('User'))
    @patch(resolve_patch('Role'))
    def test_user_repeated(self, mock_role, mock_user):
        request = dict(
            username='exisTs',
            role='rol',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Username already exists")
        self.assertEqual(result.http_code, 406)
        mock_user.objects.assert_called_with(username='exists')

    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('User.objects'))
    @patch(resolve_patch('Role.objects'))
    def test_ok(self, mock_role_objects, mock_user_objects,
                mock_user_save):
        # Mocks
        mock_user_list = Mock()
        mock_user_list.first = Mock(return_value=None)
        mock_user_objects.return_value = mock_user_list

        mock_list_role = Mock()
        mock_list_role.first.return_value = 'a role'
        mock_role_objects.return_value = mock_list_role

        request = dict(
            username='str',
            role='a role',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)
        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "created")
        self.assertEqual(result.http_code, 201)
        self.assertIsInstance(result.user, User)

    @patch(resolve_patch('CreateUser._create_user'), *{
        'return_value.objects.side_effect': Exception()
    })
    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('User.objects'))
    @patch(resolve_patch('Role'))
    def test_except(self, mock_role, mock_user_objects,
                    mock_user_save):
        # Mocks
        mock_first = Mock()
        mock_first.first = Mock(return_value=None)
        mock_user_objects.return_value = mock_first

        request = dict(
            username='str',
            role='aRole',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "internal_server_error")
        self.assertEqual(result.http_code, 500)
        self.assertIsNone(result.user)


class TestEditUser(TestCase):

    def test_request_not_valid(self):
        use_case = EditUser()
        result = use_case.handle('uuid', {'key': 'value'})

        expected = {
            'key': ['unknown field'],
            'password': ['required field'],
            'password_confirmed': ['required field']
            }
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, str(expected))
        self.assertEqual(result.http_code, 400)

    def test_passwords_not_valid(self):
        use_case = EditUser()
        # pass con espacios
        request = dict(
            password=' dp33',
            password_confirmed='123'
        )
        result = use_case.handle('uuid', request=request)
        expected = {'password': ['Must not contain spaces']
                    }
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, str(expected))
        self.assertEqual(result.http_code, 400)

    def test_passwords_not_match(self):
        request = dict(
            password='pass',
            password_confirmed='1234'
        )
        use_case = EditUser()
        result = use_case.handle(uuid='uuid', request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Passwords don't match")
        self.assertEqual(result.http_code, 406)

    @patch(resolve_patch('User.objects'))
    def test_not_found(self, mock_user_objects):
        # Mocks
        mock_first = Mock()
        mock_first.first = Mock(return_value=None)
        mock_user_objects.return_value = mock_first

        request = dict(
            password='pass',
            password_confirmed='pass'
        )
        use_case = EditUser()
        result = use_case.handle(uuid='uuid', request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'not_found')
        self.assertEqual(result.http_code, 404)
        mock_user_objects.assert_called_with(id='uuid')

    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('User.objects'))
    def test_ok(self, mock_user_objects, mock_user_save):
        # Mocks
        user = User()
        mock_first = Mock()
        mock_first.first = Mock(return_value=user)
        mock_user_objects.return_value = mock_first

        request = dict(
            password='pass',
            password_confirmed='pass'
        )
        use_case = EditUser()
        result = use_case.handle(uuid='uuid', request=request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "ok")
        self.assertEqual(result.http_code, 200)
        self.assertEqual(result.user, user)
        mock_user_save.assert_called_with()

    @patch(resolve_patch('EditUser._edit'), *{
        'return_value.objects.side_effect': Exception()
    })
    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('User.objects'))
    def test_except(self, mock_user_objects, mock_user_save):
        # Mocks
        user = User()
        mock_first = Mock()
        mock_first.first = Mock(return_value=user)
        mock_user_objects.return_value = mock_first

        request = dict(
            password='pass',
            password_confirmed='pass'
        )
        use_case = EditUser()
        result = use_case.handle(uuid='uuid', request=request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "internal_server_error")
        self.assertEqual(result.http_code, 500)
        self.assertIsNone(result.user)


class TestDeleteUser(TestCase):
    _config = Mock()
    _logger = Mock()
    @patch(resolve_patch('User.objects'))
    def test_not_found(self, mock_user_objects):
        # Mocks
        mock_first = Mock()
        mock_first.first = Mock(return_value=None)
        mock_user_objects.return_value = mock_first

        use_case = DeleteUser()
        result = use_case.handle(uuid='uuid')

        self.assertIsInstance(result, Response)
        self.assertEqual(result.message, 'not_found')
        self.assertEqual(result.http_code, 404)
        mock_user_objects.assert_called_with(id='uuid')

    @patch(resolve_patch('User.delete'))
    @patch(resolve_patch('User.objects'))
    def test_ok(self, mock_user_objects, mock_user_delete):
        # Mocks
        user = User()
        mock_first = Mock()
        mock_first.first = Mock(return_value=user)
        mock_user_objects.return_value = mock_first

        use_case = DeleteUser()
        result = use_case.handle(uuid='uuid')

        # asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.message, "ok")
        self.assertEqual(result.http_code, 200)
        mock_user_delete.assert_called_with()

    @patch(resolve_patch('User.delete'), *{
        'return_value.objects.side_effect': Exception()
    })
    @patch(resolve_patch('User.delete'))
    @patch(resolve_patch('User.objects'))
    def test_except(self, mock_user_objects, mock_user_delete):
        # Mocks
        user = User()
        mock_first = Mock()
        mock_first.first = Mock(return_value=user)
        mock_user_objects.return_value = mock_first

        use_case = DeleteUser()
        result = use_case.handle(uuid='uuid')

        # asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.message, "internal_server_error")
        self.assertEqual(result.http_code, 500)
