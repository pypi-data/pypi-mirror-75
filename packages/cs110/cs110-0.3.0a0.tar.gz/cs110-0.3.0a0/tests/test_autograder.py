import os.path

import mock

with mock.patch('requests.get') as mock_get, \
     mock.patch('builtins.input') as mock_input:
    from cs110 import autograder


@mock.patch('requests.get')
def test_connected_to_internet(mock_get):
    autograder.connected_to_internet()
    mock_get.assert_called_once_with(autograder.autograder_ping,
                                     timeout=mock.ANY)


def test_get_user_preference():
    autograder.connected = True
    with mock.patch('builtins.input') as mock_input:
        autograder.get_user_preference()
        mock_input.assert_called_once_with("Test against server? [Y/N]: ")

    autograder.connected = False
    autograder.get_user_preference()
    with mock.patch('builtins.print') as mock_print:
        autograder.get_user_preference()
        mock_print.assert_any_call("Not connected to Internet.  "
                                   "Running program locally.")


def test__get_login():
    with mock.patch('os.getlogin') as mock_getlogin, \
         mock.patch('getpass.getuser') as mock_getuser:
        autograder._get_login()
        mock_getlogin.assert_called_once_with()
        mock_getuser.assert_not_called

    with mock.patch('os.getlogin', side_effect=OSError) as mock_getlogin, \
         mock.patch('getpass.getuser') as mock_getuser:
        autograder._get_login()
        mock_getlogin.assert_called_once_with()
        mock_getuser.assert_called_once_with()


@mock.patch('sys.exit')
@mock.patch('requests.post')
@mock.patch('cs110.autograder.get_user_preference', return_value=True)
@mock.patch('cs110.autograder.connected_to_internet', return_value=True)
def test_main(mock_connected_to_internet, mock_get_user_preference,
              mock_post, mock_exit):
    with open(os.path.join(os.path.dirname(__file__),
                           'examples/helloworld_test.py'), 'r') as f:
        test = f.read()

    mock_response = mock.Mock()
    mock_response.json.return_value = {
      'message': test,
      'response_code': 200,
      'timestamp': 0,
    }
    mock_post.return_value = mock_response

    with mock.patch('builtins.print') as mock_print, \
         mock.patch('cs110.autograder.run_testcases',
                    wraps=autograder.run_testcases) as mock_run_testcases, \
         mock.patch('cs110.autograder.run_script',
                    wraps=autograder.run_script) as mock_run_script:
        autograder.main()

    mock_run_testcases.assert_called_once()
    mock_run_script.assert_called_once_with('helloworld.py', mock.ANY)

    mock_print.assert_any_call("Your Program's Output:")
    mock_print.assert_any_call("Hello World\n")
    mock_print.assert_any_call("Feedback:")
    mock_print.assert_any_call("SUCCESS!")

    mock_exit.assert_called_once_with()
