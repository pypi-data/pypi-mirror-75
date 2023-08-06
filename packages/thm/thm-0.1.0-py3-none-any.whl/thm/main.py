import click


@click.command()
@click.option(
    "-u", "--upload", help="Upload your notes & script additions to GitHub", is_flag=True
)
@click.option(
        "-a", "--add", type=str, help="Add a new libary to the scripts. Will automatically sudo-apt install install it.", default=None
        )
@click.option("-d", "--download", help="Download your config repo", type=str, default=None)
def main(**kwargs):
    if kwargs["upload"]:
        upload()
    elif kwargs["-a"] not None:
        add()
    elif kwargs["-d"] not None:
        download()
    print(kwargs)

def upload():
    yes

def add():
    None

def download():
    None


if __name__ == "__main__":
    main()
