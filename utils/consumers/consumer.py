from channels.generic.websocket import AsyncJsonWebsocketConsumer

class Consumer(AsyncJsonWebsocketConsumer):
    def __init__(self, room, *args, private = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        self.private = private

    async def connect(self):
        try:
            self.user = self.scope.get('user')
            if self.user.is_anonymous:
                await self.close()

            if self.private:
                self.room = f'{self.user.username}_' + self.room
            if self.room:
                await self.accept()
                await self.channel_layer.group_add(self.room, self.channel_name)
                await self.send()
            else:
                await self.close()
        except:
            await self.close()

    async def disconnect(self, code):
        if self.room is not None:
            await self.channel_layer.group_discard(self.room, self.channel_name)

    async def send():
        pass

    # async def receive(self, text_data):
    #     await self.channel_layer.group_send(
    #         self.room,
    #         {
    #             'type': 'notificate',
    #             'event': self.event,
    #             'message': json.loads(text_data)
    #         }
    #     )

    async def notificate(self, event):
        await self.send_json(event)
