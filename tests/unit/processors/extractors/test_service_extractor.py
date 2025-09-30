import pytest

from ctfbridge.models.challenge import Challenge, Service, ServiceType
from ctfbridge.processors.extractors.services import ServiceExtractor


@pytest.fixture
def extractor():
    return ServiceExtractor()


@pytest.fixture
def basic_challenge():
    return Challenge(id="test", name="Test Challenge", description="", points=100, categories=[])


def test_can_handle(extractor, basic_challenge):
    # Should not handle empty description
    assert not extractor.can_handle(basic_challenge)

    # Should handle if has description
    basic_challenge.description = "Has service"
    assert extractor.can_handle(basic_challenge)


def test_extract_netcat_service(extractor, basic_challenge):
    # Test various nc formats
    formats = [
        "nc localhost 1234",
        "netcat localhost 1234",
        "NC localhost 1234",
        "nc -v localhost 1234",
        "nc -nv localhost 1234",
    ]

    for cmd in formats:
        basic_challenge.services = []
        basic_challenge.description = f"Connect using: {cmd}"
        result = extractor.apply(basic_challenge)
        assert len(result.services) == 1
        service = result.services[0]
        assert service.type == ServiceType.TCP
        assert service.host == "localhost"
        assert service.port == 1234
        assert cmd in service.raw


def test_extract_telnet_service(extractor, basic_challenge):
    basic_challenge.description = "Connect: telnet challenge.com 23"
    result = extractor.apply(basic_challenge)
    assert len(result.services) == 1
    service = result.services[0]
    assert service.type == ServiceType.TELNET
    assert service.host == "challenge.com"
    assert service.port == 23


def test_extract_ftp_service(extractor, basic_challenge):
    # Test with explicit port
    basic_challenge.services = []
    basic_challenge.description = "FTP server: ftp files.ctf.com 2121"
    result = extractor.apply(basic_challenge)
    assert len(result.services) == 1
    service = result.services[0]
    assert service.type == ServiceType.FTP
    assert service.host == "files.ctf.com"
    assert service.port == 2121

    # Test with default port
    basic_challenge.services = []
    basic_challenge.description = "FTP: ftp storage.ctf.com"
    result = extractor.apply(basic_challenge)
    assert len(result.services) == 1
    service = result.services[0]
    assert service.type == ServiceType.FTP
    assert service.host == "storage.ctf.com"
    assert service.port == 21


def test_extract_ssh_service(extractor, basic_challenge):
    # Test various SSH formats
    cases = [
        ("ssh server.ctf.com", "server.ctf.com", 22),
        ("ssh -p 2222 server.ctf.com", "server.ctf.com", 2222),
        ("ssh user@server.ctf.com", "server.ctf.com", 22),
        ("ssh -p 2222 user@server.ctf.com", "server.ctf.com", 2222),
    ]

    for cmd, host, port in cases:
        basic_challenge.services = []
        basic_challenge.description = f"Connect: {cmd}"
        result = extractor.apply(basic_challenge)
        assert len(result.services) == 1
        service = result.services[0]
        assert service.type == ServiceType.SSH
        assert service.host == host
        assert service.port == port


def test_extract_http_service(extractor, basic_challenge):
    cases = [
        ("http://web.ctf.com", 80),
        ("https://web.ctf.com", 443),
        ("http://web.ctf.com:8080", 8080),
        ("https://web.ctf.com:8443", 8443),
    ]

    for url, port in cases:
        basic_challenge.services = []
        basic_challenge.description = f"Web service: {url}"
        result = extractor.apply(basic_challenge)
        assert len(result.services) == 1
        service = result.services[0]
        assert service.type == ServiceType.HTTP
        assert service.host == "web.ctf.com"
        assert service.port == port
        assert service.url == url


def test_extract_multiple_services(extractor, basic_challenge):
    # Test multiple services of different types
    basic_challenge.description = """
    Services:
    1. Web interface: http://web.ctf.com:8080
    2. Shell access: ssh -p 2222 user@shell.ctf.com
    3. Admin panel: nc localhost 4444
    """
    result = extractor.apply(basic_challenge)
    assert len(result.services) == 3

    # Check web service
    web = next(s for s in result.services if s.type == ServiceType.HTTP)
    assert web.host == "web.ctf.com"
    assert web.port == 8080

    # Check SSH service
    ssh = next(s for s in result.services if s.type == ServiceType.SSH)
    assert ssh.host == "shell.ctf.com"
    assert ssh.port == 2222

    # Check netcat service
    nc = next(s for s in result.services if s.type == ServiceType.TCP)
    assert nc.host == "localhost"
    assert nc.port == 4444


def test_extract_multiple_similar_services(extractor, basic_challenge):
    # Test multiple services of the same type
    basic_challenge.description = """
    Multiple ports:
    - Main service: nc localhost 1111
    - Debug port: nc localhost 2222
    - Admin port: nc localhost 3333
    """
    result = extractor.apply(basic_challenge)
    assert len(result.services) == 3

    ports = sorted(s.port for s in result.services)
    assert ports == [1111, 2222, 3333]
    assert all(s.type == ServiceType.TCP for s in result.services)
    assert all(s.host == "localhost" for s in result.services)


def test_handle_errors_gracefully(extractor, basic_challenge):
    # Test with invalid port
    basic_challenge.description = "nc localhost invalid_port"
    result = extractor.apply(basic_challenge)
    assert not result.services  # Should not crash

    # Test with missing host
    basic_challenge.description = "nc :1234"
    result = extractor.apply(basic_challenge)
    assert not result.services  # Should not crash
