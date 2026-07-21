import sys
import os
import time
import argparse

STALE_SECONDS = 600  # 10 minutes — if lock is older than this, it's a crashed tick


def acquire(lock_file):
    if os.path.exists(lock_file):
        age = time.time() - os.path.getmtime(lock_file)
        if age < STALE_SECONDS:
            print(f"LOCKED — previous tick still running ({int(age)}s old). Skipping.")
            sys.exit(1)
        else:
            print(f"STALE LOCK detected ({int(age)}s old) — clearing and acquiring.")
            os.remove(lock_file)

    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))
    print("LOCK ACQUIRED")
    sys.exit(0)


def release(lock_file):
    if os.path.exists(lock_file):
        os.remove(lock_file)
        print("LOCK RELEASED")
    else:
        print("LOCK RELEASE — file not found (already cleared)")
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tick lock manager")
    parser.add_argument("command", choices=["acquire", "release"])
    parser.add_argument(
        "--lock-file", default="tick.lock", help="Lock file name (default: tick.lock)"
    )
    args = parser.parse_args()

    if args.command == "acquire":
        acquire(args.lock_file)
    else:
        release(args.lock_file)
