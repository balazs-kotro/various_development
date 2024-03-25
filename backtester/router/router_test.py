from router.router import Router


def test_router_run(mocker):
    workflow = "workflow"
    mock_route = mocker.MagicMock()
    dummy_routes = {workflow: mock_route}
    router = Router(dummy_routes)
    router.run(workflow=workflow)

    mock_route.assert_called()
