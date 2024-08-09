from __init__ import create_app

application = create_app()

"""You can run this file in order to make the server run on the localhost."""
if __name__ == "__main__":
    application.run(host='0.0.0.0')
