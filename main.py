# -*- coding: utf-8 -*-
from build_app import app

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host="127.0.0.1", port=8888, reload=False, debug=False)
