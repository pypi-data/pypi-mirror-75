import base64
from pathlib import Path
import textwrap
from os import path
from typing import Tuple, Union

from erdpy import utils, guards


def get_pubkey(pem_file: Union[str, Path]):
    _, pubkey = parse(pem_file)
    return pubkey


def parse(pem_file: Union[str, Path]) -> Tuple[bytes, bytes]:
    pem_file = path.expanduser(pem_file)
    guards.is_file(pem_file)

    lines = utils.read_lines(pem_file)
    lines = [line for line in lines if "-----" not in line]
    key_base64 = "".join(lines)
    key_hex = base64.b64decode(key_base64).decode()
    key_bytes = bytes.fromhex(key_hex)

    seed = key_bytes[:32]
    pubkey = key_bytes[32:]
    return seed, pubkey


def parse_validator_pem(pem_file):
    pem_file = path.expanduser(pem_file)
    guards.is_file(pem_file)

    lines = utils.read_lines(pem_file)

    first_line = lines[0]
    start = first_line.find('for ') + len('for ')
    stop = first_line.rfind('-----')
    bls_key = first_line[start:stop]

    lines = [line for line in lines if "-----" not in line]
    key_base64 = "".join(lines)
    key_hex = base64.b64decode(key_base64).decode()
    key_bytes = bytes.fromhex(key_hex)

    seed = key_bytes
    return seed, bls_key


def write(pem_file: Union[str, Path], seed: bytes, pubkey: bytes, name: str = ""):
    pem_file = path.expanduser(pem_file)

    if not name:
        name = pubkey.hex()

    header = f"-----BEGIN PRIVATE KEY for {name}-----"
    footer = f"-----END PRIVATE KEY for {name}-----"

    seed_hex = seed.hex()
    pubkey_hex = pubkey.hex()
    combined = seed_hex + pubkey_hex
    combined = combined.encode()
    key_base64 = base64.b64encode(combined).decode()

    payload_lines = textwrap.wrap(key_base64, 64)
    payload = "\n".join(payload_lines)
    content = "\n".join([header, payload, footer])
    utils.write_file(pem_file, content)
