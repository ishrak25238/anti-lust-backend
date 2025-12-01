from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict
from datetime import datetime
import hashlib
from database import Base, async_session

class ParentChildLink(Base):
    __tablename__ = "parent_child_links"
    
    id = Column(Integer, primary_key=True)
    parent_email = Column(String, index=True)
    child_code = Column(String, unique=True)
    child_name = Column(String)
    device_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ThreatLogModel(Base):
    __tablename__ = "threat_logs"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, ForeignKey("parent_child_links.device_id"))
    source = Column(String)
    reason = Column(String)
    context = Column(Text)
    timestamp = Column(DateTime)

class SyncService:
    async def link_accounts(self, parent_email: str, child_code: str, child_name: str) -> str:
        async with async_session() as session:
            result = await session.execute(
                select(ParentChildLink).where(ParentChildLink.child_code == child_code)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                existing.parent_email = parent_email
                existing.child_name = child_name
                await session.commit()
                return existing.device_id
            else:
                raise Exception("Invalid pairing code")
    
    async def store_logs(self, logs: List[Dict]):
        async with async_session() as session:
            for log_data in logs:
                log = ThreatLogModel(
                    device_id=log_data['device_id'],
                    source=log_data['source'],
                    reason=log_data['reason'],
                    context=log_data['context'],
                    timestamp=datetime.fromisoformat(log_data['timestamp'])
                )
                session.add(log)
            await session.commit()
    
    async def get_logs_for_parent(self, parent_email: str) -> List[Dict]:
        async with async_session() as session:
            result = await session.execute(
                select(ParentChildLink).where(ParentChildLink.parent_email == parent_email)
            )
            links = result.scalars().all()
            
            all_logs = []
            for link in links:
                logs_result = await session.execute(
                    select(ThreatLogModel).where(ThreatLogModel.device_id == link.device_id)
                )
                logs = logs_result.scalars().all()
                
                for log in logs:
                    all_logs.append({
                        "device_id": log.device_id,
                        "source": log.source,
                        "reason": log.reason,
                        "context": log.context,
                        "timestamp": log.timestamp.isoformat()
                    })
            
            return all_logs
    
    async def get_logs_by_device(self, device_id: str) -> List[Dict]:
        async with async_session() as session:
            result = await session.execute(
                select(ThreatLogModel).where(ThreatLogModel.device_id == device_id)
            )
            logs = result.scalars().all()
            
            return [{
                "device_id": log.device_id,
                "source": log.source,
                "reason": log.reason,
                "context": log.context,
                "timestamp": log.timestamp.isoformat()
            } for log in logs]
