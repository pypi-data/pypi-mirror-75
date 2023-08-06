import time
import zlib
import logging
import hashlib
import binascii
from typing import BinaryIO, Union, Dict, Optional, Iterable


__all__ = ['get_hashes_of_stream']


LOGGER_NAME = "easyhash"
SUPPORTED_ALGORITHMS = [
    "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224",
    "sha3_256", "sha3_384", "sha3_512", "blake2b", "blake2s", "crc32",
    "adler32", "shake_128", "shake_256"]


def _better_hex(i, l):
    a = "{0:#0{1}x}".format(i, l)[2:]
    if len(a) % 2 == 1:
        a = "0" + a
    return a


def get_hashes_of_stream(
        stream: BinaryIO,
        algorithms: Iterable[str] = None,
        length: Optional[int] = None,
        binary: bool = False,
        chunk_size: int = 1024 * 1024 * 64,
        hash_lengths: Dict[str, int] = None) -> Dict[str, Union[str, bytes]]:
    """Get hashes from a stream.

    Arguments:
        stream: File-like object containing the data to hash.
        algorithms: List of hashing algorithms to use, if not specified
            then all the algorthms in `SUPPORTED_ALGORITHMS` are used.
        length: Number of bytes to read from the stream, if not
            specified then all the remaining bytes in the stream will
            be read.
        binary: If `True` then the hash digest will be in binary
            format, if `False` then they'll be in hexadecimal format.
        chunk_size: Maximum number of bytes to read from the file at a
            time.
        hash_lengths: Some hashing algorithms need a user-specified
            length, this is where they should be set.

    Returns:
        Dictionary mapping of hash algorithms to hash digests.

    >>> from io import BytesIO
    >>> get_hashes_of_stream(BytesIO(b"test"), ["md5"])["md5"]
    '098f6bcd4621d373cade4e832627b4f6'
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.debug("hashing %r", stream)
    # track when the hashing started
    hashing_started_at = time.perf_counter()
    # default set of hash algorithms to use
    if algorithms is None:
        algorithms = SUPPORTED_ALGORITHMS
    # default digest lengths
    if hash_lengths is None:
        hash_lengths = {
            "shake_128": 256 // 8,
            "shake_256": 512 // 8,
        }
    # dictionary containing hash objects mapped to their algorithm names
    hashes = {}
    for algo in algorithms:
        if algo == "crc32" or algo == "adler32":
            continue
        hashes[algo] = hashlib.new(algo)
    # crc32 and adler32 use different API
    if "crc32" in algorithms:
        crc32_value = 0
    if "adler32" in algorithms:
        adler32_value = 1
    # process each chunk
    length_read = 0
    while True:
        if length:
            amount_to_read = min(chunk_size, length - length_read)
        else:
            amount_to_read = chunk_size
        if not amount_to_read:
            break
        chunk = stream.read(amount_to_read)
        if not chunk:
            break
        length_read += len(chunk)
        for hash_obj in hashes.values():
            hash_obj.update(chunk)
        # crc32 and adler32 use different API
        if "crc32" in algorithms:
            crc32_value = zlib.crc32(chunk, crc32_value)
        if "adler32" in algorithms:
            adler32_value = zlib.adler32(chunk, adler32_value)
    # get hash digests
    hash_digests: Dict[str, Union[str, bytes]] = {}
    for algo, hash_obj in hashes.items():
        if algo.startswith('shake_'):
            if algo == "shake_128":
                hash_length = hash_lengths[algo]
            elif algo == "shake_256":
                hash_length = hash_lengths[algo]
            else:
                message = "unsupported shake algorithm: %s" % algo
                raise ValueError(message)
            hash_digests[algo] = hash_obj.hexdigest(  # type: ignore
                hash_length)
        else:
            hash_digests[algo] = hash_obj.hexdigest()
    # crc32 and adler32 use different API
    if "crc32" in algorithms:
        hash_digests["crc32"] = _better_hex(crc32_value & 0xffffffff, 10)
    if "adler32" in algorithms:
        hash_digests["adler32"] = _better_hex(adler32_value & 0xffffffff, 10)
    # convert hashes to binary if requested
    if binary:
        for algo, hash_digest in hash_digests.items():
            hash_digests[algo] = binascii.unhexlify(hash_digest)
    # track when the hashing finished
    hashing_finished_at = time.perf_counter()
    # determine time taken to hash
    hashing_duration = hashing_finished_at - hashing_started_at
    # log duration
    logger.debug("%r hashed in %dms", stream, hashing_duration * 1000)
    # all done
    return hash_digests
