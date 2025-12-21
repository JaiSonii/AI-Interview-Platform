from app.main import create_app
import uvicorn

def main():
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=4002)


if __name__ == "__main__":
    main()
