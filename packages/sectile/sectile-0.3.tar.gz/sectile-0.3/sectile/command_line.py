import argparse



def main():
    parser = argparse.ArgumentParser(
        description='Sectile generates files from fragments.'
    )

    subparsers = parser.add_subparsers(
        title='Actions',
        description=(
            'To get more information, run "sectile [command] --help".'
        ),
        dest='action',
    )

    parser_dimension = subparsers.add_parser(
        'dimension',
        help='modify sectile dimensions',
    )



