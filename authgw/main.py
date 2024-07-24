import dotenv
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from authgw.router import routes


dotenv.load_dotenv()

class APIServer:

    app = None

    def __init__(self):
        pass

    @staticmethod
    def _get_app():
        if not APIServer.app:
            APIServer.app = FastAPI(debug=True)
            origins = ["*"]
            APIServer.app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        return APIServer.app
    
    def create_app(self):
        app = self._get_app()
        routes.generate_routes(app)
        return app


def run():
    app = APIServer().create_app()
    uvicorn.run(app, host=str(os.environ.get("HOST")), port=int(os.environ.get("PORT")))
