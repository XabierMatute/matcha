from your_database import db
from datetime import datetime

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False, index=True)
    receiver_id = db.Column(db.Integer, nullable=False, index=True)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_sender_receiver', 'sender_id', 'receiver_id'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }

def save_message(sender_id, receiver_id, message):
    """
    Guarda un mensaje en la base de datos.
    """
    if not sender_id or not receiver_id or not message:
        raise ValueError("Sender ID, Receiver ID, and Message are required.")
    
    new_message = ChatMessage(sender_id=sender_id, receiver_id=receiver_id, message=message)
    db.session.add(new_message)
    db.session.commit()
    return new_message.serialize()

def get_messages_between(user1_id, user2_id):
    """
    Obtiene todos los mensajes intercambiados entre dos usuarios.
    """
    if not user1_id or not user2_id:
        raise ValueError("Both user IDs are required.")
    
    messages = (
        ChatMessage.query.filter(
            ((ChatMessage.sender_id == user1_id) & (ChatMessage.receiver_id == user2_id)) |
            ((ChatMessage.sender_id == user2_id) & (ChatMessage.receiver_id == user1_id))
        )
        .order_by(ChatMessage.timestamp.asc())
        .all()
    )
    return [message.serialize() for message in messages]

