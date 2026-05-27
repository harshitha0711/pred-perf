import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


class InMemoryCollection:
    def __init__(self):
        self._data = []

    def insert_one(self, doc: dict):
        # create a simple inserted_id placeholder
        from uuid import uuid4
        doc = dict(doc)
        doc.setdefault("_id", str(uuid4()))
        self._data.append(doc)
        class R: inserted_id = doc["_id"]
        return R()

    def find_one(self, query: dict):
        for d in self._data:
            ok = True
            for k, v in query.items():
                if d.get(k) != v:
                    ok = False
                    break
            if ok:
                return d
        return None

    def find(self, query: dict = None):
        if not query:
            return list(self._data)
        out = []
        for d in self._data:
            ok = True
            for k, v in query.items():
                if d.get(k) != v:
                    ok = False
                    break
            if ok:
                out.append(d)
        return out


if not MONGO_URI:
    # No URI set — use in-memory collections so the app remains runnable locally.
    users_collection = InMemoryCollection()
    history_collection = InMemoryCollection()
else:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client["student_app"]
        users_collection = db["users"]
        history_collection = db["history"]
    except Exception as e:
        # If MongoDB is unreachable (DNS/Network), fall back to in-memory stores
        # and log the error for the developer.
        import warnings
        warnings.warn(f"MongoDB unavailable, falling back to in-memory DB. Details: {e}")
        users_collection = InMemoryCollection()
        history_collection = InMemoryCollection()
