import click


def register(app):
    @app.cli.group()
    def user():
        """Handle users."""
        pass

    @user.command()
    @click.argument("username")
    @click.argument("password")
    def add(username, password):
        """Add an user."""
        from bytardag.models import User
        from bytardag import db

        user = User(username=username)
        user.password = password
        db.session.add(user)
        db.session.commit()
        click.echo("Created user {}".format(username))

    @app.cli.group()
    def sid():
        """Handle seller-IDs."""
        pass

    @sid.command()
    @click.argument("file", type=click.File("r"))
    def init(file):
        """Import seller IDs from file."""
        from bytardag.models import Seller
        from bytardag import db

        count = 0
        for line in file:
            sid = line.strip()
            if sid:
                s = Seller(seller_id=sid)
                count += 1
                db.session.add(s)
        db.session.commit()
        click.echo(f"Added {count} seller IDs to database.")

    @sid.command()
    @click.argument("file", type=click.File("w"))
    def refresh(file):
        """Refresh JS cache for auto-complete."""
        import os
        import json
        from bytardag.models import Seller
        from bytardag import db

        sellers = db.session.query(Seller).all()
        data = json.dumps([s.seller_id for s in sellers])

        file.write(
                f"/* Auto-complete data, do not edit! */\nexport const sellers = {data};"
            )
