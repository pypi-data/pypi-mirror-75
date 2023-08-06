import requests


class CoralClient:
    """Cliente HTTP para comunicação com Coral

    :param str coral_url: Endereço da API do serviço Coral
    :param str api_key: Chave de acesso a API
    :param str atlantis_client_id: Id do cliente que a chave de API foi emitida
    """

    def __init__(self, coral_url, api_key, atlantis_client_id):
        self.coral_url = coral_url
        self.api_key = api_key
        self.atlantis_client_id = atlantis_client_id

    def _get_headers(self, bucket, region=None):
        return {
            'bucket': bucket,
            'region': region,
            'atlantisclientid': self.atlantis_client_id,
            'x-api-key': self.api_key
        }

    def get_file(self, bucket, region, key):
        """Obtém informações de um determinado arquivo.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = CoralSyncClient('https://storage.spacetimeanalytics.com', 'apikey', 'atlantisclientid')
            file = client.get_file('spacetimelabs-bucket', 'us-west-2', '/folder/file.ext')

        :param bucket: Bucket do arquivo
        :type bucket: str
        :param region: Região do bucket
        :type region: str
        :param key: Chave do arquivo
        :type key: str
        :return: Objeto do arquivo
        :rtype: dict
        """
        response = requests.get(
                '{}/api/file'.format(self.coral_url),
                headers=self._get_headers(bucket, region=region),
                params={
                    'key': key
                }
            )
        response.raise_for_status()
        return response.json()


class CoralSyncClient(CoralClient):
    """Cliente HTTP para sincronização dos arquivos do banco de dados do Coral

    :param str coral_url: Endereço da API do serviço Coral
    :param str api_key: Chave de acesso a API
    :param str atlantis_client_id: Id do cliente que a chave de API foi emitida
    """

    def __init__(self, coral_url, api_key, atlantis_client_id):
        super().__init__(coral_url, api_key, atlantis_client_id)

    def upsert_file(self, bucket, key, last_modified, size, metadata=None):
        """Crie ou atualiza um arquivo no banco do Coral.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = CoralSyncClient('https://storage.spacetimeanalytics.com', 'apikey', 'atlantisclientid')
            file_uri = client.upsert_file('spacetimelabs-bucket', '/folder/file.ext', '2020-06-26T14:51Z', 123,
                                          { 'thumb': 's3://bucket/folder/file.ext' })

        :param bucket: Bucket do arquivo
        :type bucket: str
        :param key: Chave do arquivo
        :type key: str
        :param last_modified: Data de última modificação do arquivo (Formato datetime ISO)
        :type last_modified: str
        :param size: Tamanho do arquivo em bytes
        :type size: int
        :param metadata: Dicionário de metadados do arquivo
        :type metadata: dict, optional
        :return: Objeto do arquivo persistido
        :rtype: dict
        """
        response = requests.post(
                '{}/api/sync'.format(self.coral_url),
                headers=self._get_headers(bucket),
                params={
                    'key': key
                }, json={
                    'last_modified': last_modified,
                    'size': size,
                    'metadata': metadata,
                }
            )
        response.raise_for_status()
        return response.json()

    def delete_file(self, bucket, key):
        """Remove um arquivo do banco do Coral.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = CoralSyncClient('https://storage.spacetimeanalytics.com', 'apikey', 'atlantisclientid')
            client.delete_file('spacetimelabs-bucket', '/folder/file.ext')

        :param bucket: Bucket do arquivo
        :type bucket: str
        :param key: Chave do arquivo
        :type key: str
        :return: Código da resposta (204 para successo)
        :rtype: int
        """
        response = requests.delete(
                '{}/api/sync'.format(self.coral_url),
                headers=self._get_headers(bucket),
                params={
                    'key': key
                }
            )
        response.raise_for_status()
        return response.status_code
