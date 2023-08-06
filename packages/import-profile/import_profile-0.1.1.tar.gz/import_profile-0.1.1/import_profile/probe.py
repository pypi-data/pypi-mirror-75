import importlib
import json
import psutil
import time
import sys


class ImportSpy(importlib.abc.Loader):
    def __init__(self, before_import_callback, after_import_callback):
        self._active = set()
        self.before_import_callback = before_import_callback
        self.after_import_callback = after_import_callback

    def find_module(self, fullname, path=None):
        if fullname in self._active:
            return None
        else:
            return self

    def load_module(self, fullname):
        self._active.add(fullname)

        self.before_import_callback(fullname)
        module = importlib.import_module(fullname)
        self.after_import_callback(fullname)

        return module


def psutil_to_json(process):
    cpu_times = process.cpu_times()
    memory_info = process.memory_full_info()

    r = {}
    for k in ("user", "system", "children_user", "children_system"):
        value = getattr(cpu_times, k, None)
        if value is not None:
            r["cpu." + k] = value

    for k in ("rss", "vms", "shared", "uss"):
        value = getattr(memory_info, k, None)
        if value is not None:
            r["memory." + k] = value

    return r


def main():
    config = json.loads(sys.stdin.readline())
    log = []
    process = psutil.Process()

    def before_import_callback(fullname):
        log.append([time.time(), "begin_import", fullname])

    def after_import_callback(fullname):
        log.append([time.time(), "end_import", fullname])

    def log_status():
        log.append([time.time(), "process", psutil_to_json(process)])
        log.append(
            [time.time(), "sys_modules", list(sorted(sys.modules.keys()))]
        )

    sys.meta_path.insert(
        0, ImportSpy(before_import_callback, after_import_callback)
    )

    log_status()
    for m in config["modules"]:
        log.append([time.time(), "begin_manual_import", m])
        importlib.import_module(m)
        log_status()
        log.append([time.time(), "end_manual_import", m])

    print(json.dumps(log))
    sys.stdout.flush()

    sys.stdin.readline()


if __name__ == "__main__":
    main()
