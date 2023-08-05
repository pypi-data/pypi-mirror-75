import subprocess

# TODO: These are integration tests

def test_cli_version():
    # Link: https://janakiev.com/blog/python-shell-commands/
    process = subprocess.run(['wowtool', '--version'], 
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    cli_response = process.stderr
    assert 'There was an error in the CLI' not in cli_response

def test_cli_recording_query():
    process = subprocess.run(['wowtool', 'recording', 'query', '--name', 'Baton-7124602'], 
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    cli_response = process.stderr
    assert 'There was an error in the CLI' not in cli_response

def test_cli_live_query():
    process = subprocess.run(['wowtool', 'live', 'query', '--name', 'Baton-7124602'], 
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    cli_response = process.stderr
    assert 'There was an error in the CLI' not in cli_response

def test_cli_trans_query():
    process = subprocess.run(['wowtool', 'trans', 'query', '--name', 'Baton-7083486'], 
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    cli_response = process.stderr
    assert 'There was an error in the CLI' not in cli_response

def test_cli_resource_validator():
    process = subprocess.run(['wowtool', 'resource', 'validator', '--spec-file', 'tests/fixtures/spec_one_output_template.yaml'], 
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    cli_response = process.stderr
    assert 'There was an error in the CLI' not in cli_response

# def test_cli_create_resource():
#     process = subprocess.run(['wowtool', 'resource', 'create', '--spec-file', 'tests/fixtures/spec_one_output_template.yaml'], 
#                         stdin =subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE, 
#                         universal_newlines=True)
#     cli_response = process.stderr
#     assert 'There was an error in the CLI' not in cli_response

# def test_cli_update_resource():
#     process = subprocess.run(['wowtool', 'resource', 'update', '--spec-file', 'tests/fixtures/spec_one_output_template_updated.yaml'], 
#                             stdin =subprocess.PIPE,
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.PIPE, 
#                             universal_newlines=True)
#     cli_response = process.stderr
#     assert 'There was an error in the CLI' not in cli_response