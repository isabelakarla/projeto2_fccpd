FROM alpine

RUN apk add --no-cache curl

CMD ["sh", "-c", "while true; do echo 'Realizando requisição...'; curl -s http://server:8080; echo ''; sleep 3; done"]
