"""Generate JWTs using secp256k1.pem.
"""

# Generate a keypair using:
#
# openssl ecparam -name secp256k1 -genkey -noout -out secp256k1.pem
# openssl ec -in secp256k1.pem -pubout > secp256k1.pub

# Use as:
# curl -H "Authorization: Bearer $(python keys.py '{"group": "staff"}' --exp 2h --sub john)" 0:8000/uptime/domains/ -XPOST -H "Content-Type: application/json" -d '{"domain": "john.org"}'


import argparse
from datetime import datetime, timedelta
from pathlib import Path
import json
import jwt
import shortuuid
from pytimeparse import parse as parse_duration


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claims", type=json.loads)
    parser.add_argument("--iss", "--issuer", type=str, default="keys.py")
    parser.add_argument(
        "--exp",
        "--expire",
        type=parse_duration,
        help="Expire in (ex: 1h, 10s, 365 days, ...)",
        default=3600,
    )
    parser.add_argument("--sub", "--subject", type=str, default="admin")
    return parser.parse_args()


def main():
    args = parse_args()
    print(
        jwt.encode(
            {
                "iss": args.iss,
                "sub": args.sub,
                "exp": datetime.now() + timedelta(seconds=args.exp),
                "jti": shortuuid.uuid(),
                **args.claims,
            },
            Path("secp256k1.pem").read_text(),
            algorithm="ES256",
        )
    )


if __name__ == "__main__":
    main()
