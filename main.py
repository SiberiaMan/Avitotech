import asyncio
from matrix_traversal import get_matrix

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'

loop = asyncio.get_event_loop()
lst = loop.run_until_complete(get_matrix(SOURCE_URL))
