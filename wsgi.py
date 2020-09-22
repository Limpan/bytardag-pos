from bytardag import cli, create_app

app = create_app()
cli.register(app)
