import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from data.release import Release


class Package(SqlAlchemyBase):
    __tablename__ = 'packages'

    id: str = sa.Column(sa.String, primary_key=True)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    last_updated: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    summary: str = sa.Column(sa.String, nullable=False)
    description: str = sa.Column(sa.String, nullable=True)

    home_page: str = sa.Column(sa.String)
    docs_url: str = sa.Column(sa.String)
    package_url: str = sa.Column(sa.String)

    author_name: str = sa.Column(sa.String)
    author_email: str = sa.Column(sa.String, index=True)

    license: str = sa.Column(sa.String, index=True)

    # releases relationship
    releases: List[Release] = orm.relationship("Release", order_by=[
        Release.major_ver.desc(),
        Release.minor_ver.desc(),
        Release.build_ver.desc(),
    ], back_populates='package')

    def __repr__(self):
        return '<Package {}>'.format(self.id)


# p = Package()  # one query
#
# print(p.id)
# print("All releases")
# for r in p.releases:
#     print("{}.{}.{}".format(r.major_ver, r.minor_ver, r.build_ver))

# class Package:
#
#     def __init__(self,
#                  package_name: str,
#                  summary: str,
#                  description: str,
#                  home_page: str,
#                  lic: str,
#                  author_name: str,
#                  maintainers: list = None,
#                  ):
#         if maintainers is None:
#             maintainers = []
#         self.maintainers = maintainers
#         self.author_name = author_name
#         self.license = lic
#         self.home_page = home_page
#         self.description = description
#         self.summary = summary
#         self.package_name = package_name
#         self.id = package_name
