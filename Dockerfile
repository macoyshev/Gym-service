FROM python:3.9

WORKDIR /app

COPY . .

ENV DB_URI='sqlite+aiosqlite:///app/db/primary.db' \
    DB_URI_SYNC='sqlite:///app/db/primary.db' \
    SECRET_KEY='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7' \
    ALGORITHM='HS256' \
    ADMIN_KEY='key'

# dependencies
RUN python3 -m pip install --upgrade pip \
	&& python3 -m pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

