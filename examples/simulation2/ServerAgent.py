from asyncio import sleep
from peak import Agent, JoinCommunity, LeaveCommunity, Message, OneShotBehaviour, Template
import json

class ServerAgent(Agent):
    class ManageTraining(OneShotBehaviour):

        async def on_start(self):
            await self.wait_for(
                JoinCommunity("training_group", f"conference.{self.agent.jid.domain}")
            )
            self.graph_json = {
                "title": {"text": "Confidence Band", "subtext": "Example in MetricsGraphics.js", "left": "center"},
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross", "animation": False, "label": {"backgroundColor": "#ccc", "borderColor": "#aaa", "borderWidth": 1, "shadowBlur": 0, "shadowOffsetX": 0, "shadowOffsetY": 0, "color": "#222"}}},
                "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
                "xAxis": {"type": "category", "data": [], "boundaryGap": False},
                "yAxis": {"splitNumber": 3},
                "series": [
                    {"name": "L", "type": "line", "data": [], "lineStyle": {"opacity": 0}, "stack": "confidence-band", "symbol": "none"},
                    {"name": "U", "type": "line", "data": [], "lineStyle": {"opacity": 0}, "areaStyle": {"color": "#ccc"}, "stack": "confidence-band", "symbol": "none"},
                    {"type": "line", "data": [], "itemStyle": {"color": "#333"}, "showSymbol": False}
                ]
            }

        async def wait_for_members(self):
            # Esperar até que o número mínimo de agentes esteja presente
            while True:
                members = await self.community_members(f"training_group@conference.{self.agent.jid.domain}")
                count = 0
                for _ in members:
                    count += 1
                print(count)
                if count >= 3:  # Verificar se o número mínimo de agentes (2) está presente
                    break
                await sleep(2)

        async def run(self):
            await self.wait_for_members() # Aguardar agentes suficientes
            # Iniciar treino
            for i in range(30):  # 30 iterações de treino
                msg = Message(to=f"training_group@conference.{self.agent.jid.domain}")  
                msg.body = "modelA"
                print(msg.body)
                await self.send_to_community(msg) # Envia o modelo para os agentes
                training_results = []
                for _ in range(2):  # Assumindo 2 agentes para simplificação
                    result_msg = await self.receive() # Aguarda resultado do agente
                    if result_msg and (result_msg.body.split(": ")[1] in ['0', '1']):
                        result_value = int(result_msg.body.split(": ")[1]) # Obtém o resultado
                        training_results.append(result_value) # Armazena o resultado
                
                if training_results:
                    max_result = max(training_results)
                    average_result = sum(training_results) / len(training_results) # Calcula a média dos resultados
                    print(f"Average training result: {average_result}") # Exibe a média dos resultados
                    # Atualizar JSON do gráfico
                    self.graph_json['xAxis']['data'].append(str(i))
                    self.graph_json['series'][2]['data'].append(average_result)
                    self.graph_json['series'][0]['data'].append(max_result)
                    # Enviar gráfico atualizado
                    graph_msg = Message(to=f"training_group_ui@conference.{self.agent.jid.domain}")
                    graph_msg.body = json.dumps(self.graph_json)
                    await self.send_to_community(graph_msg)

            self.kill()

        async def on_end(self):
            await self.wait_for(
                LeaveCommunity("training_group", f"conference.{self.agent.jid.domain}")
            )
            await self.agent.stop()

    async def setup(self):
        template = Template()
        template.metadata = {"agente": "trabalho"}
        self.add_behaviour(self.ManageTraining(), template=template)
