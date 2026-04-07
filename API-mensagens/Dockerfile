# imagem do repositório oficial
FROM python:3.11

#cria uma pasta dentro do container
WORKDIR /app

# instala todas as bibliotecas python
RUN pip install -re rquirements.txt

#copia o projeto inteiro para dentro do container
COPY . .

#roda quando o container inicia
CMD ["python", "main.py"]