import requests
from . import VERSION


class WavesClient:
    """Cliente HTTP para comunicação com Waves

    :param str waves_url: Endereço da API do Waves
    :param str api_key: Chave de API para autenticação
    """

    def __init__(self, waves_url, api_key):
        self.waves_url = waves_url
        self.api_key = api_key

    def get_workflow(self, identifier):
        """Obtem um fluxo por ID

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            workflow = client.get_workflow('aweeds@v1.0.2')

        :param identifier: Id do fluxo desejado
        :type identifier: str
        :return: Objeto do fluxo
        :rtype: dict
        """
        response = requests.get(
            '{}/api/workflows/{}'.format(self.waves_url, identifier),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def create_workflow(self, workflow):
        """Cria um novo fluxo

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            workflow = client.create_workflow({
                'name': 'workflow',
                'steps': []
            })

        :param workflow: Fluxo a ser criado
        :type workflow: dict
        :return: Objeto do fluxo criado
        :rtype: dict
        """
        response = requests.post(
            '{}/api/workflows'.format(self.waves_url),
            headers=self._get_headers(),
            json=workflow)
        response.raise_for_status()
        return response.json()

    def archive_workflow(self, identifier):
        """Arquiva um fluxo

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            workflow = client.archive_workflow('workflow_identifier')

        :param identifier: Id do fluxo desejado
        :type identifier: str
        :return: Objeto do fluxo arquivado
        :rtype: dict
        """
        response = requests.put(
            '{}/api/workflows/{}/archive'.format(self.waves_url, identifier),
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def unarchive_workflow(self, identifier):
        """Desarquiva um fluxo

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            workflow = client.unarchive_workflow('workflow_identifier')

        :param identifier: Id do fluxo desejado
        :type identifier: str
        :return: Objeto do fluxo desarquivado
        :rtype: dict
        """
        response = requests.put(
            '{}/api/workflows/{}/unarchive'.format(self.waves_url, identifier),
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def list_executions(self, term=None, status=None, sort_by=None, page=None, size=None):
        """Busca execuções com os filtros passados

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            executions = client.list_executions()

        :param term: Palavra-chave de busca (Identificador, descrição ou fluxo)
        :type term: str, opcional
        :param status: Lista de status desejados (Status possíveis: QUEUED, SUCCESS, CANCELED, FAILURE, STARTED) 
        :type status: list, opcional
        :param sort_by: Nome da coluna para ordenação. Utilize "-" para ordem decrescente
        :type sort_by: str, opcional
        :param page: Número da página atual 
        :type page: int, opcional
        :param size: Tamanho da página
        :type size: int, opcional
        :return: Objeto da paginação contendo as chaves "meta" e "objects"
        :rtype: dict
        """
        response = requests.get(
            '{}/api/executions'.format(self.waves_url),
            headers=self._get_headers(),
            params={
                'term': term, 
                'status': status,
                'sort_by': sort_by, 
                'page': page, 
                'size': size
            }
        )
        response.raise_for_status()
        return response.json()

    def get_execution(self, identifier):
        """Obtem uma execução por ID

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            execution = client.get_execution('Jun-26-8857')

        :param identifier: Id da execução desejada
        :type identifier: str
        :return: Objeto da execução
        :rtype: dict
        """
        response = requests.get(
            '{}/api/executions/{}'.format(self.waves_url, identifier),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def create_execution(self, workflow_identifier, inputs, description=None):
        """Cria uma execução a partir de um fluxo e uma lista de entradas

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            execution = client.create_execution('aweeds@v1.0.2', {'shapefile': 's3://file.zip'})

        :param workflow_identifier: Id do fluxo
        :type workflow_identifier: str
        :param inputs: Entradas do fluxo no formato chave:valor
        :type inputs: dict
        :param description: Descrição da execução
        :type description: str, opcional
        :return: Objeto da execução criada
        :rtype: dict
        """
        response = requests.post(
            '{}/api/executions'.format(self.waves_url),
            headers=self._get_headers(),
            json={
                "workflow_identifier": workflow_identifier,
                "inputs": inputs,
                "description": description
            })
        response.raise_for_status()
        return response.json()

    def update_execution(self, identifier, description=None):
        """Atualiza os dados de uma execução. Atualmente só é possível atualizar a sua descrição

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            execution = client.update_execution('Jun-26-8331', 'nova descrição')

        :param identifier: Id da execução
        :type identifier: str
        :param description: Nova descrição da execução
        :type description: str
        :return: Objeto da execução atualizada
        :rtype: dict
        """
        response = requests.put(
            '{}/api/executions/{}'.format(self.waves_url, identifier),
            headers=self._get_headers(),
            json={
                "description": description
            })
        response.raise_for_status()
        return response.json()

    def delete_execution(self, identifier):
        """Realiza um SOFT DELETE na execução desejada

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            client.delete_execution('Jun-26-8331')

        :param identifier: Id da execução
        :type identifier: str
        """
        response = requests.delete(
            '{}/api/executions/{}'.format(self.waves_url, identifier),
            headers=self._get_headers())
        response.raise_for_status()

    def create_businesstask(self, btask):
        """Cria uma nova tarefa

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            btask = client.create_businesstask({
                'name': 'btask',
                'runs_on': 'awsasg',
                'docker_registry': 'ubuntu:latest'})

        :param btask: Tarefa a ser criada
        :type btask: dict
        :return: Objeto da tarefa criada
        :rtype: dict
        """
        response = requests.post(
            '{}/api/business-tasks'.format(self.waves_url),
            headers=self._get_headers(),
            json=btask)
        response.raise_for_status()
        return response.json()

    def publish_businesstask(self, identifier):
        """Pública uma tarefa não publicada

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            btask = client.publish_businesstask('btask_identifier')

        :param identifier: Id da tarefa
        :type identifier: str
        :return: Objeto da tarefa publicada
        :rtype: dict
        """
        response = requests.put(
            '{}/api/business-tasks/{}/publish'.format(self.waves_url, identifier),
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def unpublish_businesstask(self, identifier):
        """Despública uma tarefa publicada

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            btask = client.unpublish_businesstask('btask_identifier')

        :param identifier: Id da tarefa
        :type identifier: str
        :return: Objeto da tarefa despublicada
        :rtype: dict
        """
        response = requests.put(
            '{}/api/business-tasks/{}/unpublish'.format(self.waves_url, identifier),
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def list_workers(self):
        """Lista os workers da aplicação

        Exemplo:

        .. code-block:: python

            from stl_sdk.waves import WavesClient

            client = WavesClient('https://waves-dev.spacetimeanalytics.com', 'api_key')
            workers = client.list_workers()

        :return: Objeto dos workers da aplicação
        :rtype: dict
        """
        response = requests.get(
            '{}/api/workers'.format(self.waves_url),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def _get_headers(self):
        headers = {
            'User-Agent': 'stl-sdk/{}'.format(VERSION),
            'X-API-KEY': self.api_key
        }
        return headers
