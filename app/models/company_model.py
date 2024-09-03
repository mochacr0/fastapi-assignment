from sqlalchemy import Column, String, Double, Enum
from sqlalchemy.orm import relationship

from app.commons.enums import CompanyMode
from app.models.base_model import BaseModel


class Company(BaseModel):
    __tablename__ = "companies"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(Enum(CompanyMode), nullable=True)
    rating = Column(Double, nullable=True)
    users = relationship("User", back_populates="company")

    def __repr__(self):
        return f"<Company {self.name}>"
