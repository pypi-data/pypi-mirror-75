import itkdb


def test_build_url_utils(mocker):
    request = mocker.MagicMock()
    request.url = 'https://itkpd-test.unicorncollege.cz/createTestRunAttachment'
    request.body = b'abytestring'
    assert (
        itkdb.caching.utils.build_url(request)
        == 'https://itkpd-test.unicorncollege.cz/createTestRunAttachment?&body=abytestring'
    )
