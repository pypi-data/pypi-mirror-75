def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,icinga-host,wekan-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="wekan",
        help="service"
    )
