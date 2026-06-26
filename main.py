"""Entrypoint uvicorn — puerto 8097."""

import uvicorn

from uipath_copilot.settings import UIPATH_COPILOT_HOST, UIPATH_COPILOT_PORT

if __name__ == "__main__":
    uvicorn.run(
        "uipath_copilot.app:app",
        host=UIPATH_COPILOT_HOST,
        port=UIPATH_COPILOT_PORT,
        reload=False,
    )
