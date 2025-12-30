import socket
import time
import subprocess
import sys
import os

def wait_for_service(host, port, timeout=60):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, int(port)), timeout=1):
                print(f"Service {host}:{port} is reachable!")
                return True
        except (socket.timeout, ConnectionRefusedError):
            pass
        except Exception as e:
            print(f"Error checking {host}:{port}: {e}")

        if time.time() - start_time > timeout:
            print(f"Timeout waiting for {host}:{port}")
            return False
            
        print(f"Waiting for {host}:{port}...")
        time.sleep(2)

def main():
    # 1. Wait for Postgres
    pg_host = os.getenv("POSTGRES_HOST", "postgres")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    if not wait_for_service(pg_host, pg_port):
        sys.exit(1)

    # 2. Wait for ChromaDB
    chroma_host = os.getenv("CHROMADB_HOST", "chromadb")
    chroma_port = os.getenv("CHROMADB_PORT", "8000")
    if not wait_for_service(chroma_host, chroma_port):
        sys.exit(1)

    # 3. Run Ingestion (Optional check if needed, or always run on startup)
    print("Running ingestion pipeline...")
    # We call the script as a subprocess
    result = subprocess.run(["python", "scripts/run_ingestion.py"], capture_output=False)
    
    if result.returncode != 0:
        print("Ingestion failed! Check logs.")        
    else:
        print("Ingestion pipeline finished successfully.")

    # 4. Start Streamlit
    print("Starting Streamlit App...")
    # Exec replaces the current process with the new process
    env = os.environ.copy()
    env["PYTHONPATH"] = f"/code:{env.get('PYTHONPATH', '')}"
    os.execvpe("streamlit", ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"], env)

if __name__ == "__main__":
    main()
