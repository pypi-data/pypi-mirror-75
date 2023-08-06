'''
Logic for swapping out Azure Key Vault secret identifiers with the secret
values.
'''


# The latter is a known PyLint bug.
# https://github.com/PyCQA/pylint/issues/3507
# pylint: disable=global-statement,isinstance-second-argument-not-valid-type,no-name-in-module


import re
from typing import Dict, Iterable, Tuple, Union
import urllib.parse
from typeguard import typechecked
from pyconfigurableml._core import run_with_specified_config


_CREDENTIALS_ = None
_KEY_VAULT_CLIENT_DICT_ = None


@typechecked
def parse_azure_secret_identifier(secret_identifier: str) -> \
        Tuple[bool, Union[None, str], Union[None, str], Union[None, str]]:
    '''
    Parse the reference to an Azure Key Vault secret (optionally with version).
    The first member of the output will be `True` if parse succeeded, `False`
    otherwise. The other members are (key vault name, secret name, version).
    '''
    parsed = urllib.parse.urlparse(secret_identifier)

    match = re.match(r'([\w\-]+)\.vault\.azure\.net', parsed.netloc)
    if parsed.scheme == 'https' and not parsed.params and not parsed.query \
            and not parsed.fragment and match:
        kv_name = match.groups()[0]
        path = [x for x in parsed.path.split('/') if x]
        secret_name = path[1]
        secret_version = path[2] if len(path) == 3 else None
        return (True, kv_name, secret_name, secret_version)

    return (False, None, None, None)


@typechecked
def _get_azure_secret(kv_name: str,
                      secret_name: str,
                      sec_version: Union[None, str]) -> str:
    global _CREDENTIALS_, _KEY_VAULT_CLIENT_DICT_

    if _KEY_VAULT_CLIENT_DICT_ is None:
        _KEY_VAULT_CLIENT_DICT_ = {}
    if kv_name in _KEY_VAULT_CLIENT_DICT_:
        client = _KEY_VAULT_CLIENT_DICT_[kv_name]
    else:
        from azure.keyvault.secrets import SecretClient
        vault_url = f'https://{kv_name}.vault.azure.net/'
        client = SecretClient(vault_url, _CREDENTIALS_)
        _KEY_VAULT_CLIENT_DICT_[kv_name] = client

    return client.get_secret(secret_name, version=sec_version).value


def _recurse_resolve_azure_secrets(config):
    if isinstance(config, str):
        (success, kv_name, secret_name, ver) = parse_azure_secret_identifier(config)
        if success:
            config = _get_azure_secret(kv_name, secret_name, ver)
    elif isinstance(config, dict):
        config = {k: _recurse_resolve_azure_secrets(v) for (k, v) in config.items()}
    elif isinstance(config, Iterable):
        config = list(map(_recurse_resolve_azure_secrets, config))

    return config


@run_with_specified_config(__name__)
@typechecked
def resolve_azure_secrets(config, inner_config: Dict[str, Union[bool, str]]):
    '''
    Resolve all references to Azure Key Vault secrets with the values of those
    secrets.
    '''

    if inner_config['resolve_secret_identifiers']:
        from azure.identity import DefaultAzureCredential
        global _CREDENTIALS_

        tenant = inner_config['tenant'] if 'tenant' in inner_config else None
        _CREDENTIALS_ = DefaultAzureCredential(shared_cache_tenant_id=tenant)
        config = _recurse_resolve_azure_secrets(config)

    return config
