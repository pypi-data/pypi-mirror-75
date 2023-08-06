import click


@click.group(context_settings={'help_option_names': ['--help', '-h']})
def mlwcli():
    """Demo WP Control Help"""


@mlwcli.group()
def wp():
    """Commands for WP"""


@wp.command('install')
def wp_install():
    """Install WP instance"""


@click.pass_context
def wp_dup():
    """Duplicate WP instance"""


if __name__ == '__main__':
    mlwcli()
