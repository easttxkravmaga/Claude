import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    BigInteger,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


def _utcnow() -> datetime:
    return datetime.utcnow()


def _new_group_id() -> str:
    return str(uuid.uuid4())


class Provider(str, Enum):
    linkedin = "linkedin"
    meta = "meta"


class RefreshStatus(str, Enum):
    success = "success"
    failed = "failed"
    pending = "pending"


class Platform(str, Enum):
    facebook = "facebook"
    instagram = "instagram"
    linkedin = "linkedin"


class MediaType(str, Enum):
    none = "none"
    image = "image"
    video = "video"


class PostStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    posting = "posting"
    processing = "processing"
    posted = "posted"
    failed = "failed"


class BatchSource(str, Enum):
    csv = "csv"
    xlsx = "xlsx"
    manual = "manual"
    ai = "ai"


class OAuthCredential(Base):
    __tablename__ = "oauth_credentials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[Provider] = mapped_column(SQLEnum(Provider), nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    client_id: Mapped[str] = mapped_column(String(255), nullable=False)
    client_secret_enc: Mapped[str] = mapped_column(Text, nullable=False)
    access_token_enc: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token_enc: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    person_urn: Mapped[str | None] = mapped_column(String(255), nullable=True)
    page_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ig_account_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    last_refresh_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_refresh_status: Mapped[RefreshStatus | None] = mapped_column(
        SQLEnum(RefreshStatus), nullable=True
    )
    last_refresh_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )

    __table_args__ = (
        Index("ix_oauth_provider_label", "provider", "label", unique=True),
    )


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    source: Mapped[BatchSource] = mapped_column(SQLEnum(BatchSource), nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="batch")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_group_id: Mapped[str] = mapped_column(
        String(36), default=_new_group_id, nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=False, default="")
    platform: Mapped[Platform] = mapped_column(SQLEnum(Platform), nullable=False)

    media_type: Mapped[MediaType] = mapped_column(
        SQLEnum(MediaType), default=MediaType.none, nullable=False
    )
    media_gcs_path: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    media_mime: Mapped[str | None] = mapped_column(String(64), nullable=True)
    media_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    media_duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    media_aspect_ratio: Mapped[str | None] = mapped_column(String(8), nullable=True)

    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    campaign_tag: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)

    status: Mapped[PostStatus] = mapped_column(
        SQLEnum(PostStatus), default=PostStatus.draft, nullable=False
    )
    approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    platform_post_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    post_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    batch_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("batches.id"), nullable=True
    )
    batch: Mapped[Batch | None] = relationship("Batch", back_populates="posts")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )
    posted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_posts_status_scheduled_at", "status", "scheduled_at"),
        Index("ix_posts_platform_posted_at", "platform", "posted_at"),
    )
