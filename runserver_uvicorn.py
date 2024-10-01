from uvicorn import Config, Server

if __name__ == '__main__':
    config = Config('fastapi_app:app', host='0.0.0.0', port=5000, log_level='info', workers=2, reload=True)
    server = Server(config)
    server.run()
