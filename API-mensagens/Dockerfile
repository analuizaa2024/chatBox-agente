# imagem do repositório oficial
FROM python:3.12

#cria uma pasta dentro do container
WORKDIR /app

COPY requirements.txt .

# instala todas as bibliotecas python
RUN pip install -r requirements.txt

#copia o projeto inteiro para dentro do container
COPY . .

#roda quando o container inicia
CMD ["python", "main.py"]