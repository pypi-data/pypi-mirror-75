from flask_boiler.context import Context as CTX
CTX.load()

engine = CTX.services.engine


from flask_boiler.view import Mediator


class TodoMediator(Mediator):

    from flask_boiler.source.leancloud import before_save
    src = before_save('Todo')

    @src.triggers.before_save
    def fb_before_todo_save(self, ref, snapshot):
        raise ValueError(f"{str(ref)} {str(snapshot)}")

    @classmethod
    def start(cls):
        cls.src.start()

