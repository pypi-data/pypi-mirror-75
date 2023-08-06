from typing import Iterator, Optional, Tuple

from .types import Chunk

def assert_tag(target: str, chunk: Optional[Chunk]) -> bytes:
    """Return chunk data if chunk has target 4CC tag."""
    if not chunk:
        raise ValueError(f'no 4CC header')
    if chunk.tag != target:
        raise ValueError(f'expected tag to be {target} but got {chunk.tag}')
    return chunk.data

def print_chunks(chunks: Iterator[Tuple[int, Chunk]], level: int = 0, base: int = 0) -> Iterator[Tuple[int, Chunk]]:
    indent = '    ' * level
    for offset, chunk in chunks:
        print(f'{indent}{base + offset} {chunk.tag} {len(chunk.data)}')
        yield base + offset, chunk

def drop_offsets(chunks: Iterator[Tuple[int, Chunk]]) -> Iterator[Chunk]:
    """Drop offset from each (offset, chunk) tuple in given iterator"""
    return (chunk for _, chunk in chunks)
