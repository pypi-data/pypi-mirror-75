import argparse
import json
from getpass import getpass

import jwt
import datetime
import sys
import os
import platform
import requests
import time
from faas.core import FaasAPIClient, Configuration
from cli import __version__ as version

if platform.system() == 'Windows':
    import colorama

    colorama.init()


# ------- Print version command -------
def print_version(args=None, api_client=None):
    print('======================================')
    print('======= Sonra Intelligence Ltd =======')
    print('=======    FaaS Python SDK     =======')
    print(f'=======     version {version}      =======')
    print('======================================')
    return None


# ------- Check the token validity -------
def check_access(args, api_client):
    _config_client = Configuration()
    setattr(_config_client, 'config', _config_client.load_config())
    # if config file absent
    if _config_client.config is None:
        print('\033[31mError: To use FaaS you need' +
              ' to log in to the system!\033[0m')
        sys.exit(2)
    # check whether cfg file is valid and not corrupted
    elif isinstance(_config_client.config, dict
                    ) and 'access_token' in _config_client.config.keys(
    ) and 'refresh_token' in _config_client.config:
        api_client.access_token = _config_client.config['access_token']
        api_client.refresh_token = _config_client.config['refresh_token']
    else:
        print('\033[31mError: Your configuration file is corrupted' +
              ' Please provide new log in...\033[0m')
        _config_client.delete_config()
        sys.exit(2)

    _validation_result = validate_expiry(_config_client)
    if _validation_result[1]:
        # -------- Check whether cfg json was overwritten
        # -------- if yes - changes the token pair
        api_client.access_token = _validation_result[2].config[
            'access_token']
        api_client.refresh_token = _validation_result[2].config[
            'refresh_token']
    return _validation_result[0]


# noinspection PyProtectedMember
def login(args, api_client):
    args.username = input('Please enter your email---> '
                          ) if args.username is None else args.username
    args.password = getpass('Please enter your password---> '
                            ) if args.password is None else args.password
    api_client.username = args.username
    api_client.password = args.password
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    token = api_client.get_access_token()
    if not token:
        print('\033[31mError: Invalid FaaS ' +
              'credentials...\033[0m')
        sys.exit(2)
    api_client.access_token = token[0]
    api_client.refresh_token = token[1]
    _config = Configuration()
    setattr(_config, 'config', Configuration.fill_config(api_client))

    _config.save_config()
    if not validate_expiry(_config):
        api_client.logger.warning(
            'FaaS credentials are out of date...Exiting')
        sys.exit(2)
    api_client.logger.warning(time.strftime(
        "%b %d %Y %H:%M:%S", time.localtime()))
    api_client.logger.warning(
        'You have successfully logged into FaaS')
    return None


# ------- Validate the token's expiry date
# ------- Returns tuple:
#   ------- Ist -> expire (True, False)
#   ------- IInd - cfg was overwritten (True, False)
#   ------- IIId - possibly changed token and refresh token
def validate_expiry(_config):
    _token_result = jwt.decode(_config.config['access_token'],
                               verify=False)['exp']
    # valid token
    if datetime.datetime.fromtimestamp(
            _token_result) > datetime.datetime.now():
        return True, False
    # algorithms=['HS256'])
    _token_refresh = jwt.decode(_config.config['refresh_token'],
                                verify=False)['exp']
    # valid refresh_token
    if datetime.datetime.fromtimestamp(
            _token_refresh) > datetime.datetime.now():
        _refresh_result = refresh_token(_config)
        if _refresh_result[0]:
            return True, True, _refresh_result[1]
    print('\033[31mIn vain, your token is' +
          ' out of date. Contact support, please...\033[0m')
    return False, False


# ------- Rewrote user's config file with new refresh token -----
def refresh_token(_config):
    _data = {'grant_type': 'refresh_token',
             'refresh_token': _config.config['refresh_token']}
    _endpoint = 'https://api.sonra.io' if 'endpoint' \
                                          not in _config.config else _config.config['endpoint']

    _resp = requests.post(f'{_endpoint}/oauth/token', _data)
    if _resp.status_code != 200:
        return False,
    _new_config = _resp.json()
    _config.config['access_token'] = _new_config['access_token']
    _config.config['refresh_token'] = _new_config['refresh_token']
    _config.save_config()
    return True, _config



def source_data_create_file(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    data = api_client.create_file_data_source(name=args.name,
                                              _type=args.type, _file=args.file)

    print_json(data)
    return True



def source_connection_create_s3(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    if args.type.lower() not in ['xml', 'json', 'xsd']:
        raise Exception('--type is not valid, it can only be XML, XSD, JSON')

    data = None
    if args.type.lower() == 'xsd':
        data = api_client.create_s3_schema_source(args.name,
                                                  args.path,
                                                  args.role_arn)
    else:
        data = api_client.create_s3_data_source(args.name,
                                                args.type,
                                                args.path,
                                                args.role_arn)
    print_json(data)
    return True


def source_connection_create_http(args, api_client: FaasAPIClient):
    # check if --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    if args.type.lower() not in ['xml', 'json', 'xsd']:
        raise Exception('--type is not valid, it can only be XML, XSD, JSON')

    data = None
    if args.type.lower() == 'xsd':
        data = api_client.create_http_schema_source(args.name, args.url)
    else:
        data = api_client.create_source_http(args.name, args.url, args.type)
    print_json(data)
    return True


# -------> HTTP as data_source object creation
def source_data_create_http(args, api_client: FaasAPIClient):
    # check if --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    data = api_client.create_source_http(args.name,
                                         args.url,
                                         args.type)
    print_json(data)
    return True


# ---------------------------------------------------------------
# check file's extension
# ---------------------------------------------------------------
def check_extension(_name, _ext):
    if not os.path.isfile(_name.path):
        return False

    _extension = _name.name.split('.')[-1]
    if _extension in _ext:
        return True

    return False


# ---------------------------------------------------------------
# call of the specific content help file
# ---------------------------------------------------------------
def print_context_help(args):
    # escape symbols in help *.txt files should be marked as "/033"

    # finding help directory
    _help_path = os.path.sep.join([os.path.dirname(
        os.path.realpath(__file__)), 'help_texts'])

    if not hasattr(args, 'command') or args.command is None:
        # General help
        """
        with os.scandir(_help_path) as _entries: 
            _t_outs = [_entry.name for _entry in _entries
                       if check_extension(_entry, 'txt') and
                       _entry.name.count('_') == 1]
            
            for _help_text in _t_outs:
                print_help_from_file(os.path.sep.join(
                        [_help_path, _help_text]))
        """
        print_help_from_file(os.path.sep.join(
            [_help_path, "faascli_general_help.txt"]))
        sys.exit(2)

    _help_f = ''  # name of the certain help file
    # ------->
    if hasattr(args, 'subcommand') and args.subcommand is None:
        delattr(args, 'subcommand')
    if 'source_connection' in args.command:
        if hasattr(args, 'subcommand'
                   ) and args.subcommand in 'create':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'sc_create_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'list':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'sc_list_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'delete':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'sc_delete_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'get':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'sc_get_help.txt']))
        else:
            print_help_from_file(os.path.sep.join(
                [_help_path, 'source_connection_help.txt']))
    # # ------->
    # elif 'schema_source' in args.command or 'source_schema' in args.command:
    #     if hasattr(args, 'subcommand'
    #                ) and args.subcommand in 'create':
    #         print_help_from_file(os.path.sep.join(
    #             [_help_path, 'ss_create_help.txt']))
    #     elif hasattr(args, 'subcommand'
    #                  ) and args.subcommand in 'list':
    #         print_help_from_file(os.path.sep.join(
    #             [_help_path, 'ss_list_help.txt']))
    #     elif hasattr(args, 'subcommand'
    #                  ) and args.subcommand in 'delete':
    #         print_help_from_file(os.path.sep.join(
    #             [_help_path, 'ss_delete_help.txt']))
    #     elif hasattr(args, 'subcommand'
    #                  ) and args.subcommand in 'get':
    #         print_help_from_file(os.path.sep.join(
    #             [_help_path, 'ss_get_help.txt']))
    #     else:
    #         print_help_from_file(os.path.sep.join(
    #             [_help_path, 'schemasource_help.txt']))
    # # ------->
    elif args.command in 'target_connection':
        if hasattr(args, 'subcommand'
                   ) and args.subcommand in 'create':
            if hasattr(args, 'subcommand2'
                       ) and args.subcommand2 in 'snowflake':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_snowflake_help.txt']))
            elif hasattr(args, 'subcommand2'
                         ) and args.subcommand2 in 'mysql':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_mysql_help.txt']))
            elif hasattr(args, 'subcommand2'
                         ) and args.subcommand2 in 'postgresql':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_postgresql_help.txt']))
            elif hasattr(args, 'subcommand2'
                         ) and args.subcommand2 in 's3':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_s3_help.txt']))
            elif hasattr(args, 'subcommand2'
                         ) and args.subcommand2 in 'sqlserver':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_sqlserver_help.txt']))
            elif hasattr(args, 'subcommand2'
                         ) and args.subcommand2 in 'oracle':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_oracle_help.txt']))
            elif hasattr(args, 'subcommand2'
                         ) and args.subcommand2 in 'redshift':
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_redshift_help.txt']))
            else:
                print_help_from_file(os.path.sep.join(
                    [_help_path, 'tc_create_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'list':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'tc_list_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'delete':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'tc_delete_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'get':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'tc_get_help.txt']))
        else:
            print_help_from_file(os.path.sep.join(
                [_help_path, 'targetconnection_help.txt']))
    # ------->
    elif args.command in 'conversion':
        if hasattr(args, 'subcommand'
                   ) and args.subcommand in 'execute':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'conv_exec_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'execute_upload':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'conv_exec_upload_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'list':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'conv_list_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'delete':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'conv_delete_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'get':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'conv_get_help.txt']))
        else:
            print_help_from_file(os.path.sep.join(
                [_help_path, 'conversion_help.txt']))
    # ------->
    elif args.command in 'login':
        print_help_from_file(os.path.sep.join(
            [_help_path, 'login_help.txt']))
    # ------->
    elif args.command in 'webhook':
        if hasattr(args, 'subcommand'
                   ) and args.subcommand in 'create':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'wh_create_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'list':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'wh_list_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'delete':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'wh_delete_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'get':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'wh_get_help.txt']))
        else:
            print_help_from_file(os.path.sep.join(
                [_help_path, 'webhook_help.txt']))
    # ---> Endpoint help
    elif args.command in 'endpoint':
        print_help_from_file('endpoint_help.txt')
    elif args.command in 'data_flow':
        if hasattr(args, 'subcommand'
                   ) and args.subcommand in 'create':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_create_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'create_upload':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_create_upload_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'list':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_list_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'delete':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_delete_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'get':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_get_help.txt']))
        elif hasattr(args, 'subcommand'
                     ) and args.subcommand in 'trigger':
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_trigger_help.txt']))
        else:
            print_help_from_file(os.path.sep.join(
                [_help_path, 'df_help.txt']))
    sys.exit(2)


# -------> print a content of the certain help file
def print_help_from_file(_file):
    with open(_file) as _txt:
        _content = _txt.read()
        _cont_parts = _content.split('/033')
        _i = 0
        for _part in _cont_parts:
            if _part.startswith('['):
                _cont_parts[_i] = '\033' + _part
            _i += 1

        _content = ''.join(_cont_parts)
        print(_content)

    return None


def source_data_list(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    if args.limit is not None:
        print_json(api_client.list_data_sources(args.limit))
    else:
        print_json(api_client.list_data_sources())
    return None


def source_data_delete(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    print_json(api_client.delete_data_source(args.name))


def source_data_get(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.get_data_source(args.name))


def source_schema_create_file(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    source_schema = api_client.create_file_schema_source(
        name=args.name, file=args.file)
    print_json(source_schema)
    return True


def source_schema_create_http(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    source_schema = api_client.create_http_schema_source(
        name=args.name, url=args.url)
    print_json(source_schema)
    return True


def source_schema_from_s3(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    _source_schema = api_client.create_s3_schema_source(
        name=args.name, path=args.path,
        role_arn=args.role_arn)
    print_json(_source_schema)
    return True


def source_schema_list(args, api_client: FaasAPIClient):
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    if args.limit is not None:
        print_json(api_client.list_schema_sources(args.limit))
    else:
        print_json(api_client.list_schema_sources())
    return None


def source_schema_delete(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.delete_schema_source(args.name))


def source_schema_get(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.get_schema_source(args.name))


def target_connection_create(args):
    print('command=' + args.command)
    print('name=' + args.name)
    print('file=' + args.file)


def target_connection_create_snowflake(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_snowflake_target_connection(
        name=args.name
        , host=args.host
        , username=args.username
        , password=args.password
        , database=args.database
        , warehouse=args.warehouse
        , schema=args.schema
        , role=args.role
    )
    print_json(resp)


def target_connection_create_mysql(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_mysql_target_connection(
        name=args.name
        , host=args.host
        , username=args.username
        , password=args.password
        , database=args.database
    )
    print_json(resp)


def target_connection_create_postgresql(
        args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_postgresql_target_connection(
        name=args.name
        , host=args.host
        , username=args.username
        , password=args.password
        , database=args.database
        , schema=args.schema
    )
    print_json(resp)


def target_connection_create_s3(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_s3_target_connection(
        name=args.name
        , path=args.path
        , role_arn=args.role_arn
    )
    print_json(resp)


def target_connection_create_sqlserver(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_sqlserver_target_connection(
        name=args.name
        , host=args.host
        , username=args.username
        , password=args.password
        , database=args.database
    )
    print_json(resp)


def target_connection_create_oracle(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_oracle_target_connection(
        name=args.name
        , host=args.host
        , username=args.username
        , password=args.password
        , database=args.database
    )
    print_json(resp)


def target_connection_create_redshift(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_redshift_target_connection(
        name=args.name
        , host=args.host
        , username=args.username
        , password=args.password
        , database=args.database
    )
    print_json(resp)


def target_connection_create_bigquery(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    resp = api_client.create_bigquery_target_connection(
        name=args.name
        , dataset=args.dataset
        , storage=args.storage
        , credentials=args.credentials
    )
    print_json(resp)


def target_connection_list(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    if args.limit is not None:
        print_json(api_client.list_target_connections(args.limit))
    else:
        print_json(api_client.list_target_connections())
    return None


def target_connection_delete(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.delete_target_connection(args.name))


def target_connection_get(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.get_target_connection(args.name))


def conversion_create(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.create_conversion(
        args.name, args.source_data, args.source_schema,
        args.target_connection, args.append, args.use_stats,
        args.prefix, args.suffix))


def conversion_execute(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.execute_conversion(
        args.name, args.data_flow, args.source_data,
        args.target_connection, args.append, args.format,
        args.prefix, args.suffix))


def conversion_execute_upload(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    if args.source_data_type.lower() not in ['xml', 'json']:
        raise Exception('--source_data_type is not valid, it can only be XML or JSON')

    # check if dataflow exists, before uploading files
    try:
        api_client.get_dataflow(args.data_flow)
    except Exception:
        print("Dataflow with name {name} does not exists".format(name=args.data_flow))
        return False

    # check if conversion name is available, before uploading files
    try:
        cv = api_client.get_conversion(args.name)
        print("Conversion with name {name} already exists".format(name=cv['name']))
        return False
    except Exception:
        pass

    try:
        data_tmp_name = args.name + str(int(time.time() * 1000))
        source_data = api_client.create_file_data_source(data_tmp_name, args.source_data_type, args.source_data)
        args.source_data = source_data['name']

        print_json(api_client.execute_conversion(
            args.name, args.data_flow, args.source_data,
            args.target_connection, args.append, args.format,
            args.prefix, args.suffix))
    except Exception:
        pass
    finally:
        if hasattr(args, 'source_data') and args.source_data is not None:
            api_client.delete_data_source(args.source_data)
    return True


def conversion_list(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.list_conversions(args))
    return None


def conversion_delete(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.delete_conversion(args.name))


def conversion_get(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.get_conversion(args.name))


def webhook_create(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.create_webhook(args.name, args.url))


def webhook_list(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    if args.limit is not None:
        print_json(api_client.list_webhooks(args.limit))
    else:
        print_json(api_client.list_webhooks())
    return None


def webhook_delete(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.delete_webhook(args.name))


def webhook_get(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.get_webhook(args.name))
    return True


def dataflow_create(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    # check if --optimize flag presents
    if hasattr(args, 'optimize') and args.optimize is not None:
        if hasattr(args, 'source_schema'
                   ) or hasattr(args, 'schema'):
            # args.optimize = args.optimize.lower()
            setattr(api_client, 'optimize', args.optimize)
        else:
            raise Exception('--optimize option for now can '
                            'only be used together with --source_schema '
                            '(--schema)!')
    print_json(api_client.create_dataflow(args.name, args.source_data, args.source_schema, args.optimize))
    return True


def dataflow_create_upload(args, api_client: FaasAPIClient):
    upload_data = False
    upload_schema = False
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False

    if hasattr(args, 'source_data') and args.source_data is not None:
        # check if input xml or json
        if hasattr(args, 'source_data_type'):
            # requires right type
            if args.source_data_type is None or args.source_data_type.lower() not in ['xml', 'json']:
                raise Exception('--source_data_type is not valid, it can only be XML or JSON')
            if args.source_data_type.lower() == 'json':
                # ignore optimize and source_schema
                args.optimize = None
                args.source_schema = None
                upload_schema = False
            upload_data = True

    if hasattr(args, 'source_schema') and args.source_schema is not None:
        upload_schema = True

    # check if --optimize flag presents
    if hasattr(args, 'optimize') and args.optimize is not None:
        if hasattr(args, 'source_schema') or hasattr(args, 'schema'):
            setattr(api_client, 'optimize', args.optimize)
        else:
            raise Exception('--optimize option for now can '
                            'only be used together with --source_schema '
                            '(--schema)!')

    try:
        # check if dataflow name is available, before uploading files
        try:
            df = api_client.get_dataflow(args.name)
            print("Dataflow with name {name} already exists".format(name=df['name']))
            return False
        except Exception:
            pass

        if upload_schema:
            schema_tmp_name = args.name + str(int(time.time() * 1000))
            source_schema = api_client.create_file_schema_source(schema_tmp_name, args.source_schema)
            args.source_schema = source_schema['name']

        if upload_data:
            data_tmp_name = args.name + str(int(time.time() * 1000))
            source_data = api_client.create_file_data_source(data_tmp_name, args.source_data_type, args.source_data)
            args.source_data = source_data['name']

        print_json(api_client.create_dataflow(args.name, args.source_data, args.source_schema, args.optimize))
    except Exception as ex:
        print(ex)
    finally:
        if hasattr(args, "source_schema") and args.source_schema is not None:
            api_client.delete_schema_source(args.source_schema)

        if hasattr(args, "source_data") and args.source_data is not None:
            api_client.delete_data_source(args.source_data)

    return True


def dataflow_list(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    if args.limit is not None:
        print_json(api_client.list_dataflows(args.limit))
    else:
        print_json(api_client.list_dataflows())
    return None


def dataflow_delete(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.delete_dataflow(args.name))


def dataflow_get(args, api_client: FaasAPIClient):
    # check wether --endpoint presents
    if hasattr(args, 'endpoint') and args.endpoint is not None:
        setattr(api_client, 'endpoint', args.endpoint)
    if not check_access(args, api_client):
        return False
    print_json(api_client.get_dataflow(args.name))


# ---
def dataflow_trigger(args, api_client: FaasAPIClient):
    if not check_access(args, api_client):
        return False
    print_json(api_client.trigger_dataflow(
        args))

    return None


def print_json(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


# noinspection PyUnusedLocal
def process_current_command(args, api_client: FaasAPIClient):
    print_context_help(args)
    sys.exit(2)


def change_endpoint(args, api_client: FaasAPIClient):
    if not check_access(args, api_client):
        return False
    _conf = Configuration()
    setattr(_conf, 'config', _conf.load_config())
    _conf.config.update({'endpoint': args.url})
    _conf.save_config()
    return None


# -------> Override help and error handler functions
class ArgParseCustomHelp(argparse.ArgumentParser):

    def print_usage(self, file=None):
        if file is None:
            file = sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None, *args, **kwargs):
        #
        _args = self.prog.split(' ')
        args = argparse.Namespace()
        if len(_args) > 1:
            setattr(args, 'command', _args[1])
        if len(_args) > 2:
            setattr(args, 'subcommand', _args[2])
        if len(_args) > 3:
            setattr(args, 'subcommand2', _args[3])
        print_context_help(args)
        return None

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = sys.stderr
            file.write(message)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        sys.exit(status)

    def error(self, message):
        print(f'\033[31mError: {message} \033[0m')
        ArgParseCustomHelp.print_help(self)
        sys.exit(2)


# -------> FaasCli global parser
# noinspection SpellCheckingInspection,SpellCheckingInspection
class ArgumentParser:
    def __init__(self):
        # super().__init__()
        self.parser = self.init_parser(self)

    @staticmethod
    def init_parser(self):
        # -------> create the top-level parser
        parser = ArgParseCustomHelp()
        parser.set_defaults(func=parser.print_help)
        subparsers = parser.add_subparsers(dest="command")
        # create a parser for yhe "endpoint" command to change API builtin url
        parser_endpoint = subparsers.add_parser('endpoint')
        parser_endpoint.add_argument('--url')
        parser_endpoint.set_defaults(func=change_endpoint)
        # ---------------------------------------------------
        # create the parser for the "login" command
        parser_login = subparsers.add_parser('login')
        parser_login.add_argument('--username')
        parser_login.add_argument('--password')
        parser_login.add_argument('--endpoint')
        parser_login.set_defaults(func=login)
        # ---------------------------------------------------
        # create the parser for the "version" command
        parser_version = subparsers.add_parser('version')
        parser_version.set_defaults(func=print_version)

        # ---------------------------------------------------
        # create the parser for the "source_data" command
        parser_sc = subparsers.add_parser('source_connection', aliases=['source'])
        parser_sc.add_argument('--endpoint')
        parser_sc.set_defaults(func=process_current_command)
        parser_sc_subparsers = parser_sc.add_subparsers(dest='subcommand')

        parser_sc_create = parser_sc_subparsers.add_parser('create')
        create_sc_type = parser_sc_create.add_subparsers(dest="type")

        # -------> S3 as data source
        create_sc_s3 = create_sc_type.add_parser('s3')
        create_sc_s3.add_argument("--name", required=True)
        create_sc_s3.add_argument("--type", required=True)
        create_sc_s3.add_argument("--path", required=True)
        create_sc_s3.add_argument("--role_arn", required=True)
        create_sc_s3.set_defaults(func=source_connection_create_s3)

        # -------> HTTP as source_data
        create_sc_http = create_sc_type.add_parser('http')
        create_sc_http.add_argument("--name", required=True)
        create_sc_http.add_argument("--type", required=True)
        create_sc_http.add_argument("--url", required=True)
        create_sc_http.set_defaults(func=source_connection_create_http)

        # -------> list of existing source_datas in FaaS
        parser_sc_list = parser_sc_subparsers.add_parser('list')
        parser_sc_list.add_argument(('--limit'))
        parser_sc_list.set_defaults(func=source_data_list)
        # -------> delete
        parser_sc_delete = parser_sc_subparsers.add_parser(
            'delete')
        parser_sc_delete.set_defaults(func=source_data_delete)
        parser_sc_delete.add_argument('--name', required=True)
        # -------> get
        parser_sc_get = parser_sc_subparsers.add_parser('get')
        parser_ds_get_group = parser_sc_get.add_mutually_exclusive_group(required=True)
        parser_ds_get_group.add_argument('--name', dest="name", required=False, action=NameAction)
        parser_ds_get_group.add_argument('name', nargs=argparse.OPTIONAL, default=None, action=NameAction)
        parser_sc_get.set_defaults(func=source_data_get)
        #
        # # ---------------------------------------------------
        # # create the parser for the "source_schema" command
        # parser_ss = subparsers.add_parser('source_schema', aliases=['source_schema'])
        # parser_ss.add_argument('--endpoint')
        # parser_ss.set_defaults(func=process_current_command)
        # parser_ss_subparsers = parser_ss.add_subparsers(
        #     dest='subcommand')
        # # -------> Create source_schema
        # parser_ss_create = parser_ss_subparsers.add_parser(
        #     'create')
        # parser_ss_create.set_defaults(func=process_current_command)
        # schema = parser_ss_create.add_subparsers(dest="source_type")
        # # file as schema source
        # file_schema = schema.add_parser("fromfile", aliases=['file'])
        # file_schema.add_argument("--name", required=True)
        # file_schema.add_argument("--file", required=True)
        # file_schema.set_defaults(func=source_schema_create_file)
        # # S3 as data source
        # _s3_schema = schema.add_parser('froms3', description=
        # 'Indicate your S3 bucket', aliases=['s3'])
        # _s3_schema.add_argument("--name", required=True)
        # _s3_schema.add_argument("--path", required=True)
        # _s3_schema.add_argument("--role_arn", required=True)
        # _s3_schema.set_defaults(func=source_schema_from_s3)
        # # http as source_schema
        # file_schema = schema.add_parser("http")
        # file_schema.set_defaults(func=source_schema_create_file)
        # file_schema.add_argument("--name", required=True)
        # file_schema.add_argument("--url", required=True)
        # file_schema.set_defaults(func=source_schema_create_http)
        #
        # parser_ss_list = parser_ss_subparsers.add_parser(
        #     'list')
        # parser_ss_list.add_argument(('--limit'))
        # parser_ss_list.set_defaults(func=source_schema_list)
        # parser_ss_delete = parser_ss_subparsers.add_parser(
        #     'delete')
        # parser_ss_delete.add_argument('--name', required=True)
        # parser_ss_delete.set_defaults(func=source_schema_delete)
        # parser_ss_get = parser_ss_subparsers.add_parser('get')
        # parser_ss_get_group = parser_ss_get.add_mutually_exclusive_group(required=True)
        # parser_ss_get_group.add_argument('--name', dest="name", required=False, action=NameAction)
        # parser_ss_get_group.add_argument('name', nargs=argparse.OPTIONAL, default=None, action=NameAction)
        # parser_ss_get.set_defaults(func=source_schema_get)

        # ---------------------------------------------------
        # create the parser for the "target_connection" command
        parser_tc = subparsers.add_parser('target_connection', aliases=['target'])
        parser_tc.add_argument('--endpoint')
        parser_tc.set_defaults(func=process_current_command)
        parser_tc_subparsers = parser_tc.add_subparsers(
            dest='subcommand')

        parser_tc_create = parser_tc_subparsers.add_parser(
            'create')
        parser_tc_create.set_defaults(func=process_current_command)
        target_type = parser_tc_create.add_subparsers(
            dest="target_type")

        # ------- Snowflake target_connection ----------------------------------
        target_type_sf = target_type.add_parser("snowflake")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--host", required=True)
        target_type_sf.add_argument("--username", required=True)
        target_type_sf.add_argument("--password", required=True)
        target_type_sf.add_argument("--database", required=True)
        target_type_sf.add_argument("--warehouse", required=True)
        target_type_sf.add_argument("--schema", required=True)
        target_type_sf.add_argument("--role")
        target_type_sf.set_defaults(func=target_connection_create_snowflake)
        # ------- MySQL target_connection ----------------------------------
        target_type_sf = target_type.add_parser("mysql")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--host", required=True)
        target_type_sf.add_argument("--username", required=True)
        target_type_sf.add_argument("--password", required=True)
        target_type_sf.add_argument("--database", required=True)
        target_type_sf.set_defaults(func=target_connection_create_mysql)
        # ------- PostGreSQL target_connection ----------------------------------
        target_type_sf = target_type.add_parser("postgresql")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--host", required=True)
        target_type_sf.add_argument("--username", required=True)
        target_type_sf.add_argument("--password", required=True)
        target_type_sf.add_argument("--database", required=True)
        target_type_sf.add_argument("--schema")
        target_type_sf.set_defaults(func=target_connection_create_postgresql)
        # ------- S3 target_connection ----------------------------------
        target_type_sf = target_type.add_parser("s3")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--path", required=True)
        target_type_sf.add_argument("--role_arn", required=True)
        target_type_sf.set_defaults(func=target_connection_create_s3)
        # ------- SQLServer target_connection ----------------------------------
        target_type_sf = target_type.add_parser("sqlserver")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--host", required=True)
        target_type_sf.add_argument("--username", required=True)
        target_type_sf.add_argument("--password", required=True)
        target_type_sf.add_argument("--database", required=True)
        target_type_sf.set_defaults(func=target_connection_create_sqlserver)
        # ------- Oracle target_connection ----------------------------------
        target_type_sf = target_type.add_parser("oracle")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--host", required=True)
        target_type_sf.add_argument("--username", required=True)
        target_type_sf.add_argument("--password", required=True)
        target_type_sf.add_argument("--database", required=True)
        target_type_sf.set_defaults(func=target_connection_create_oracle)
        # ------- Redshift target_connection ----------------------------------
        target_type_sf = target_type.add_parser("redshift")
        target_type_sf.add_argument("--name", required=True)
        target_type_sf.add_argument("--host", required=True)
        target_type_sf.add_argument("--username", required=True)
        target_type_sf.add_argument("--password", required=True)
        target_type_sf.add_argument("--database", required=True)
        target_type_sf.set_defaults(func=target_connection_create_redshift)
        target_type_bq = target_type.add_parser("bigquery")
        target_type_bq.add_argument("--name", required=True)
        target_type_bq.add_argument("--dataset", required=True)
        target_type_bq.add_argument("--storage", required=True)
        target_type_bq.add_argument("--credentials", required=True)
        target_type_bq.set_defaults(func=target_connection_create_bigquery)

        parser_tc_list = parser_tc_subparsers.add_parser('list')
        parser_tc_list.add_argument(('--limit'))
        parser_tc_list.set_defaults(func=target_connection_list)
        parser_tc_delete = parser_tc_subparsers.add_parser('delete')
        parser_tc_delete.add_argument('--name', required=True)
        parser_tc_delete.set_defaults(
            func=target_connection_delete)
        parser_tc_get = parser_tc_subparsers.add_parser('get')
        parser_tc_get_group = parser_tc_get.add_mutually_exclusive_group(required=True)
        parser_tc_get_group.add_argument('--name', dest="name", required=False, action=NameAction)
        parser_tc_get_group.add_argument('name', nargs=argparse.OPTIONAL, default=None, action=NameAction)
        parser_tc_get.set_defaults(func=target_connection_get)

        # ---------------------------------------------------
        # create the parser for the "conversion" command
        parser_conversion = subparsers.add_parser('conversion')
        parser_conversion.add_argument('--endpoint')
        parser_conversion.set_defaults(func=process_current_command)
        parser_conversion_subparsers = parser_conversion.add_subparsers(
            dest='subcommand')
        # create subcommand
        parser_conversion_create = parser_conversion_subparsers.add_parser(
            'create')
        parser_conversion_create.set_defaults(func=process_current_command)
        parser_conversion_create.add_argument('--name', required=True)
        parser_conversion_create.add_argument('--source_data', '--data_source', '--data',
                                              required=True)
        parser_conversion_create.add_argument('--source_schema', '--schema_source', '--schema',
                                              required=False,
                                              default=None)
        parser_conversion_create.add_argument('--target_connection', '--target', required=False,
                                              default=None)
        parser_conversion_create.add_argument('--append', required=False,
                                              default=None)
        parser_conversion_create.add_argument('--use_stats',
                                              required=False, default='true')
        parser_conversion_create.add_argument('--prefix',
                                              required=False, default='true')
        parser_conversion_create.add_argument('--suffix',
                                              required=False, default='true')
        parser_conversion_create.set_defaults(func=conversion_create)

        parser_conversion_execute = parser_conversion_subparsers.add_parser('execute')
        parser_conversion_execute.set_defaults(func=process_current_command)
        parser_conversion_execute.add_argument('--name', required=True)
        parser_conversion_execute.add_argument('--data_flow', required=True)
        parser_conversion_execute.add_argument('--source_data', required=False)
        parser_conversion_execute.add_argument('--target_connection', '--target', required=False, default=None)
        parser_conversion_execute.add_argument('--append', required=False, default=None)
        parser_conversion_execute.add_argument('--format', required=False, default=None)
        parser_conversion_execute.add_argument('--prefix', required=False, default=None)
        parser_conversion_execute.add_argument('--suffix', required=False, default=None)
        parser_conversion_execute.set_defaults(func=conversion_execute)

        parser_conversion_execute_upload = parser_conversion_subparsers.add_parser('execute_upload')
        parser_conversion_execute_upload.set_defaults(func=process_current_command)
        parser_conversion_execute_upload.add_argument('--name', required=True)
        parser_conversion_execute_upload.add_argument('--data_flow', required=True)
        parser_conversion_execute_upload.add_argument('--source_data', '--data_source', '--data', required=True)
        parser_conversion_execute_upload.add_argument('--source_data_type', '--data_source_type', '--data_type',
                                                      required=True)
        parser_conversion_execute_upload.add_argument('--target_connection', '--target', required=False,
                                                      default=None)
        parser_conversion_execute_upload.add_argument('--append', required=False, default=None)
        parser_conversion_execute_upload.add_argument('--format', required=False, default=None)
        parser_conversion_execute_upload.add_argument('--prefix', required=False, default=None)
        parser_conversion_execute_upload.add_argument('--suffix', required=False, default=None)
        parser_conversion_execute_upload.set_defaults(func=conversion_execute_upload)

        parser_conversion_list = parser_conversion_subparsers.add_parser('list')
        parser_conversion_list.add_argument('--limit')
        parser_conversion_list.add_argument('--filter_df')
        parser_conversion_list.set_defaults(func=conversion_list)
        parser_conversion_delete = parser_conversion_subparsers.add_parser('delete')
        parser_conversion_delete.add_argument('--name', required=True)
        parser_conversion_delete.set_defaults(func=conversion_delete)
        parser_conversion_get = parser_conversion_subparsers.add_parser('get')
        parser_conversion_get_group = parser_conversion_get.add_mutually_exclusive_group(required=True)
        parser_conversion_get_group.add_argument('--name', dest="name", required=False, action=NameAction)
        parser_conversion_get_group.add_argument('name', nargs=argparse.OPTIONAL, default=None, action=NameAction)
        parser_conversion_get.set_defaults(func=conversion_get)

        # ---------------------------------------------------
        # create the parser for the "data_flow" command
        parser_flow = subparsers.add_parser('data_flow')
        parser_flow.add_argument('--endpoint')
        parser_flow.set_defaults(func=process_current_command)
        parser_flow_subparsers = parser_flow.add_subparsers(
            dest='subcommand')
        # -------
        parser_flow_create = parser_flow_subparsers.add_parser('create')
        parser_flow_create.set_defaults(func=process_current_command)
        parser_flow_create.add_argument('--name', required=True)
        parser_flow_create.add_argument('--source_data', '--data_source', '--data', required=False)
        parser_flow_create.add_argument('--source_schema', '--schema_source', '--schema', required=False, default=None)
        parser_flow_create.add_argument('--optimize', required=False)
        parser_flow_create.set_defaults(func=dataflow_create)

        parser_flow_create_upload = parser_flow_subparsers.add_parser('create_upload')
        parser_flow_create_upload.set_defaults(func=process_current_command)
        parser_flow_create_upload.add_argument('--name', required=True)
        parser_flow_create_upload.add_argument('--source_data', '--data_source', '--data', required=False)
        parser_flow_create_upload.add_argument('--source_data_type', '--data_source_type', '--data_type',
                                               required=False)
        parser_flow_create_upload.add_argument('--source_schema', '--schema_source', '--schema', required=False,
                                               default=None)
        parser_flow_create_upload.add_argument('--optimize', required=False)
        parser_flow_create_upload.set_defaults(func=dataflow_create_upload)
        # ---------------------------------
        parser_flow_list = parser_flow_subparsers.add_parser(
            'list')
        parser_flow_list.add_argument(('--limit'))
        parser_flow_list.set_defaults(func=dataflow_list)
        parser_flow_delete = parser_flow_subparsers.add_parser(
            'delete')
        parser_flow_delete.add_argument('--name',
                                        required=True)
        parser_flow_delete.set_defaults(func=dataflow_delete)
        # parser_flow_trigger = parser_flow_subparsers.add_parser(
        #     'trigger')
        # parser_flow_trigger.add_argument('--name',
        #                                  required=True)
        # parser_flow_trigger.add_argument('--append',
        #                                  required=False)
        # parser_flow_trigger.add_argument('--format',
        #                                  required=False)
        # parser_flow_trigger.add_argument('--target',
        #                                  required=False)
        # parser_flow_trigger.set_defaults(func=dataflow_trigger)
        parser_flow_get = parser_flow_subparsers.add_parser('get')
        parser_flow_get_group = parser_flow_get.add_mutually_exclusive_group(required=True)
        parser_flow_get_group.add_argument('--name', dest="name", required=False, action=NameAction)
        parser_flow_get_group.add_argument('name', nargs=argparse.OPTIONAL, default=None, action=NameAction)
        parser_flow_get.set_defaults(func=dataflow_get)

        # ---------------------------------------------------
        # create the parser for the "webhook" command
        parser_webhook = subparsers.add_parser('webhook')
        parser_webhook.add_argument('--endpoint')
        parser_webhook.set_defaults(func=process_current_command)
        parser_webhook_subparsers = parser_webhook.add_subparsers(
            dest='subcommand')
        parser_webhook_create = parser_webhook_subparsers.add_parser(
            'create')
        parser_webhook_create.set_defaults(func=process_current_command)
        parser_webhook_create.add_argument('--name', required=True)
        parser_webhook_create.add_argument('--url', required=True)
        parser_webhook_create.set_defaults(func=webhook_create)
        parser_webhook_list = parser_webhook_subparsers.add_parser('list')
        parser_webhook_list.add_argument(('--limit'))
        parser_webhook_list.set_defaults(func=webhook_list)
        parser_webhook_delete = parser_webhook_subparsers.add_parser('delete')
        parser_webhook_delete.add_argument('--name', required=True)
        parser_webhook_delete.set_defaults(func=webhook_delete)
        parser_webhook_get = parser_webhook_subparsers.add_parser('get')
        parser_webhook_get_group = parser_webhook_get.add_mutually_exclusive_group(required=True)
        parser_webhook_get_group.add_argument('--name', dest="name", required=False, action=NameAction)
        parser_webhook_get_group.add_argument('name', nargs=argparse.OPTIONAL, default=None, action=NameAction)
        parser_webhook_get.set_defaults(func=webhook_get)

        return parser

    # TODO add aliases to all commands like data_source, source_schema
    # TODO  and target_connection

    def parse_args(self, args=None):
        if args:
            return self.parser.parse_args(args)
        else:
            return self.parser.parse_args()


class NameAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(NameAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if hasattr(namespace, self.dest) and values is None:
            return
        setattr(namespace, self.dest, values)


def main():
    api_client = FaasAPIClient()
    api_client.user_agent = f'FaaS CLI v{version}'
    # api_client.endpoint = 'https://faasdev.sonra.io'
    parser = ArgumentParser()
    args = parser.parse_args()
    try:
        args.func(args, api_client)
    except Exception as _err:  # AttributeError:
        parser.parser.error(str(_err))
        ArgParseCustomHelp.print_help(parser.parser)


if __name__ == "__main__":
    main()
