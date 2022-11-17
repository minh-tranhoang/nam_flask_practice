from app import create_app

application = create_app('config')

if __name__ == "__main__":
    application.run(port=3000)