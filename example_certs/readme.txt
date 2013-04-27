## Generate public/private key
openssl genrsa -des3 -out server.key 1024

## Create CSR
openssl req -new -key server.key -out server.csr

## Remove passphrase from key
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key

## generate self signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

