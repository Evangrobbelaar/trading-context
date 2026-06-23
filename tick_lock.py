import sys
import os
import time

LOCK_FILE = "tick.lock"
STALE_SECONDS = 600  # 10 minutes — if lock is older than this, it's a crashed tick


def acquire():
    if os.path.exists(LOCK_FILE):
        age = time.time() - os.path.getmtime(LOCK_FILE)
        if age < STALE_SECONDS:
            print(f"LOCKED — previous tick still running ({int(age)}s old). Skipping.")
            sys.exit(1)
        else:
            print(f"STALE LOCK detected ({int(age)}s old) — clearing and acquiring.")
            os.remove(LOCK_FILE)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    print("LOCK ACQUIRED")
    sys.exit(0)


def release():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        print("LOCK RELEASED")
    else:
        print("LOCK RELEASE — file not found (already cleared)")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tick_lock.py [acquire|release]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "acquire":
        acquire()
    elif cmd == "release":
        release()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
