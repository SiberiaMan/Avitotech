import validators
import aiohttp
from typing import List
from typing import Optional


def check_url(url: str) -> Optional[bool]:
    """
    This function checks is valid URL or not
    :param url: URL
    :return: True if is valid, else False
    """
    if validators.url(url):
        return True
    return False


async def get_formatted_matrix(resp: aiohttp.client.ClientResponse) -> List[List[int]]:
    """
    This function creates and returns a formatted matrix from the server's response
    :param resp: received response from server
    :return: formatted [int] matrix
    """
    chunk_size = 1024
    with open('.matrix.txt', 'wb') as fd:
        while True:
            chunk = await resp.content.read(chunk_size)
            if not chunk:
                break
            fd.write(chunk)
    with open('.matrix.txt', 'r') as fd:
        matrix = fd.readlines()
    matrix = matrix[1::2]
    new_matrix = []
    for line in matrix:
        line = list(map(int, line.strip().replace('|', '').split()))
        new_matrix.append(line)
    return new_matrix


def traverse_matrix_counterclockwise(matrix: List[List[int]]) -> List[int]:
    """
    This function traverses the matrix counterclockwise and returns a list
    :param matrix: formatted matrix
    :return: a list obtained by traversing the matrix counterclockwise
    """
    matrix = list(zip(*matrix[:]))[:]  # rows -> columns, columns -> rows
    lst = []
    while matrix:
        lst += matrix[0]
        matrix = list(zip(*matrix[1:]))[::-1]
    return lst
