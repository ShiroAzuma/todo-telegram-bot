from setuptools import setup, find_packages

setup(
    name="todo-telegram-bot",
    version="1.0.0",
    description="Telegram bot for task management",
    author="ShiroAzuma",
    py_modules=["bot"],
    install_requires=[
        "aiogram>=3.0.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.9",
)
