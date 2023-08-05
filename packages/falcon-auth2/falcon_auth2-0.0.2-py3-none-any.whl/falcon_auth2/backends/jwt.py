# try:
#     import jwt
# except ImportError:
#     jwt = None


# class CustomJWTAuthBackend(AuthBackend):
#     """
#     Token based authentication using the `JSON Web Token standard https://jwt.io/introduction/`
#     Clients should authenticate by passing the token key in the `Authorization`
#     HTTP header, or in the param argument `token`

#     NOTE: Custom implementation taken form falcon_auth.JWTAuthBackend
#     """

#     def __init__(self):
#         self.secret_key = getSecretKey()
#         self.algorithm = JWT.ALGORITHM
#         self.leeway = timedelta(seconds=JWT.LEEWAY)
#         self.auth_header_prefix = JWT.TOKEN_PREFIX
#         self.expiration_delta = timedelta(seconds=JWT.EXPIRE_IN)
#         self.issuer = JWT.ISSUER
#         self.audience = JWT.AUDIENCE
#         self.options = jwt.PyJWT._get_default_options()
#         for key in self.options:
#             self.options[key] = True

#     def _decode_jwt_token(self, req: falcon.Request):
#         """Decodes the jwt token into a payload"""
#         print("cookie 4200\n", req.get_cookie_values("open_id_token_4200"))
#         print("cookie 5555\n", req.get_cookie_values("open_id_token_5555"))
#         try:
#             auth_header = req.auth
#             token = self.parse_auth_token_from_request(auth_header=auth_header)
#         except falcon.HTTPError:
#             # check if the token was passed as a param instead else raise the original exception
#             token = req.get_param("token")
#             if not token:
#                 raise

#         try:
#             payload = jwt.decode(
#                 jwt=token,
#                 key=self.secret_key,
#                 options=self.options,
#                 algorithms=[self.algorithm],
#                 issuer=self.issuer,
#                 audience=self.audience,
#                 leeway=self.leeway,
#             )
#         except jwt.InvalidTokenError as ex:
#             raise falcon.HTTPUnauthorized(description=str(ex))

#         return payload

#     def authenticate(self, req, resp, resource):
#         """Extract auth token from request `authorization` header or token query, decode jwt token,
#         verify configured claims and return either an user object if successful else raise an
#         falcon.HTTPUnauthoried exception
#         """
#         with resp.context.timeLogger("auth"):
#             payload = self._decode_jwt_token(req)
#             user = getUserFromToken(payload, session=getSessionFromRequest(req))
#         if not user:
#             raise falcon.HTTPUnauthorized(description="Invalid JWT Credentials")

#         return user

#     def get_auth_token(self, user_payload):
#         """Create a JWT authentication token from user_payload

#         Parameters
#         - user_payload: dict
#             A `dict` containing required information to create authentication token
#         """
#         now = datetime.utcnow()
#         payload = {
#             "user": user_payload,
#             "iat": now,
#             "nbf": now,
#             "exp": now + self.expiration_delta,
#         }

#         if self.issuer is not None:
#             payload["iss"] = self.issuer

#         if self.audience is not None:
#             payload["aud"] = self.audience

#         return jwt.encode(payload, self.secret_key, algorithm=self.algorithm).decode("utf-8")


# class JWTAuthBackend(AuthBackend):
#     """
#     Token based authentication using the `JSON Web Token standard <https://jwt.io/introduction/>`__
#     Clients should authenticate by passing the token key in the `Authorization`
#     HTTP header, prepended with the string specified in the setting
#     `auth_header_prefix`. For example:
#         Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
#     Args:
#         user_loader(function, required): A callback function that is called with the
#             decoded `jwt payload` extracted from the `Authorization`
#             header. Returns an `authenticated user` if user exists matching the
#             credentials or return `None` to indicate if no user found or credentials
#             mismatch.
#         secrey_key(string, required): A secure key that was used to encode and
#             create the `jwt token` from a dictionary payload
#         algorithm(string, optional): Specifies the algorithm that was used
#             to for cryptographic signing. Default is ``HS256`` which stands for
#             HMAC using SHA-256 hash algorithm. Other supported algorithms can be
#             found `here <http://pyjwt.readthedocs.io/en/latest/algorithms.html>`__
#         auth_header_prefix(string, optional): A prefix that is used with the
#             bases64 encoded credentials in the `Authorization` header. Default is
#             ``jwt``
#         leeway(int, optional): Specifies the timedelta in seconds that is allowed
#             as leeway while validating `expiration time` / `nbf(not before) claim`
#             /`iat (issued at) claim` which is in past but not very
#             far. For example, if you have a JWT payload with an expiration time
#             set to 30 seconds after creation but you know that sometimes you will
#             process it after 30 seconds, you can set a leeway of 10 seconds in
#             order to have some margin. Default is ``0 seconds``
#         expiration_delta(int, optional): Specifies the timedelta in seconds that
#             will be added to current time to set the expiration for the token.
#             Default is ``1 day(24 * 60 * 60 seconds)``
#         audience(string, optional): Specifies the string that will be specified
#             as value of ``aud`` field in the jwt payload. It will also be checked
#             agains the ``aud`` field while decoding.
#         issuer(string, optional): Specifies the string that will be specified
#             as value of ``iss`` field in the jwt payload. It will also be checked
#             agains the ``iss`` field while decoding.
#     """

#     def __init__(
#         self,
#         user_loader,
#         secret_key,
#         algorithm="HS256",
#         auth_header_prefix="jwt",
#         leeway=0,
#         expiration_delta=24 * 60 * 60,
#         audience=None,
#         issuer=None,
#         verify_claims=None,
#         required_claims=None,
#     ):

#         try:
#             jwt
#         except NameError:
#             raise ImportError(
#                 "Optional dependency falcon-authentication[backend-jwt] not installed"
#             )

#         super(JWTAuthBackend, self).__init__(user_loader)
#         self.secret_key = secret_key
#         self.algorithm = algorithm
#         self.leeway = timedelta(seconds=leeway)
#         self.auth_header_prefix = auth_header_prefix
#         self.expiration_delta = timedelta(seconds=expiration_delta)
#         self.audience = audience
#         self.issuer = issuer
#         self.verify_claims = verify_claims or ["signature", "exp", "nbf", "iat"]
#         self.required_claims = required_claims or ["exp", "iat", "nbf"]

#         if "aud" in self.verify_claims and not audience:
#             raise ValueError(
#                 "Audience parameter must be provided if " "`aud` claim needs to be verified"
#             )

#         if "iss" in self.verify_claims and not issuer:
#             raise ValueError(
#                 "Issuer parameter must be provided if " "`iss` claim needs to be verified"
#             )

#     def _decode_jwt_token(self, req):

#         # Decodes the jwt token into a payload
#         token = self.parse_auth_token_from_request(auth_header=req.get_header("Authorization"))

#         options = dict(("verify_" + claim, True) for claim in self.verify_claims)

#         options.update(dict(("require_" + claim, True) for claim in self.required_claims))

#         try:
#             payload = jwt.decode(
#                 jwt=token,
#                 key=self.secret_key,
#                 options=options,
#                 algorithms=[self.algorithm],
#                 issuer=self.issuer,
#                 audience=self.audience,
#                 leeway=self.leeway,
#             )
#         except jwt.InvalidTokenError as ex:
#             raise BackendAuthenticationFailure(backend=self, description=str(ex))

#         return payload

#     def authenticate(self, req, resp, resource):
#         """
#         Extract auth token from request `authorization` header, decode jwt token,
#         verify configured claims and return either a ``user`` object if successful
#         else raise an `BackendAuthenticationFailure` exception.
#         """
#         payload = self._decode_jwt_token(req)
#         return {
#             "user": self.load_user(req, resp, resource, payload),
#         }

#     def get_auth_token(self, user_payload):
#         """
#         Create a JWT authentication token from ``user_payload``
#         Args:
#             user_payload(dict, required): A `dict` containing required information
#                 to create authentication token
#         """
#         now = datetime.utcnow()
#         payload = {"user": user_payload}
#         if "iat" in self.verify_claims:
#             payload["iat"] = now

#         if "nbf" in self.verify_claims:
#             payload["nbf"] = now + self.leeway

#         if "exp" in self.verify_claims:
#             payload["exp"] = now + self.expiration_delta

#         if self.audience is not None:
#             payload["aud"] = self.audience

#         if self.issuer is not None:
#             payload["iss"] = self.issuer

#         return jwt.encode(
#             payload, self.secret_key, algorithm=self.algorithm, json_encoder=ExtendedJSONEncoder
#         ).decode("utf-8")
