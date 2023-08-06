import click
import json
from ssm.aws import ssm_client
from ssm.color import color


@click.group()
def cli():
    """A CLI wrapper for the SSM."""
    pass


@cli.command()
@click.argument('path')
@click.option('-o', '--output', default='.env.ssm.json', help='Name to the output JSON file.')
def dump(path: str, output: str):
    """Get all cataloged credentials and save it on a file."""
    parameters = []
    extra_args = {
        'Path': path,
        'Recursive': False,
        'WithDecryption': True,
        'MaxResults': 2
    }
    data = {}

    if not output.endswith('.json'):
        click.echo('Output file must ends with .json', err=True)
        exit(1)

    while True:
        response = ssm_client.get_parameters_by_path(**extra_args)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code != 200:
            click.echo('Could not fetch parameters, HTTPStatusCode: ' + status_code, err=True)

        parameters = parameters + response['Parameters']

        if 'NextToken' not in response:
            break

        extra_args['NextToken'] = response['NextToken']

    data['parameters'] = parameters

    click.echo(json.dumps(data, indent=4, sort_keys=True, default=str))

    with open(output, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True, default=str)


@cli.command()
@click.option('-f', '--file', default='.env.ssm.json', help='Name to the JSON file.')
def load(file: str):
    """Load all cataloged credentials from a file and update the SSM client."""
    if not file.endswith('.json'):
        click.echo('Output file must ends with .json', err=True)
        exit(1)
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            for param in data['parameters']:
                args = {
                    'Name': param['Name'],
                    'Value': param['Value'],
                    'Overwrite': True,
                    'Type': param['Type'],
                    'Tier': "Intelligent-Tiering"
                }
                response = ssm_client.put_parameter(**args)
                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    click.echo(param['Name'] + color.FAIL + ' FAIL' + color.ENDC, err=True)
                    exit(1)
                else:
                    click.echo(param['Name'] + color.OK + ' OK' + color.ENDC)
    except BaseException:
        click.echo('No such file named ' + file + ' in directory.', err=True)
        exit(1)


if __name__ == "__main__":
    cli()
