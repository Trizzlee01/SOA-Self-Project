import pickle
import uuid
import redis
from nameko.extensions import DependencyProvider

class SessionWrapper:
    def __init__(self, connection):
        self.redis = connection
        self.default_expiration = 60 * 60

    def generate_session_id(self):
        key = str(uuid.uuid4())
        while self.redis.exist(key):
            key = str(uuid.uuid4())
        return key
    
    def set_session(self, user_data):
        # Pickle User Data so that can be stored in Redis
        user_data_pickled = pickle.dumps(user_data)

        # Get Session ID
        session_id = self.generate_session_id()

        # Store Session Data with Expire Time in Redis
        self.redis.set(session_id, user_data_pickled, ex=self.default_expire)

        return session_id

    def get_session(self, session_id):
        # Get the Data from Redis
        result = self.redis.get(session_id)

        if result:
            # Unpack the user data from Redis
            user_data = pickle.loads(result)
        else:
            user_data = None

        return user_data

    def delete_session(self, sessionId):
        self.redis.delete(sessionId)
        return 1


class SessionProvider(DependencyProvider):
    def __init__(self):
        self.client = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def get_dependency(self, worker_ctx):
        return SessionWrapper(self.client)
