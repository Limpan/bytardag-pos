import click


def register(app):
    @app.cli.group()
    def user():
        """Handle users."""
        pass

    @user.command()
    def add():
        """Add an user."""
        from app.models import User
        from app import db

        user = User(username="test1")
        user.set_password("qwerty")
        db.session.add(user)
        db.session.commit()
        click.echo("Created user")

    @app.cli.group()
    def sid():
        """Handle seller-IDs."""
        pass

    @sid.command()
    @click.argument("file", type=click.File("r"))
    def init(file):
        """Import seller IDs from file."""
        from app.models import Seller
        from app import db

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
    def refresh():
        """Refresh JS cache for auto-complete."""
        import os
        import json
        from app.models import Seller
        from app import db

        base_dir = os.path.dirname(__file__)
        file_loc = os.path.join(base_dir, "static/js/autocomplete.js")

        sellers = db.session.query(Seller).all()
        data = json.dumps([s.seller_id for s in sellers])

        with open(file_loc, mode="w") as fp:
            fp.write(
                f"/* Auto-complete data, do not edit! */\nexport const sellers = {data};"
            )
        click.echo("Successfully updated auto-complete data.")
