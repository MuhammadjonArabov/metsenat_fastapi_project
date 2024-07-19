from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin.admin import setup_admin
from app.api import __routes__


async def on_startup() -> None:
    print('The app is working 🎊🎉🎛')


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)
        self.__register_events(app)
        self.__register_middlewares(app)
        self.__register_websocket(app)
        self.__register_admin(app)

    def get_app(self):
        return self.__app

    @staticmethod
    def __register_routes(app):
        __routes__.register_routes(app)

    @staticmethod
    def __register_websocket(app):
        pass

    @staticmethod
    def __register_admin(app):
        setup_admin(app)
        return app

    @staticmethod
    def __register_events(app: FastAPI):
        app.on_event('startup')(on_startup)

    @staticmethod
    def __register_middlewares(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # yoki kerakli manbalarni kiriting
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
