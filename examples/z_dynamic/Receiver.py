import uuid
from peak import Agent, OneShotBehaviour, CyclicBehaviour, DynamicBehaviourManager, Template,  getLogger, log

logger = getLogger(__name__)


class Receiver(Agent, DynamicBehaviourManager): 
    class ReceiveHelloWorld(OneShotBehaviour):
        async def run(self):
            logger.info("waiting for message")
            msg = await self.receive()
            if msg:
                logger.info("message received")
                print(f"{msg.sender} sent me a message: '{msg.body}'")
                if msg.get_metadata("performative") == "add_behaviour":
                    behaviour_instance = await self.agent.add_dynamic_behaviour(msg.body)
                    print (f"Behaviour added: {behaviour_instance}")
                    print (f"old behaviours: {self.agent.receiveHelloWorld}")    
                    self.agent.add_behaviour(behaviour_instance)
                        
                        

    async def setup(self):
        self.receiveHelloWorld = self.ReceiveHelloWorld()
        self.dynamic_behaviours = {}
        self.dynamic_behaviours[0] = self.receiveHelloWorld
        template_add = Template()
        template_add.set_metadata("performative", "add_behaviour")
        self.add_behaviour(self.ReceiveHelloWorld(), template=template_add)

    async def funcFim(self):
        print("Fim")
        await self.stop()