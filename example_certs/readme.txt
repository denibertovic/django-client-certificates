################### SERVER ###########################################################

## Generate public/private key
openssl genrsa -des3 -out server.key 1024

## Create CSR
openssl req -new -key server.key -out server.csr

## Remove passphrase from key
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key

## generate self signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt


######################################################################################


######################### CLIENT CERTS ###############################################


## generate request
openssl req -key client.key -new -out client.req

# create client.cnf file
[ ssl_client ]
basicConstraints = CA:FALSE
nsCertType = client
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth


#Create a certificate request into a self signed certificate using extensions for the client certifiacte:
openssl x509 -req -days 365 -in client.req -signkey client.key -out client.crt -extfile client.cnf -extensions ssl_client

# export crt and key into pkcs12
openssl pkcs12 -export -in input.crt -inkey input.key -certfile root.crt -out bundle.p12


## Check a Certificate Signing Request (CSR)
openssl req -text -noout -verify -in CSR.csr
## Check a private key
openssl rsa -in privateKey.key -check
## Check a certificate
openssl x509 -in certificate.crt -text -noout
## Check a PKCS#12 file (.pfx or .p12)
openssl pkcs12 -info -in keyStore.p12

