import aiohttp
import validators
from typing import List, Optional
from aiohttp import ClientError
from asyncio.exceptions import TimeoutError


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
    with open('matrix.txt', 'wb') as fd:
        while True:
            chunk = await resp.content.read(chunk_size)
            if not chunk:
                break
            fd.write(chunk)
    with open('matrix.txt', 'r') as fd:
        matrix = fd.readlines()
    matrix = matrix[1::2]
    new_matrix = []
    for line in matrix:
        line = list(map(int, line.strip().replace('|', '').split()))
        new_matrix.append(line)
    return new_matrix


async def send_request(url: str) -> List[List[int]]:
    """
    This function send a request to URL and processes the response, if any
    :param url: URL
    :return: formatted matrix if response exists
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if 400 <= resp.status < 500:
                    print(f'Client error - {resp.status}')
                elif resp.status >= 500:
                    print(f'Server error - {resp.status}')
                else:
                    print(resp.status)
                    matrix = await get_formatted_matrix(resp)
                    return matrix
    except TimeoutError:
        print("Timeout error!")
    except ClientError:
        print("Some problems with connection or URL")
    except Exception as e:
        print(e)


def get_answer(matrix: List[List[int]]) -> List[int]:
    """
    This function traverses the matrix counterclockwise and returns a list
    :param matrix: formatted matrix
    :return: a list obtained by traversing the matrix counterclockwise
    """
    matrix = list(zip(*matrix[:]))[:]  # rows -> columns, columns -> rows
    print(matrix)
    lst = []
    while matrix:
        lst += matrix[0]
        matrix = list(zip(*matrix[1:]))[::-1]
    return lst


async def get_matrix(url: str) -> List[int]:
    if check_url(url):
        matrix = await send_request(url)
        if matrix:
            lst = get_answer(matrix)
            return lst
    else:
        print("Invalid URL address")
