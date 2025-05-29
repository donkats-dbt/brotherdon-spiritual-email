# app_remove.py

from utils.db import remove_marked_subscribers

def run_removal_process():
    removed_count = remove_marked_subscribers()
    print(f"Removed {removed_count} subscribers.")

if __name__ == "__main__":
    run_removal_process()
