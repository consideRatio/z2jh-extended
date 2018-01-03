#!/usr/bin/env python3
import argparse
import os
import subprocess

from ruamel.yaml import YAML

yaml = YAML(typ='rt')
yaml.indent(mapping=2, offset=2, sequence=4)


def last_modified_commit(*paths, **kwargs):
    return subprocess.check_output([
        'git',
        'log',
        '-n', '1',
        '--pretty=format:%h',
        *paths
    ], **kwargs).decode('utf-8')


def last_modified_date(*paths, **kwargs):
    return subprocess.check_output([
        'git',
        'log',
        '-n', '1',
        '--pretty=format:%cd',
        '--date=iso',
        *paths
    ], **kwargs).decode('utf-8')


def path_touched(*paths, commit_range):
    return subprocess.check_output([
        'git', 'diff', '--name-only', commit_range, *paths
    ]).decode('utf-8').strip() != ''


def render_build_args(options, ns):
    """Get docker build args dict, rendering any templated args."""
    build_args = options.get('buildArgs', {})
    for key, value in build_args.items():
        build_args[key] = value.format(**ns)
    return build_args


def build_image(image_path, image_spec, build_args):
    cmd = ['docker', 'build', '-t', image_spec, image_path]

    for k, v in build_args.items():
        cmd += ['--build-arg', '{}={}'.format(k, v)]
    subprocess.check_call(cmd)


def build_images(prefix, images, tag=None, commit_range=None, push=False):
    value_modifications = {}
    for name, options in images.items():
        image_path = os.path.join('images', name)
        paths = options.get('paths', []) + [image_path]
        last_commit = last_modified_commit(*paths)
        if tag is None:
            tag = last_commit
        image_name = prefix + name
        image_spec = '{}:{}'.format(image_name, tag)
        value_modifications[options['valuesPath']] = {
            'name': image_name,
            'tag': tag
        }

        if commit_range and not path_touched(*paths, commit_range=commit_range):
            print(f"Skipping {name}, not touched in {commit_range}")
            continue

        template_namespace = {
            'LAST_COMMIT': last_commit,
            'TAG': tag,
        }

        build_args = render_build_args(options, template_namespace)
        build_image(image_path, image_spec, build_args)

        if push:
            if prefix.find('gcr.io') >= 0:
                subprocess.check_call([
                    'gcloud', 'docker', '--', 'push', image_spec
                ])
            else:
                subprocess.check_call([
                    'docker', 'push', image_spec
                ])

    return value_modifications


def build_values(name, values_mods):
    """Update name/values.yaml with modifications"""

    values_file = os.path.join(name, 'values.yaml')

    with open(values_file) as f:
        values = yaml.load(f)

    for key, value in values_mods.items():
        parts = key.split('.')
        mod_obj = values
        for p in parts:
            mod_obj = mod_obj[p]
        mod_obj.update(value)

    with open(values_file, 'w') as f:
        yaml.dump(values, f)


def build_chart(name, paths=None, version=None):
    """Update chart with specified version or last-modified commit in path(s)"""
    chart_file = os.path.join(name, 'Chart.yaml')
    with open(chart_file) as f:
        chart = yaml.load(f)

    if version is None:
        if paths is None:
            paths = ['.']
        commit = last_modified_commit(*paths)
        version = chart['version'].split('-')[0] + '-' + commit

    chart['version'] = version

    with open(chart_file, 'w') as f:
        yaml.dump(chart, f)


def deploy(chart, release):
    # Set up helm!
    subprocess.check_call(['helm', 'init', '--client-only'])
    subprocess.check_call(['helm', 'dep', 'update'], cwd='z2jh-extended')

    subprocess.check_call([
        'helm', 'upgrade', release,
        '--install',
        '--namespace', release,
        '--values', 'z2jh-extended/secret-values.yaml',
        'z2jh-extended/'
    ])


def main():
    with open('build-config.yaml') as f:
        config = yaml.load(f)

    argparser = argparse.ArgumentParser()

    argparser.add_argument('--push', action='store_true')
    argparser.add_argument('--deploy', action='store_true')
    argparser.add_argument('--release', default='prod', help='A Helm release name and k8s namespace for a deployment')
    argparser.add_argument('--tag', default=None, help='Use this tag for images & charts')
    argparser.add_argument('--commit-range', help='Range of commits to consider when building images')

    args = argparser.parse_args()

    for chart in config['charts']:
        value_mods = build_images(chart['imagePrefix'], chart['images'], args.tag, args.commit_range, args.push)
        build_values(chart['name'], value_mods)
        chart_paths = ['.'] + chart.get('paths', [])
        build_chart(chart['name'], paths=chart_paths, version=args.tag)
        if args.deploy:
            deploy(chart['name'], args.release)


main()
