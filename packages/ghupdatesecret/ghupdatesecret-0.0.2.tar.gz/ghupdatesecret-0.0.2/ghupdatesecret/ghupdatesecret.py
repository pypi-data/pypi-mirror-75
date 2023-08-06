"""A command line utility to update GitHub repository secrets."""
import argparse
import sys
from base64 import b64encode
from typing import NamedTuple
import requests
from nacl import encoding, public


class Repository(NamedTuple):

    """A GitHub repository."""

    owner: str
    name: str


class Authentication(NamedTuple):

    """GitHub API authentication details."""

    username: str
    password: str


class RepositoryKey(NamedTuple):

    """A GitHub repository public key."""

    key_id: str
    key: str


def encrypt_secret(public_key: str, secret: str) -> str:
    """Encrypt a string secret using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"),
                                  encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def get_repository_public_key(repository: Repository,
                              authentication: Authentication) -> RepositoryKey:
    """Get the public key for a repository."""
    request = requests.get(
        "https://api.github.com/repos/{}/{}/actions/secrets/public-key".format(
            repository.owner, repository.name),
        auth=(authentication.username, authentication.password))

    if request.status_code != 200:
        raise RuntimeError("Could not get public key for repository.")

    response = request.json()

    return RepositoryKey(response["key_id"], response["key"])


def update_repository_secret(repository: Repository, name: str, secret: str,
                             authentication: Authentication) -> None:
    """Update the secret for a repository."""
    key_id, key = get_repository_public_key(repository, authentication)

    encrypted_secret = encrypt_secret(key, secret)

    payload = {"encrypted_value": encrypted_secret, "key_id": key_id}

    request = requests.put(
        "https://api.github.com/repos/{}/{}/actions/secrets/{}".format(
            repository.owner, repository.name, name),
        json=payload,
        auth=(authentication.username, authentication.password))

    if not (request.status_code == 201 or request.status_code == 204):
        raise RuntimeError("Received error when pushing updated secret.")


def main():
    """Run the ghupdatesecret CLI."""
    parser = argparse.ArgumentParser(
        description='Update a GitHub repository secret')

    parser.add_argument("repository")
    parser.add_argument("secret_name")

    parser.add_argument('--user', '-u', required=True)
    parser.add_argument('--password', '-p', required=True)

    args = parser.parse_args()

    secret_value = sys.stdin.read()

    repository_parts = args.repository.split("/")

    update_repository_secret(
        Repository(repository_parts[0], repository_parts[1]), args.secret_name,
        secret_value, Authentication(args.user, args.password))


if __name__ == "__main__":
    main()
