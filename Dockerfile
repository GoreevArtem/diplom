FROM arm32v7/python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Установка Rust и Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"


RUN pip install --upgrade pip

RUN pip install -r /code/requirements.txt

COPY . /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]