# Copyright 2020 Ben Kehoe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import subprocess
import sys

__version__ = '0.3.1'

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--profile', required=True, help='The AWS profile to configure')

    parser.add_argument('--sso-start-url')
    parser.add_argument('--sso-region')

    interactive_group = parser.add_mutually_exclusive_group()
    interactive_group.add_argument('--set-auth-interactive', '-i', action='store_const', const=True, dest='interactive', help='Enable interactive auth')
    interactive_group.add_argument('--set-auth-noninteractive', '-n', action='store_const', const=False, dest='interactive', help='Disable interactive auth')

    parser.add_argument('--version', action='store_true')

    args = parser.parse_args()

    if args.version:
        print(__version__)
        parser.exit()

    def get(name):
        return subprocess.run(['aws', 'configure', 'get', 'profile.{}.{}'.format(args.profile, name)], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def set(name, value):
        subprocess.run(['aws', 'configure', 'set', 'profile.{}.{}'.format(args.profile, name), value or ''], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    default_sso_start_url =  os.environ.get('AWS_CONFIGURE_SSO_DEFAULT_SSO_START_URL',  os.environ.get('AWS_CONFIGURE_DEFAULT_SSO_START_URL'))
    default_sso_region    =  os.environ.get('AWS_CONFIGURE_SSO_DEFAULT_SSO_REGION',     os.environ.get('AWS_CONFIGURE_DEFAULT_SSO_REGION'))

    if args.sso_start_url:
        set('sso_start_url', args.sso_start_url)
    elif not get('sso_start_url') and default_sso_start_url:
        set('sso_start_url', default_sso_start_url)

    if args.sso_region:
        set('sso_region', args.sso_region)
    elif not get('sso_region') and default_sso_region:
        set('sso_region', default_sso_region)

    result = subprocess.run('aws configure sso --profile {}'.format(args.profile), shell=True).returncode

    if result:
        sys.exit(result)

    if os.environ.get('AWS_CONFIGURE_SSO_DISABLE_CREDENTIAL_PROCESS', '').lower() not in ['1', 'true']:
        credential_process_opts = ''
        if args.interactive is True:
            credential_process_opts += ' --interactive'
        elif args.interactive is False:
            credential_process_opts += ' --noninteractive'
        set('credential_process', 'aws-sso-credential-process --profile {profile}{opts}'.format(profile=args.profile, opts=credential_process_opts))

if __name__ == '__main__':
    main()

