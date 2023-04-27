import os

def main():

    base_dir = 'C:/Program Files/'
    pattern = 'Nuke'
    all_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and pattern in d]
    sorted_dirs = sorted(all_dirs, reverse=True)
    
    if sorted_dirs:
        highest_version_folder = sorted_dirs[0]
        for filename in os.listdir(os.path.join(base_dir, highest_version_folder)):
            if filename.startswith("Nuke") and filename.endswith(".exe"):
                print(os.path.join(os.path.join(base_dir, highest_version_folder), filename))
    else:
        print("No directories found that match the pattern.")

if __name__ == "__main__":
    main()