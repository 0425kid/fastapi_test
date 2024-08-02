from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from models import Message
from schemas import MessageCreate

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/",
    summary="모든 메시지 불러오기",
    description="모든 메시지 목록을 가져옴",
    response_description="메시지 배열"
)
def get_all_message(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages
    #profiles = db.query(Caregiver).all()

# 메시지 전송 API
@router.post("/send-message/", response_model=MessageCreate)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(
        sender_username=message.sender_username,
        receiver_username=message.receiver_username,
        content=message.content
    )
    try:
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"메시지 전송 실패: {str(e)}")
    
    return Response(
        content=f"메시지 생성이 성공적으로 완료되었습니다. 메시지 내용: {db_message.content}",
        status_code=200
    )

@router.get(
    "/get_message_by_sender",
    summary = "전송자 기준으로 메시지 탐색"
)
def get_message_by_sender(username: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.sender_username == username).all()
    return messages

@router.get(
    "/get_message_by_receiver",
    summary = "수신자 기준으로 메시지 탐색"
)
def get_message_by_receiver(username: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.receiver_username == username).all()
    return messages


# 모든 메시지 삭제 및 테이블 초기화
@router.delete(
    "/reset/",
    summary="모든 메시지 삭제 및 테이블 초기화",
    description="caregivers 테이블에 있는 모든 데이터를 삭제하고 테이블 초기화."
)
def delete_all_caregivers(db: Session = Depends(get_db)):
    try:
        # CaregiverProfile과 관련된 레코드를 먼저 삭제합니다
        db.query(Message).delete()
        db.commit()

        # 자동 증가 column 초기화 (text() 함수 사용)
        db.execute(text('TRUNCATE TABLE messages RESTART IDENTITY CASCADE'))
        db.commit()
        
        return {"message": "메시지 테이블 초기화 완료"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"메시지 테이블 초기화 실패: {str(e)}")
