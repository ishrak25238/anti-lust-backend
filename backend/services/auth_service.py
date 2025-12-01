from sqlalchemy.future import select
from database import async_session, User, AccountType
from passlib.context import CryptContext
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    async def create_user(self, email: str, account_type: str, pin: str):
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            if result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="User already exists")
            
            pin_hash = pwd_context.hash(pin)
            
            user = User(
                email=email,
                account_type=account_type,
                pin_hash=pin_hash
            )
            session.add(user)
            await session.commit()
            return user

    async def verify_pin(self, email: str, pin: str) -> bool:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                return False
            
            return pwd_context.verify(pin, user.pin_hash)

    async def switch_to_parent_mode(self, email: str, pin: str):
        """
        Irreversible switch to Parent Mode.
        Once enabled, cannot go back to Self Mode easily.
        """
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            if not pwd_context.verify(pin, user.pin_hash):
                raise HTTPException(status_code=401, detail="Invalid PIN")
            
            user.account_type = AccountType.PARENT.value
            await session.commit()
            logger.info(f"User {email} switched to IRREVERSIBLE PARENT MODE")
            return True

    async def set_emergency_mode(self, email: str, enabled: bool, pin: str):
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            if not pwd_context.verify(pin, user.pin_hash):
                raise HTTPException(status_code=401, detail="Invalid PIN")
            
            user.emergency_mode = enabled
            await session.commit()
            return True
