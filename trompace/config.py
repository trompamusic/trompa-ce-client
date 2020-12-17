import configparser
import datetime
import logging
import os

from typing import List, Dict

import requests

import trompace
import jwt


class TrompaConfig:
    config: configparser.ConfigParser = None
    host: str = None
    websocket_host: str = None

    # JWT identifier
    jwt_id: str = None
    # JWT key
    jwt_key: str = None
    # Allowed CE scopes
    jwt_scopes: List[str] = []

    # path to store a cache file containing the jwt token
    jwt_key_cache: str = None
    # jwt token
    jwt_token_encoded: str = None
    # decoded jwt token
    jwt_token_decoded: Dict[str, str] = {}

    def load(self, configfile: str = None):
        if configfile is None:
            configfile = os.getenv("TROMPACE_CLIENT_CONFIG")
            if not configfile:
                raise ValueError("called load() without a path and TROMPACE_CLIENT_CONFIG environment variable unset")
            if not os.path.exists(configfile):
                raise ValueError(f"No such config file '{configfile}'")

        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        self._set_logging()
        self._set_server()
        self._set_jwt()

    def _set_logging(self):
        section_logging = self.config["logging"]
        level = section_logging.get("level").upper()
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        trompace.logger.addHandler(ch)
        trompace.logger.setLevel(level)

    def _set_server(self):
        server = self.config["server"]
        if "host" not in server or "secure" not in server:
            raise ValueError("Cannot find 'server.host' or 'server.secure' option")
        host = server.get("host")
        if server.getboolean("secure"):
            self.host = "https://{}".format(host)
            self.websocket_host = "wss://{}/graphql".format(host)
            self.secure = True
        else:
            self.host = "http://{}".format(host)
            self.websocket_host = "ws://{}/graphql".format(host)
            self.secure = False

    def _set_jwt(self):
        server = self.config["server"]
        host = server.get("host")

        auth = self.config["auth"]
        if "id" not in auth or "key" not in auth or "scopes" not in auth:
            raise ValueError("Cannot find 'auth.id' or 'auth.key' or 'auth.scopes' option")

        self.jwt_id = auth.get("id")
        self.jwt_key = auth.get("key")
        self.jwt_scopes = auth.get("scopes").split(",")

        if "token_cache_dir" not in auth:
            cache_dir = os.getcwd()
            trompace.logger.debug(f"No cache directory set for storing jwt token, "
                                  f"using current directory ({cache_dir})")
        else:
            cache_dir = auth.get("token_cache_dir")

        jwt_cache_file = f".trompace-client-jwt-token-cache-{host.replace('/', '-')}"
        self.jwt_key_cache = os.path.join(cache_dir, jwt_cache_file)

        if os.path.exists(self.jwt_key_cache):
            trompace.logger.debug(f"found a cached token, reading from file {jwt_cache_file}")
            with open(self.jwt_key_cache) as fp:
                token = fp.read()
                self._set_jwt_token(token)

    def _set_jwt_token(self, token):
        try:
            decoded = jwt.decode(token, verify=False)
            self.jwt_token_encoded = token
            self.jwt_token_decoded = decoded
        except jwt.DecodeError:
            trompace.logger.warn("Could not decode cached jwt token, ignoring")

    def _save_jwt_token(self, token):
        """Save a JWT token to the cache file"""
        with open(self.jwt_key_cache, "w") as fp:
            fp.write(token)

    @property
    def jwt_token(self):
        """Get the token needed to authenticate to the CE. If no token is available, request one from the CE
        using the id, key and scopes. If the token is going to expire within the next hour, re-request it.
        Once requested, save it to ``self.jwt_key_cache``"""
        if self.jwt_token_encoded is None:
            trompace.logger.debug("no token, getting one")
            # No token, refresh it
            token = get_jwt(self.host, self.jwt_id, self.jwt_key, self.jwt_scopes)
            self._set_jwt_token(token)
            self._save_jwt_token(token)
        elif self.jwt_token_encoded:
            token = jwt.decode(self.jwt_token_encoded, verify=False)
            now = datetime.datetime.now(datetime.timezone.utc).timestamp()
            expired = token.get('exp', 0) < now
            # check if it's expiring
            if expired:
                trompace.logger.debug("token is expiring, renewing")
                # TODO: Duplicate
                token = get_jwt(self.host, self.jwt_id, self.jwt_key, self.jwt_scopes)
                self._set_jwt_token(token)
                self._save_jwt_token(token)
        # Now we have a token, return it
        # TODO: The issuing step could fail
        return self.jwt_token_encoded


def get_jwt(host, jwt_id, jwt_key, jwt_scopes):
    """Request a JWT key from the CE"""
    # TODO: Would be nice to put this in trompace.connection, but issues with circular import
    url = os.path.join(host, "jwt")
    data = {
        "id": jwt_id,
        "apiKey": jwt_key,
        "scopes": jwt_scopes
    }
    r = requests.post(url, json=data)
    j = r.json()
    if j['success']:
        return j['jwt']
    else:
        print("invalid response getting jwt", j)
    return None


config = TrompaConfig()
