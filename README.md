# Ghostunnel Demo

## :bookmark: Requirements

- [Openssl](https://github.com/openssl/openssl)

## :books: Ghostunnel

Ghostunnel is a simple TLS proxy with mutual authentication support for securing non-TLS backend applications.

Ghostunnel supports two modes, client mode and server mode. Ghostunnel in server mode runs in front of a backend server and accepts TLS-secured connections, which are then proxied to the (insecure) backend. A backend can be a TCP domain/port or a UNIX domain socket. Ghostunnel in client mode accepts (insecure) connections through a TCP or UNIX domain socket and proxies them to a TLS-secured service. In other words, ghostunnel is a replacement for stunnel.

### Features

- **Access control**: Ghostunnel enforces mutual authentication by requiring a valid client certificate for all connections. Policies can enforce checks on the peer certificate in a connection, either via simple flags or declarative policies using Open Policy Agent. This is useful for restricting access to services that don't have native access control.

- **Certificate hotswapping**: Ghostunnel can reload certificates at runtime without dropping existing connections. Certificates can be loaded from disk, the SPIFFE Workload API, or a PKCS#11 module. This allows short-lived certificates to be used with Ghostunnel as you can pick up new certificates transparently.

- **ACME Support**: In server mode, Ghostunnel can optionally obtain and automatically renew a public TLS certificate via the ACME protocol, such as through Let's Encrypt. Note that this requires a valid FQDN accessible on the public internet for verification.

- **Monitoring and metrics**: Ghostunnel has a built-in status feature that can be used to collect metrics and monitor a running instance. Metrics can be fed into Graphite or Prometheus to see number of open connections, rate of new connections, connection lifetimes, timeouts, and other info.

- **Emphasis on security**: We have put some thought into making Ghostunnel secure by default and prevent accidental misconfiguration. For example, we always negotiate TLS v1.2 (or greater) and only use safe cipher suites. Ghostunnel also supports PKCS#11 which makes it possible to use Hardware Security Modules (HSMs) to protect private keys.

## :triangular_flag_on_post: Starting

```bash
# Clone the repository
git clone https://github.com/arielroque/ghostunnel-demo.git
```

## :tv: Demo

In this demo, we will add TLS communication between two non-tls applications (client and server) using ghostunnel.  

### Generate certs

#### CA

```bash
# Generate CA private key
openssl genpkey -algorithm RSA -out ca-key.pem

# Generate CA certificate
openssl req -x509 -new -key ca-key.pem -out ca.pem -days 365
```

#### Server key and cert

```bash
# Generate server private key
openssl genpkey -algorithm RSA -out server/server-key.pem

# Generate server certificate signing request
openssl req -new -key server/server-key.pem -out server/server-csr.pem

# Generate server certificate signed by CA
openssl x509 -req -in server/server-csr.pem -CA ca.pem -CAkey ca-key.pem -out server/server.pem -days 365 -extfile server/server.conf -extensions v3_req

# Display server certificate information
#openssl x509 -in server/server.pem -text -noout
```

#### Client key and cert

```bash
# Generate client private key
openssl genpkey -algorithm RSA -out client/client-key.pem

# Generate client certificate signing request
openssl req -new -key client/client-key.pem -out client/client-csr.pem

# Generate client certificate signed by CA
openssl x509 -req -in client/client-csr.pem -CA ca.pem -CAkey ca-key.pem -out client/client.pem -days 365

# Display client certificate information
#openssl x509 -in client/client.pem -text -noout
```

### Deploy server

#### Ghostunnel server proxy

```bash
# Deploy ghostunnel server
./server/ghostunnel server --listen localhost:5002 --target localhost:8000 --key server/server-key.pem --cert server/server.pem --cacert ca.pem --allow-all
```

#### Server

```bash
# Deploy server
python3 server/main.py
```

### Deploy client

#### Ghostunnel client proxy

```bash
# Deploy ghostunnel client
./client/ghostunnel client --listen localhost:6000 --target localhost:5002 --key client/client-key.pem --cert client/client.pem --cacert ca.pem
```

#### Client

```bash
# Deploy client
python3 client/main.py

RESPONSE: I am the server running with TLS and I am fine
```
