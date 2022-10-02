import datetime
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select

from data.package import Package
from data.release import Release
from data import db_session
import sqlalchemy.orm


# def release_count() -> int:
#     return 2_234_847
#
#
# def package_count() -> int:
#     return 274_000
#
#
# def latest_packages(limit: int = 5) -> List:
#     return [
#                {'id': 'fastapi', 'summary': "A great web framework"},
#                {'id': 'uvicorn', 'summary': "Your favorite ASGI server"},
#                {'id': 'httpx', 'summary': "Requests for an async world"},
#            ][:limit]
#
#
# def get_package_by_id(package_name: str) -> Optional[Package]:
#     package = Package(
#         package_name, "This is the summary", "Full details here!",
#         "https://fastapi.tiangolo.com/", "MIT", "Sebastián Ramírez"
#     )
#     return package
#
#
# def get_latest_release_for_package(package_name: str) -> Optional[Release]:
#     return Release("1.2.0", datetime.datetime.now())

# def release_count() -> int:
#     session = db_session.create_session()
#
#     try:
#         return session.query(Release).count()
#     finally:
#         session.close()
async def release_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Release.id))
        results = await session.execute(query)

        return results.scalar()


# def package_count() -> int:
#     session = db_session.create_session()
#
#     try:
#         return session.query(Package).count()
#     finally:
#         session.close()
async def package_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Package.id))
        results = await session.execute(query)

        return results.scalar()


# def latest_packages(limit: int = 5) -> List[Package]:
#     session = db_session.create_session()
#
#     try:
#         releases = session.query(Release) \
#             .options(
#             sqlalchemy.orm.joinedload(Release.package)
#         ) \
#             .order_by(Release.created_date.desc()) \
#             .limit(limit) \
#             .all()
#     finally:
#         session.close()
#
#     return list({r.package for r in releases})
async def latest_packages(limit: int = 5) -> List[Package]:
    async with db_session.create_async_session() as session:
        query = select(Release) \
            .options(
            sqlalchemy.orm.joinedload(Release.package)) \
            .order_by(Release.created_date.desc()) \
            .limit(limit)

        results = await session.execute(query)
        releases = results.scalars()

        return list({r.package for r in releases})


# def get_package_by_id(package_name: str) -> Optional[Package]:
#     session = db_session.create_session()
#
#     try:
#         package = session.query(Package).filter(Package.id == package_name).first()
#         return package
#     finally:
#         session.close()
async def get_package_by_id(package_name: str) -> Optional[Package]:
    async with db_session.create_async_session() as session:
        query = select(Package).filter(Package.id == package_name)
        result = await session.execute(query)

        return result.scalar_one_or_none()


# def get_latest_release_for_package(package_name: str) -> Optional[Release]:
#     session = db_session.create_session()
#
#     try:
#         release = session.query(Release) \
#             .filter(Release.package_id == package_name) \
#             .order_by(Release.created_date.desc()) \
#             .first()
#
#         return release
#     finally:
#         session.close()
async def get_latest_release_for_package(package_name: str) -> Optional[Release]:
    async with db_session.create_async_session() as session:
        query = select(Release) \
            .filter(Release.package_id == package_name) \
            .order_by(Release.created_date.desc())

        results = await session.execute(query)
        release = results.scalar()

        return release
