from datetime import datetime

from pydantic import BaseModel
from starlette.responses import JSONResponse

from configs.mysql_config import My_Connection


class Message(BaseModel):
    receiver_id: int
    sender_id: int
    content: str
    timestamp: datetime
    contact_id: int


class MessageModel:
    def get_messages_by_contact_id(self, contact_id: int):
        conditions = []
        params = {}
        if contact_id:
            conditions.append("contact_id = %(id_user)s")
            params['id_user'] = f"{contact_id}"

        sql = "SELECT * FROM messages"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, params)
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}

    def get_user_contact_history(self, uid: int):
        with My_Connection() as db_connection:
            db_connection.cur.execute(
                """
                SELECT chv.contact_id, chv.link_avatar, chv.user_name, chv.timestamp AS last_message_time, chv.message
                FROM contact_history_view chv
                JOIN (
                    SELECT contact_id, MAX(timestamp) AS max_timestamp
                    FROM contact_history_view
                    WHERE receiver_id = %(uid)s
                    GROUP BY contact_id
                ) max_messages
                ON chv.contact_id = max_messages.contact_id AND chv.timestamp = max_messages.max_timestamp
                WHERE chv.receiver_id = %(uid)s
                """,
                {"uid": uid}
            )
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}

    def send_message(self, data: str):
        message = Message.parse_raw(data)
        sql = "INSERT INTO messages (receiver_id, sender_id, content, timestamp, contact_id) " \
              "VALUES (%(receiver_id)s, %(sender_id)s, %(content)s, %(timestamp)s, %(contact_id)s)"

        with My_Connection() as db_connection:
            try:
                db_connection.cur.execute(sql, message.dict())
                if db_connection.cur.rowcount > 0:
                    # Nếu thêm tin nhắn thành công, trả về response 201 và đối tượng message
                    return JSONResponse(content={"message": "CREATED_SUCCESSFULLY", "message_data": message.dict()},
                                        status_code=201)
                else:
                    return JSONResponse(content={"message": "Failed to send message"}, status_code=500)
            except Exception as e:
                # Handle database errors and return an appropriate response
                return JSONResponse(content={"message": "Database error"}, status_code=500)
