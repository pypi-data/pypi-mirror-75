import asyncio
import functools
import io
import logging
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from .config import settings
from .db import get_DB_client
from .save import get_save_client
from .utils import progress_bar

logger = logging.getLogger(__name__)


class Collect:
    def __init__(self, save):
        self.sh = get_save_client(save)
        self.db = get_DB_client(settings.dbm)

    async def run(self, classes):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(10)
        with progress_bar as p:
            class_task = p.add_task("[red]CLASSES", total=len(classes))
            for cdclass in classes:
                doc_task = p.add_task(f"[green]DOCUMENTS FOR CLASS {cdclass}")
                logger.info(f"Getting documents for class {cdclass}")
                await asyncio.gather(
                    *[
                        loop.run_in_executor(
                            executor,
                            functools.partial(
                                self.parallel_docs, p, doc_task, doc, cdclass
                            ),
                        )
                        for doc in self.get_keys(cdclass)
                    ]
                )
                p.stop_task(doc_task)
                logger.info(f"Finished class {cdclass}")
                p.advance(class_task)

    def parallel_docs(self, progress, task, doc, cdclass):
        logger.info(f"Getting key {doc} in class {cdclass}")
        self.get_objects(doc, cdclass)
        progress.advance(task)

    def get_objects(self, key, cdclass):
        if self.sh.check_obj(cdclass, key):
            logger.info(f"Object {key} already exists")
            return True
        for key, part, obj in self.db.get_objects(key):
            try:
                if isinstance(obj, bytes):
                    obj = io.BytesIO(obj)
                self.sh.save_obj(obj.read(), cdclass, key, part)
            except AttributeError:
                logger.error(f"The key {key} has a empty file, it will be ignored")

    def get_keys(self, cdclass):
        exists, docs = self.sh.check_meta(f"DOCS_LIST_{cdclass}")
        if exists:
            logger.info("List of keys for class {cdclass} already exists")
            yield from [doc[0] for _, doc in docs.iterrows()]
        else:
            docs = self.db.get_keys(cdclass)
            docs = [doc[0] for doc in docs]
            self.sh.save_meta(pd.DataFrame(docs), f"DOCS_LIST_{cdclass}")
            yield from docs
