import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = 'ed15c531-c76f-40b4-b960-0fd16f11b652'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'sum'
    is_public: bool = False
    displayName: str = 'Sum'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Sum of string and integer'
    properties: List[Property] = [
        Property(
            displayName='Поле для числа в формате string (строка)',
            name='string_number',
            type=Property.Type.STRING,
            description='string',
            required=True,
            default='0',
        ),
        Property(
            displayName='Поле для числа в формате int (целое число)',
            name='int_number',
            type=Property.Type.NUMBER,
            description='integer',
            required=True,
            default=0,
        ),
        Property(
            displayName='Вывести в формате строки',
            name='switch',
            type=Property.Type.BOOLEAN,
            description='bool switch',
            required=False,
            default=False,
        )

    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            try:
                string_number=int(json.node.data.properties['string_number'])
            except ValueError:
                raise ValueError ('В полях должны быть числа')
            int_number = json.node.data.properties['int_number']
            sum=string_number+int_number
            if (json.node.data.properties['switch']):
                sum=str(sum)
            await json.save_result({
                "result": sum
            })
            json.state = RunState.complete

        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
