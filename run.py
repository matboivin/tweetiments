from app import app

if __name__ == '__main__':
    app.run_server(
        port=8000,
        host='127.0.0.1',
        debug=True
    )