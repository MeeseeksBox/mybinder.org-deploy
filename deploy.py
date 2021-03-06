#!/usr/bin/env python3
import argparse
import subprocess
import yaml
import os


def deploy(release):
    # Set up helm!
    subprocess.check_call(['helm', 'repo', 'update'])

    with open('config/common.yaml') as f:
        config = yaml.safe_load(f)

    helm = [
        'helm', 'upgrade', '--install',
        '--namespace', release,
        release,
        'jupyterhub/binderhub',
        '--version', config['version'],
        '--wait',
        '-f', 'config/common.yaml',
        '-f', 'config/secret/common.yaml',
        '-f', os.path.join('config', release + '.yaml'),
        '-f', os.path.join('config', 'secret', release + '.yaml')
    ]

    subprocess.check_call(helm)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--user-image-spec',
        default='berkeleydsep/datahub-user'
    )
    subparsers = argparser.add_subparsers(dest='action')

    deploy_parser = subparsers.add_parser('deploy', description='Deploy with helm')
    deploy_parser.add_argument('release', default='staging')


    args = argparser.parse_args()

    deploy(args.release)

main()
