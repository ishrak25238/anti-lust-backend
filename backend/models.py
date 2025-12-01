"""
Database models - imported from database.py for compatibility
"""
from database import (
    Base,
    User,
    GlobalBlocklist,
    AppPolicy,
    FapStreak,
    PreventedSite,
    IllegalContentAttempt,
    MonthlyReport,
    AccountType
)

__all__ = [
    'Base',
    'User',
    'GlobalBlocklist',
    'AppPolicy',
    'FapStreak',
    'PreventedSite',
    'IllegalContentAttempt',
    'MonthlyReport',
    'AccountType'
]
