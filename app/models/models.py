from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class GoogleApp(Base):
    __tablename__ = "apps"

    app_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    app_name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    rating_count: Mapped[float] = mapped_column(Float, nullable=True)
    installs: Mapped[str] = mapped_column(String, nullable=True)
    minimum_installs: Mapped[int] = mapped_column(BigInteger, nullable=True) 
    maximum_installs: Mapped[int] = mapped_column(BigInteger, nullable=True)
    free: Mapped[bool] = mapped_column(Boolean, default=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[str] = mapped_column(String, nullable=True)
    minimum_android: Mapped[str] = mapped_column(String, nullable=True)
    developer_id: Mapped[str] = mapped_column(String, nullable=True)
    developer_website: Mapped[str] = mapped_column(String, nullable=True)
    developer_email: Mapped[str] = mapped_column(String, nullable=True)
    released: Mapped[str] = mapped_column(String, nullable=True)
    last_updated: Mapped[str] = mapped_column(String, nullable=True)
    content_rating: Mapped[str] = mapped_column(String, nullable=True)
    privacy_policy: Mapped[str] = mapped_column(String, nullable=True)
    ad_supported: Mapped[bool] = mapped_column(Boolean, default=False)
    in_app_purchases: Mapped[bool] = mapped_column(Boolean, default=False)
    editors_choice: Mapped[bool] = mapped_column(Boolean, default=False)
    scraped_time: Mapped[str] = mapped_column(String, nullable=True)