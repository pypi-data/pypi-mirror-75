import os
import re
import shutil
import click
from jinja2 import Environment, FileSystemLoader


__version__ = "0.1.0"


# Compatibility with Python 2.7
try:
    FileExistsError
except NameError:
    FileExistsError = OSError

placeholder_re = re.compile(r'__[^_]\w+?[^_]__')


class SkipFile(Exception):
    pass


class FileCount:
    def __init__(self):
        self.created = 0
        self.overwritten = 0
        self.skipped = 0

    def __str__(self):
        return '{}/{}/{}'.format(self.created, self.overwritten, self.skipped)


def textx_jinja_generator(templates_path, target_path, config, overwrite=False):
    """
    Generates a set of files using Jinja templates.
    """

    """
    Args:
        templates_path (str): A path to templates.
        target_path (str): The path where files should be generated.
        config (dict): A config contains any data necessary
            for rendering files using Jinja engine.
        overwrite (bool): If the target files should be overwritten.
    """
    env = Environment(loader=FileSystemLoader(searchpath=templates_path),
                      trim_blocks=True, lstrip_blocks=True)
    file_count = FileCount()
    config['project_name'] = os.path.basename(os.path.abspath(target_path))

    click.echo("\nStarted generating files in {}".format(target_path))
    for root, dirs, files in os.walk(templates_path):
        for f in files:
            src_file = os.path.join(root, f)
            src_rel_path = os.path.relpath(src_file, templates_path)
            target_file = os.path.join(target_path, src_rel_path)

            # Replace placeholders in the target file name.
            placeholders = placeholder_re.findall(target_file)
            try:
                for placeholder in placeholders:
                    ph_value = config.get(placeholder.strip('_'))
                    if ph_value is False:
                        raise SkipFile
                    elif ph_value is True:
                        target_file = target_file.replace(placeholder, '')
                    elif ph_value is not None:
                        target_file = target_file.replace(placeholder, ph_value)
            except SkipFile:
                continue

            # Strip `jinja` extension from target path.
            if target_file.endswith('.jinja'):
                target_file = '.'.join(target_file.split('.')[:-1])

            # Create necessary folders.
            try:
                os.makedirs(os.path.dirname(target_file))
            except FileExistsError:
                pass

            if overwrite or not os.path.exists(target_file):

                if os.path.exists(target_file):
                    click.echo('Overwriting {}'.format(target_file))
                    file_count.overwritten += 1
                else:
                    click.echo('Creating {}'.format(target_file))
                    file_count.created += 1

                if src_file.endswith('.jinja'):
                    # Render using Jinja template
                    with open(target_file, 'w') as f:
                        f.write(
                            env.get_template(src_rel_path).render(**config))
                else:
                    # Just copy
                    shutil.copy(src_file, target_file)

            else:
                click.echo('Skipping {}'.format(target_file))
                file_count.skipped += 1

    click.echo('Done. Files created/overwritten/skipped = {}'
               .format(file_count))
