from sqlalchemy import Column, String, DateTime, Integer, Text, JSON
from database import Base, async_session
from datetime import datetime
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String, index=True)
    user_id = Column(String, nullable=True, index=True)
    device_id = Column(String, nullable=True)
    ip_address = Column(String)
    user_agent = Column(String, nullable=True)
    resource = Column(String, nullable=True)
    action = Column(String, nullable=True)
    result = Column(String)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class AuditLogger:
    async def log_auth_attempt(self, user_id: Optional[str], ip_address: str, 
                               success: bool, details: Optional[Dict] = None):
        async with async_session() as session:
            log = AuditLog(
                event_type='auth_success' if success else 'auth_failure',
                user_id=user_id,
                ip_address=ip_address,
                result='success' if success else 'failure',
                details=details or {}
            )
            session.add(log)
            await session.commit()
            
            if not success:
                logger.warning(f"Auth failure: user={user_id}, ip={ip_address}")
    
    async def log_api_access(self, endpoint: str, method: str, user_id: Optional[str],
                            device_id: Optional[str], ip_address: str, 
                            status_code: int, details: Optional[Dict] = None):
        async with async_session() as session:
            log = AuditLog(
                event_type='api_access',
                user_id=user_id,
                device_id=device_id,
                ip_address=ip_address,
                resource=endpoint,
                action=method,
                result='success' if status_code < 400 else 'failure',
                details={
                    'status_code': status_code,
                    **(details or {})
                }
            )
            session.add(log)
            await session.commit()
    
    async def log_data_access(self, user_id: str, resource: str, action: str,
                             ip_address: str, success: bool, details: Optional[Dict] = None):
        async with async_session() as session:
            log = AuditLog(
                event_type='data_access',
                user_id=user_id,
                ip_address=ip_address,
                resource=resource,
                action=action,
                result='success' if success else 'failure',
                details=details or {}
            )
            session.add(log)
            await session.commit()
            
            logger.info(f"Data access: user={user_id}, resource={resource}, action={action}")
    
    async def log_config_change(self, user_id: str, what_changed: str, 
                               old_value: str, new_value: str, ip_address: str):
        async with async_session() as session:
            log = AuditLog(
                event_type='config_change',
                user_id=user_id,
                ip_address=ip_address,
                resource=what_changed,
                action='modify',
                result='success',
                details={
                    'old_value': old_value,
                    'new_value': new_value
                }
            )
            session.add(log)
            await session.commit()
            
            logger.info(f"Config change: {what_changed} by {user_id}")
    
    async def log_payment_transaction(self, user_id: str, amount: int, 
                                     payment_intent_id: str, success: bool,
                                     ip_address: str):
        async with async_session() as session:
            log = AuditLog(
                event_type='payment',
                user_id=user_id,
                ip_address=ip_address,
                resource='payment_intent',
                action='create',
                result='success' if success else 'failure',
                details={
                    'amount': amount,
                    'payment_intent_id': payment_intent_id
                }
            )
            session.add(log)
            await session.commit()
            
            logger.info(f"Payment: user={user_id}, amount=${amount/100:.2f}, success={success}")
