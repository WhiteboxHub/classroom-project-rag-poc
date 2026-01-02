
import os

def update_env():
    env_path = '.env'
    if not os.path.exists(env_path):
        print(f"{env_path} not found.")
        return

    with open(env_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    keys_updated = {'POSTGRES_HOST': False, 'CHROMADB_HOST': False}

    for line in lines:
        key = line.split('=')[0].strip()
        if key in keys_updated:
            new_lines.append(f"{key}=localhost\n")
            keys_updated[key] = True
        else:
            new_lines.append(line)

    for key, updated in keys_updated.items():
        if not updated:
            new_lines.append(f"{key}=localhost\n")

    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print("Updated .env for local usage (Host=localhost).")

if __name__ == "__main__":
    update_env()
