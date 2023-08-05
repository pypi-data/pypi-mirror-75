import responses
from click.testing import CliRunner

from smls.constants import SEAMLESS_SERVICE_URL, SEAMLESS_SERVICE_RUN_ROUTE
from smls.seamless import run


@responses.activate
def test_run_command():
    pass
    # response_str = "Running your code seamlessly"
    # request_url = SEAMLESS_SERVICE_URL + SEAMLESS_SERVICE_RUN_ROUTE
    # responses.add(
    #     responses.POST, request_url, body=response_str)
    #
    # runner = CliRunner()
    # result = runner.invoke(run)
    #
    # # The right request was made
    # assert len(responses.calls) == 1
    # assert responses.calls[0].request.url == request_url
    # assert responses.calls[0].response.text == response_str
    #
    # # The cli command printed the response text
    # assert response_str in result.output
