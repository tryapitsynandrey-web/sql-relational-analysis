import subprocess
import sys
import os
import shutil

def main():
    """One-click launch script for the Olist Analytics Dashboard."""

    # Clean welcome message
    print("\n" + "="*60)
    print("🚀 Olist E-Commerce Analytics Pipeline - Web Dashboard")
    print("="*60)
    print("\nInitialising environment...")

    # 1. Resolve project root (the directory this script lives in)
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(project_root, "analysis", ".env")
    env_example = os.path.join(project_root, "analysis", ".env.example")

    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            # Auto-create .env from .env.example so the app can at least start
            shutil.copy(env_example, env_file)
            print("⚠️  No analysis/.env found — created one from .env.example.")
            print("   Edit analysis/.env with your real DB credentials before querying data.\n")
        else:
            # Neither file exists — warn but don't block (system env vars may be set)
            print("⚠️  Warning: analysis/.env not found and no .env.example to copy from.")
            print("   The dashboard will start, but DB queries may fail.")
            print("   Set DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME as env vars.\n")
    else:
        print("✅ Environment file verified.")

    # 2. Launch Streamlit from the project root so imports resolve correctly
    print("📊 Launching Streamlit web application...\n")
    try:
        cmd = [sys.executable, "-m", "streamlit", "run",
               os.path.join(project_root, "src", "main.py"),
               "--server.headless", "false"]
        subprocess.run(cmd, cwd=project_root, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Have a productive day!")
    except FileNotFoundError:
        print("\n❌ Streamlit is not installed in this Python environment.")
        print(f"   Run: {sys.executable} -m pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Failed to launch: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

