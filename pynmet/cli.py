import click
from pynmet import inmet


@click.group()
def cli():
    pass


@cli.command()
@click.argument('output', default='./')
@click.option('--local', default=False)
@click.argument('code')
def download(code, local, output):
    if output[-1] is '/':
        out = output + code + '.csv'
    elif output[-4:] is not '.csv':
        out = output + '.csv'
    else:
        out = output
    if '/' not in out[:2]:
        out = './' + out
    est = inmet(code, local=local)
    est.dados.to_csv(out)


def update():
    pass
