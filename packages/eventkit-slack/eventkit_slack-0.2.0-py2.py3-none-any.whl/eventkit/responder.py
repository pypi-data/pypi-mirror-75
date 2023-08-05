from functools import wraps


class EventResponder:
    def __init__(self):
        self.event_handlers = {}
        self.action_handlers = {}
        self.view_handlers = {}
        self.message_action_handlers = {}

    @staticmethod
    def _get_action_key(block_id="", action_id=""):
        return ",".join((block_id, action_id))

    def event(self, event_type):
        def wrapper(func):
            @wraps(func)
            async def decorator(*args, **kwargs):
                return await func(*args, **kwargs)

            self.event_handlers[event_type] = decorator
            return decorator

        return wrapper

    def action(self, action_id="", block_id=""):
        if not any((action_id, block_id)):
            raise ValueError("Please provide either action_id or block_id")

        def wrapper(func):
            @wraps(func)
            async def decorator(*args, **kwargs):
                return await func(*args, **kwargs)

            key = self._get_action_key(block_id, action_id)
            self.action_handlers[key] = decorator

            return decorator

        return wrapper

    def view_submission(self, callback_id):
        def wrapper(func):
            @wraps(func)
            async def decorator(*args, **kwargs):
                return await func(*args, **kwargs)

            self.view_handlers[callback_id] = decorator
            return decorator

        return wrapper

    def message_action(self, callback_id):
        def wrapper(func):
            @wraps(func)
            async def decorator(*args, **kwargs):
                return await func(*args, **kwargs)

            self.message_action_handlers[callback_id] = decorator
            return decorator

        return wrapper

    async def handle(self, request, payload):
        event_type = payload["type"]
        handler = None

        if event_type == "event_callback":
            event_type = payload["event"]["type"]
            handler = self.event_handlers.get(event_type)

        elif event_type == "block_actions":
            action = payload["actions"][0]
            block_id = action["block_id"]
            action_id = action["action_id"]

            id_combinations = ((block_id, action_id), ("", action_id), (block_id, ""))

            for block_id, action_id in id_combinations:
                key = self._get_action_key(block_id, action_id)
                handler = self.action_handlers.get(key)
                if handler:
                    break

        elif event_type == "view_submission":
            callback_id = payload["view"]["callback_id"]
            handler = self.view_handlers.get(callback_id)

        elif event_type == "message_action":
            callback_id = payload["callback_id"]
            print(callback_id)
            handler = self.message_action_handlers.get(callback_id)

        if handler:
            await handler(request, payload)
