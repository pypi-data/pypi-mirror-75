from flask_boiler.context import Context as CTX

CTX.load()

engine = CTX.services.engine


from flask_boiler.view import Mediator

# JSONRPC_URI = 'http://jsonrpc.multiri.de'
JSONRPC_URI = 'http://0.0.0.0:5000'

class TodoMediatorLc(Mediator):

    from flask_boiler.source.leancloud import hook
    from flask_boiler.sink.json_rpc import sink

    src = hook('Todo')
    snk = sink(uri=f'{JSONRPC_URI}/todo')

    @src.triggers.after_save
    def call_after_save_rpc(self, ref, snapshot):
        self.snk.emit('after_save', ref=str(ref), snapshot=snapshot.to_dict())
    #
    # @src.triggers.before_save
    # def fb_before_todo_save(self, ref, snapshot):
    #     from flask_boiler.database.firestore import FirestoreReference
    #     CTX.dbs.firestore.set(ref=FirestoreReference.from_str(str(ref)), snapshot=snapshot)
    #     raise ValueError(f"{str(ref)} {str(snapshot)}")

    @classmethod
    def start(cls):
        cls.src.start()

#
# class TodoMediator(Mediator):
#
#     from flask_boiler.source.json_rpc import JsonRpcSource as source
#     src = source(url_prefix='todo')
#
#     @src.triggers.after_save
#     def record_todo(self, response):
#         from jsonrpcclient import Response
#         assert isinstance(response, Response)
#         if response.data.ok:
#             res = response.data.result
#             ref = res['ref']
#             snapshot = res['snapshot']
#             self._fb_before_todo_save(ref=ref, snapshot=snapshot)
#         else:
#             raise Exception(response.raw)
#
#     def _fb_before_todo_save(self, ref, snapshot):
#         from flask_boiler.database.firestore import FirestoreReference
#         CTX.dbs.firestore.set(ref=FirestoreReference.from_str(str(ref)), snapshot=snapshot)
#         raise ValueError(f"{str(ref)} {str(snapshot)}")
