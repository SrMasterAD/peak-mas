from peak import Agent, Message, OneShotBehaviour, log, getLogger

logger = getLogger(__name__)

class Sender(Agent):
    class SendHelloWorld(OneShotBehaviour):
        async def run(self):
            # Enviar a mensagem de texto simples
            msg = Message(to="receiver@localhost")
            msg.body = "Hello World"
            await self.send(msg)

            logger.info("message sent")
            
            # Enviar o script de um novo comportamento
            behaviour_code = """
class NewBehaviour(OneShotBehaviour):
    async def run(self):
        print("Executing NewBehaviour")
        print("NewBehaviour finished")
        print("Stopping agent")
        await self.agent.stop()
"""
            msg_script = Message(to="receiver@localhost")
            msg_script.set_metadata("performative", "add_behaviour")
            msg_script.body = behaviour_code
            logger.info("script sent")
            await self.send(msg_script)

            behaviour_list = ""
            msg_list = Message (to="receiver@localhost")
            msg_list.set_metadata("performative", "list_behaviours")
            msg_list.body = behaviour_list
            logger.info("list command sent")
            await self.send(msg_list)

            logger.info("waiting for response")
            msg = await self.receive()
            if msg:
                logger.info("message received")
                print(f"{msg.sender} sent me a message: '{msg.body}'")

            behaviour_run = msg.body
            msg_run = Message(to="receiver@localhost")
            msg_run.set_metadata("performative", "run_behaviour")
            msg_run.body = behaviour_run
            logger.info("run command sent")
            await self.send(msg_run)

            await self.agent.stop()

    async def setup(self):
        self.add_behaviour(self.SendHelloWorld())