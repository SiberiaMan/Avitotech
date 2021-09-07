import aiohttp
from matrix_traversal.utils import (
    traverse_matrix_counterclockwise,
    get_formatted_matrix,
    check_url)
from typing import List
from aiohttp import ClientError
from asyncio.exceptions import TimeoutError


async def send_request(url: str) -> List[List[int]]:
    """
    This function sends a request to URL and processes the response, if any
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
                    matrix = await get_formatted_matrix(resp)
                    return matrix
    except TimeoutError:
        print("Timeout error!")
    except ClientError:
        print("Some problems with connection or URL")
    except Exception as e:
        print(e)


async def get_matrix(url: str) -> List[int]:
    """
    This function gets URL address, sends a request to server
    and returns a list obtained by traversing the matrix counterclockwise
    :param url: URL
    :return: list obtained by traversing the matrix
    """
    if check_url(url):
        matrix = await send_request(url)
        if matrix:
            lst = traverse_matrix_counterclockwise(matrix)
            return lst
    else:
        print("Invalid URL address")
