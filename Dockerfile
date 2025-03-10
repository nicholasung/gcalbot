FROM alpine:latest
WORKDIR /main
COPY . .
ARG TOKEN
ENV TOKEN=$TOKEN
ARG CAL_ID
ENV CAL_ID=$CAL_ID
ARG INV_LINK
ENV INV_LINK=$INV_LINK
RUN apk add --no-cache python3 py3-pip openssl=3.1.4-r6
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install setuptools==65.5.1 requests python-dotenv discord.py gcsa

CMD ["python3", "main.py"]