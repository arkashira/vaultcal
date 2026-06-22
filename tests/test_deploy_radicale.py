import pytest
from src.deploy_radicale import generate_radicale_config, deploy_radicale, main

def test_generate_radicale_config():
    config = generate_radicale_config()
    assert config.tls_certificate == "path/to/tls/certificate"
    assert config.compliance_checklist == "path/to/compliance/checklist"

def test_deploy_radicale_success():
    config = generate_radicale_config()
    success = deploy_radicale(config)
    assert success

def test_deploy_radicale_failure():
    # Simulate a failure by passing a None config
    success = deploy_radicale(None)
    assert not success

def test_main_non_interactive():
    # Simulate running the main function in non-interactive mode
    import sys
    sys.argv = ["deploy_radicale.py", "--non-interactive"]
    main()

def test_main_interactive():
    # Simulate running the main function in interactive mode
    import sys
    sys.argv = ["deploy_radicale.py"]
    main()
