from peak import Agent, Message, OneShotBehaviour


class Sender(Agent):
    class SendHelloWorld(OneShotBehaviour):
        async def run(self):
            # Enviar a mensagem de texto simples
            msg = Message(to="receiver@localhost")
            msg.body = "Hello World"
            await self.send(msg)
            
            # Enviar o script de um novo comportamento
            behaviour_code = """
class NewBehaviour(OneShotBehaviour):
    async def run(self):
        print("Executing NewBehaviour")
        await self.agent.funcFim()
"""
            msg_script = Message(to="receiver@localhost")
            msg_script.set_metadata("performative", "add_behaviour")
            msg_script.body = behaviour_code
            await self.send(msg_script)
            
            await self.agent.stop()

    async def setup(self):
        self.add_behaviour(self.SendHelloWorld())