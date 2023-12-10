from datetime import datetime

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from controller import user_controller, checking_img_controller, auth_controller, report_comment_controller, \
    comment_controller, saved_sukien_controller, message_controller, add_sukien_controller, websocket_controller
from model.message_model import MessageModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    allow_credentials=False,  # Disable credentials (cookies, jwt_auth)
    expose_headers=["*"],  # Expose all headers
)


# @app.websocket("/ws/{uid}")
# async def websocket_endpoint(websocket: WebSocket):
#     print('Accepting client connection...')
#     await websocket.accept()
#     while True:
#         try:
#             # Wait for any message from the client
#             data = await websocket.receive_text()
#             time_stamp = datetime.now()
#             print(time_stamp)
#             print(data)
#             # Send message to the client
#             await websocket.send_text(data)
#             messageModel = MessageModel()
#             return messageModel.send_message(data)
#         except Exception as e:
#             print('error:', e)
#             break
#     print('Bye..')


app.include_router(user_controller.router)
app.include_router(checking_img_controller.router)
app.include_router(auth_controller.router)
app.include_router(report_comment_controller.router)
app.include_router(comment_controller.router)
app.include_router(saved_sukien_controller.router)
app.include_router(message_controller.router)
app.include_router(add_sukien_controller.router)
app.include_router(websocket_controller.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9000)
