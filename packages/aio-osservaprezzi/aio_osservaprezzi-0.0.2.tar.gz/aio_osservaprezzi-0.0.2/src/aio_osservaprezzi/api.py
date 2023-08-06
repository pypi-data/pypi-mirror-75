from .const import ENDPOINT, REGIONS


class API:
    def __init__(self, loop, session, data):
        """Initialize the class."""
        self.loop = loop
        self.session = session
        self.data = data

    async def get_data(self):
        r = await self.session.post(
            ENDPOINT,
            data=f"region={REGIONS[self.data['region']]}\
                &province={self.data['province']}\
                &town={self.data['town']}\
                &carb=",
            ssl=False,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        json = await r.json()
        return json["array"]

    async def get_data_by_id(self, id):
        return next(filter(lambda d: d["id"] == id, await self.get_data()))
