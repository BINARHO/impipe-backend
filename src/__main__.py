import logging

import zerorpc

from functools import reduce
from graph import Graph


def main():
    max_just = reduce(lambda x, y: max(x, len(y)), logging.root.manager.loggerDict, 0)
    logging.basicConfig(level=logging.INFO,
                        format='{levelname}\t{name:<%(max_just)s}\t{message}' % {'max_just': max_just},
                        style='{', )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    address = 'tcp://127.0.0.1:1234'
    server = zerorpc.Server(Graph())

    try:
        server.bind(address)
        logger.debug(f'starting server on {address}')
        server.run()

    finally:
        server.close()


if __name__ == '__main__':
    main()
