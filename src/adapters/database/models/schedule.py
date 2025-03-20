import datetime as dt

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Schedule(BaseModel):
    __tablename__ = "schedule"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    medicine_name = Column(String, nullable=False)
    duration_days = Column(
        Integer, nullable=True
    )  # если поле null, то прием постоянный
    periodicity_hours = Column(Integer, nullable=False)

    user = relationship("User", back_populates="schedule")

    @property
    def is_active(self) -> bool:
        now_date = dt.datetime.now().date()
        duration_date = now_date + dt.timedelta(days=int(self.duration_days))
        return now_date <= duration_date

