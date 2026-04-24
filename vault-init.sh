#!/bin/sh

set -e

echo "==> Starting Vault..."

vault server -config=/vault/config.hcl &
VAULT_PID=$!

sleep 3

export VAULT_ADDR=http://127.0.0.1:8200

INIT_FILE=/vault/file/init.txt

if vault status | grep -q "Initialized.*false"; then
  echo "==> Initializing Vault..."

  vault operator init -key-shares=1 -key-threshold=1 > $INIT_FILE
fi

UNSEAL_KEY=$(grep 'Unseal Key 1:' $INIT_FILE | awk '{print $4}')
ROOT_TOKEN=$(grep 'Initial Root Token:' $INIT_FILE | awk '{print $4}')

echo "==> Unsealing Vault..."
vault operator unseal $UNSEAL_KEY

export VAULT_TOKEN=$ROOT_TOKEN

echo "==> Enabling KV v2..."
vault secrets enable -path=secret kv-v2 || true

echo "==> Seeding encryption config..."

vault kv put secret/encryption \
  blind_index_secret="cnbLhdtVO6g7RLhZMe1hE11c+16NmslcejuutnZx/0g=" \
  current_version="k2" \
  key_k1="GUSTOZJ9RkCfDagEYfAvBo9QTgBQ5IE9CzMRTKYgXdI=" \
  key_k2="+dRBLX+vZCdcIlENGZ/p3VhSXBIB1wxA3fFjfdTYc8o=" \
  key_k3="9qk8fj64mvHGw26ENhnbZeYz2y9Iyz0uqYlMFnZXKpM=" \
  key_k4="mXTejivi38KLMdd/E/bGKP9Akarx9q0fx2fDaZSahWM=" || true


echo "==> Seeding private keys..."

vault kv put secret/private \
  v1="$(cat <<'EOF'
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCiGuA5mObgTo1p
AACKElYQexjQ6Q0VhqEoOQZ4P9u4BZPNvT3e/abeEpT80fXq1FeiXdRL1PCcdWPB
ixZLwteuDtzZEsvzXa9Ria0364qmpMUa/gqmGPfFwpM7vGmapDfIB91E20hkvd0f
pN568ov2MtytzK532ZXB9LOz39YA8E/tyhJakfmpnTWh/M4jxEgsyycuF2zu79J6
0CqdzeVBlPCf3ebw0q6+EDr2sQmglPHktDso2vFcPW2zUzMHre0MMbbb/+oXNrFt
/qodLHvVOt/k6c51zpGDkZLTLT0yRf8pluiiBNEriWDSVsbY09iljrJy5bXV42jE
gHdEMD0fAgMBAAECggEAFYb1KkufCWr/xicNFfORFgI1jZ9isJj0M4e9z1/yQ/IK
//ehd53+uB9b8BEf6RixhJXqTfcQIZmd7u4TaWniw4d6Fk0JOZ9CMNVUOV4LHSM6
K7dQibXncuM/3d8hCmYZeZ5rE4GoD6d+bdKIBb11Dx5lBk2YCRbOQkzGmodfVONe
06k0XFWomzufXAamECXjJW1EHynfdQ7ly60r1L2cJ31f3pW3rr+NxnQ/Xex1wCrz
/AJkeRCnBnmddc3hIS/7UsHxm4YLpQ1R6lqhraVvcQ1xVWI0IIT3pSeNQbh4CsQu
F24mgEpbNM9Prrcpq7Nf0BrIMmMIM/PmHSGsj9de4QKBgQDQGq908QWJXwbKcLuY
2tgKy/RLcxGXHLzVN3DzefFwA4aZxMfk3k1rzHTeaaHSOX1ljMPTLhr3bM0gRkEY
LfUFEdurBV/XuDWjoTmSSLeQC56sE8VHlZARr6mbTxJh5g+AqdgNl/whZW4gfZRb
eTeSAJlfU3QZYl7DhOHJhLxAIQKBgQDHafSqH4a23rPu/Ca/QoqTH1Il6owParfR
7u21joZrI/Wj3AZRPiFpu0hKS1KscwnCE0O6eBJq9kS/CtDnjewrqeEfUlQl1LUl
SEVBoTGN3fzyBsx21WMraMM7DH5iCLlxNc4LnT0N8dSpU13nQcrkjB/sQAsKM9Af
EW91LGHVPwKBgCp2B27Y7sREu2H69owNux8Y1lO+uswWdQEcOtOzAexVC9W8LP0p
zqo8IWxwKTB3wnpB6oLgWWg6ru/y5b1FQ0Uxi5ytkAy37Vnhv5l1dN7TQCDkN9CP
V8IEEZs62wlWo7sg7JB5flxiEcJXXTn81bXYoXKt2HaFd8h1CIzRpIeBAoGBAJic
8m4wan0Ru0svFshROJSX59q0wjQaTEwSO0IzrZPZlWiuPvd2QUQV3KFfPApWkCVD
cRYIRrAtgTdkI7TS3OgdvvilnVjGjUvXH4m2v6H/PlJL+bcIYDkcmC1cxmxomOOX
dfVVhSBi74oXD0qpA4od42B/MvO/64ubYF2gdc8pAoGBAKEUXbvIt7A+bqLCbe5Y
wVJjcLf5TNhFtp8y4tEJjcOl+RxdGM7q9pCRzuh3Ysylbgcpcz5dbT7k8AsEVp/V
YjVYFyhH669olI+j/ZvdaipXSsNpX6LBu7nDlr6WKAscajxJ9IVxdXtgDSfJn4wB
0BwK4hqBWZ9pAW9kmi92oAFb
-----END PRIVATE KEY-----
EOF
)" \
  v2="$(cat <<'EOF'
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC6CCzE3/TtfHUl
Byja4hSibDE1gRYsPTVgGlpFVAX6Fs9+7wL2ZdjK8WhpdfhjCL8HxFRB2ffTl/8/
gAS7vjtoSwgPLfHSv1yFS1l1z2kY7S1lBvxYD9ZCYBTq/OSRzHR9CyX/Cpq9U3kA
sUiYLLArdTcEXd5BNUn38b6yQql+zgknwZDrZLg1J3jq82ES052NNZ1D6YCFolLF
RyQowIra/OOb+QZnKf11UqoCQgKY+RKiBvisiZE4OeHC2O4cyoEvtYelqXrNRJGF
37hOrUZ2ApucCGd1blQbB+NSGJnso0M04d3+DCjD5Kn6dFfIwjBxWwSABkPDFEzB
18wdMwbRAgMBAAECggEAOB4GLz9luYwNJGXT/68qTVK4x2yQvTiblMluSLKPeQEP
h7le2eggLRwEhKenDWzSf2vMhO7VEPmtcEDUbLP2ZMAZhsazx4CdTsJLkrvF9tR5
GJwyW/gvCGfGd5pg8tBLpXrK8/QFeK4o9roD7Y+xdvKNbZ5JUL9b+FTu0wRD7/F/
6JFS5yhUCj8E03FjuFEa73jIZgletpnno3dUo4BlYQ7L6TrsGz+eD2Fsouf+bGPY
DTX8xR7AscvRCuU3jGHDCtzcKv4o8dKtkcIpL59gE6p5nkJ6D8EZJ1l29bmEullA
OA1BDZdGy+sFPFBPNsrf8O9psp1ikZap8GzccWH1dwKBgQDudfU1m9cPtJEF/SXe
4BLs1rV7CSiIK5N4xz3m9Ot6wf+4NMyPrUO17yaLOzgDEQnh3tB783CwlrZiLpAF
+1HpdqxI9Vi6uuEH8oraCqoam7YLwoJpvmdfDJ5qt7E4IqbpaL3WrBM3I+WOhTul
EPIH/C6DKiFjwDW4CalDTx7HxwKBgQDHtwUw94wdXJuC22LbRf211vzCRYExHyMv
aeWt2Z72ZoOGWF5OuUgTFGgxCBnPt6lqDJ13XfxshVr7dj071v73yP2nqDzB6S0g
R5NSuJL9TLfHJyIpRfB8K1odo4U3t/k/oStFt9b/thPMU8XjybA6iY0mcB8k7WqA
6z5DUPOspwKBgQCc3ppuJtPmsAmLYApOwSeSCHkgtFimo8wC80dkrRBQFFlOa+V6
Syg1Altf0pg5ZDcVEMgkEnS6ppraofj7BmbPZ9NUt5okVRX+bW8sm0Fl+bNbrxyt
xaUpIRsB50+9NwaIm+/uzgpiBspX5IvlPe2KlTpf7RJEFckBBdIExoLgNwKBgH8+
GV2garIOXbpawrpH9qSTbAjutagxWX6M7tv8Ci6dE/FVfgiUPdqCJvwOWDuinZrG
nND/naMat+P86niku1/tu8bFBqjZQnoNgEy08lnWNkT5puc6+0RxboHxvB/K5E/p
BKPvxFi5jhWhzjQaPWCeYML7rqwdY7ztpIbJHeeDAoGBAOtUU9l+aYByx1Y0wjmg
FLYoVBfzkx0g6PwTyD17eYrQKdsPi8KssImIWMpI/bFVyYs4E1efG4Qb5gy+GSlb
xGKKtnPvJLPn9IwdSVc/Zwf++T4qNCmi9X0rmy4z6+TDFMv+EFjQV+jqf4GwEVE8
yKMtlf+ONMQzeKb7oKvtOGVg
-----END PRIVATE KEY-----
EOF
)" \
  v3="$(cat <<'EOF'
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCuAzZQ8d4YxW0/
ZoFdqXKl1kDPwou1ipVfbmD4C2nx3ZO9hCdQ1QMY05RmhK3TlRVU4wKOSskfR16D
h8nPbtsHs7O/Ppfjm4/pei91V+zlTnSvqc5mBzCLZaiH4sb/ja9KWiiUTMfzkQFV
xPmo2CXP6ObmuI49oy6yjKf42QN7A6SmQgNMrCRYLqIyIATCB5SDlnpe/X7hSQc1
TUC/abAS2YjhPN8ocKksN9GFxANVEeZvvWgVFsiJVU+7ni3D90taFaLfjzbf+9gR
mfW2p1w3Vf7b4ZwRXF6CmO8ZTiIGpRyBThV+OexYiVjmH6Pr0djanMqPUtqDcl6m
z4wYIOFLAgMBAAECggEACBZAakBTUyyHY8wMUDO6DyHQMUVPBEjWxgLjM1q5AuEc
uSxMPk+6P2doHQS471jmWFFLWa9CWY5a+Yi9+7AzMj4mlqS1el1M+t3qz9pnXbwx
9uo+d6Gt597VBRcWGHW8EOUY5It6qIzYDVM7S56kh8rA1OyzXUw92Z5o9JQ8uuK7
hdHpUEtiuf+4sbvAC8AJH8TCg4U7H8nbwjzsfVZFOIGNpZTY3iHOzbP+fkSXaEfH
nOS3A4KR9r5uGX8CVcb6nuuj5tWQcW+efiF4V9cEvEhh9SYaB6mc1RFXQIMFD4Kw
ebdKihJdBbRtIvE1oaYOkVbpg9e+5gCPaoFdycauwQKBgQDxLz0WMTqwi1rgIo2p
Fp8PJCePz/qCfdudPfHRxQcqNU4XhCR/D6pmyemFFaGdRR0XTMnOG3mwpV92dapZ
ld/t26/X+5BOGbUhlNWzSNqSUG0Zwq32dMyHFXes7qmQ4Q1hfJQAQjii0Pj9PATO
5bDUW48gutfUvlmEN6fYU4QnHQKBgQC4s6gb5SiTuEG2aU1t9oU3rTpGj4Nvn24s
JLx3DJiti4Qzkt8P1A8Kzm0qVrUV7EpPwJtINYSeQ5pgb5jsFLePVVWDZ/R/3Wvk
4aH/jpwulWemYviK/62HzrA3ilHfB+5gvGnNprMrpi5tGrrqfkc7NIfN0CXgA/dB
00eqYNB1hwKBgBVO1RjG1KaQSUEQDG/p3beavBwKhdlNgT+NH3Ym8BEckH+nXwoS
uj1GjWkCljqsxnsuf43EA6ZFlf+DOb+cbCI5jHmKch9UShpjadXjE9xlWp4yAuiJ
PSCaFu6iTzzLhUEdnn2/W/2WdMj6qnoU9OBuDmEX4MWc44+40w1bo4tJAoGASVLA
/Pn3JtVx+NlK7Ml9z0GMrfBRLGHtWcbnrpcokVSekd7PgLgdlJuoSLONRfu88HY0
7vCYCkAqK/iBi88Zo+Qrg3QkYxJiv8U3C33w0KltMWd+5adkm1JZMGNP5yt93ZdO
pV51KHHbYmLHK0ogOwe6leD4+Dp60P3wKFowx0cCgYAKr/QV4EpXRPdBrLka1B/+
BSyCEO07uB1mPFbguVioyJgvutBNHvISIQBqxgpsT6HheHQMIxHpCatzNU3NHjsI
kYgEu6j+4LHxiGMBEuNBvj8MUS0PvavaHjunlM8BPWfhG52YDrmq9B+np5Ik+S67
PBYdtT3srUjaZJK1rxX0Tw==
-----END PRIVATE KEY-----
EOF
)" || true

echo "==> Creating policy for backend..."

cat <<EOF > /vault/file/backend-policy.hcl
path "secret/data/encryption" {
  capabilities = ["read"]
}

path "secret/data/private" {
  capabilities = ["read"]
}

path "secret/metadata/encryption" {
  capabilities = ["read"]
}

path "secret/metadata/private" {
  capabilities = ["read"]
}
EOF

vault policy write backend-policy /vault/file/backend-policy.hcl

echo "==> Creating backend token..."

BACKEND_TOKEN=$(vault token create -policy=backend-policy -format=json | jq -r ".auth.client_token")

echo $BACKEND_TOKEN > /vault/file/backend_token

echo "==> Backend token ready ✅"

echo "==> Vault is ready 🚀"

wait $VAULT_PID