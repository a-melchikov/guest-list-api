from app.repositories.base import AbstractRepository


class BaseService:
    def __init__(self, repo: AbstractRepository):
        self.repo: AbstractRepository = repo
