from asyncio import sleep
from peak import DynamicAgent, OneShotBehaviour, CyclicBehaviour, Template,  getLogger, log , Message

logger = getLogger(__name__)


class Receiver(DynamicAgent): 
    class HelloWorldBehaviour(OneShotBehaviour):
        async def run(self):
            logger.info("waiting for message")
            msg = await self.receive()
            if msg:
                logger.info("message received")
                if msg.body == "Hello World":
                    print(f"{msg.sender} sent me a message: '{msg.body}'")
            list_of_behaviours = await self.agent.list_behaviours()  # Corrected line
            print(list_of_behaviours)
            while list_of_behaviours == "No dynamic behaviours available.":
                await sleep(10)
                list_of_behaviours = await self.agent.list_behaviours()
                print(list_of_behaviours)
            # list is a dict with the behaviours available, i want to pop the key and get the key value
            keys = list(list_of_behaviours.keys())
            print(keys)
            id = keys[0]
            msg_i = Message (to="sender@localhost")
            msg_i.set_metadata("performative", "run_behaviour")
            msg_i.body = id
            await self.send(msg_i)


    async def setup(self):
        await self.setup_dynamic()
        self.helloWorldBehaviour = self.HelloWorldBehaviour()
        self.add_behaviour(self.helloWorldBehaviou)

