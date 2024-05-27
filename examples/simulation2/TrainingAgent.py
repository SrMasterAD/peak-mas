from asyncio import sleep
from peak import Agent, JoinCommunity, LeaveCommunity, Message, OneShotBehaviour, Template
import random

class TrainingAgent(Agent):
    class TrainingBehaviour(OneShotBehaviour):
        async def on_start(self):
            await self.wait_for(
                JoinCommunity("training_group", f"conference.{self.agent.jid.domain}")
            )

        async def run(self):
            for _ in range(30):  # Assumindo 30 iterações
                # Aguarda receber modelo do servidor
                msg = await self.receive() 
                print(msg.body)
                if msg and "modelA" in msg.body:
                    # Simula o treino com um tempo aleatório entre 5 a 10 segundos
                    await sleep(random.randint(5, 10))
                    # Gera um resultado de treino hipotético
                    training_result = random.randint(0,1)
                    # Envia o resultado para o servidor
                    result_msg = Message(to=f"training_group@conference.{self.agent.jid.domain}", metadata={"agente":"trabalho"})
                    result_msg.body = f"Result: {training_result}"
                    await self.send_to_community(result_msg)
            self.kill()

        async def on_end(self):
            await self.wait_for(
                LeaveCommunity("training_group", f"conference.{self.agent.jid.domain}")
            )
            await self.agent.stop()

    async def setup(self):
        template = Template()
        template.sender = f"training_group@conference.{self.jid.domain}/server"
        self.add_behaviour(self.TrainingBehaviour(), template=template)
