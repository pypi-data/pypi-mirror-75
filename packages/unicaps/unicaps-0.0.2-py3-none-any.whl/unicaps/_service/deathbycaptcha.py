# -*- coding: UTF-8 -*-
"""
deathbycaptcha.com service
"""

import json
from typing import Dict

from .base import SocketService
from .._transport.socket_transport import StandardSocketTransport, SocketRequestJSON  # type: ignore
from .. import exceptions
from .._captcha import CaptchaType


class DBCSocketTransport(StandardSocketTransport):
    """ DeathByCaptcha Socket Transport """

    SOCKET_HOST = 'api.dbcapi.me'
    SOCKET_PORTS = tuple(range(8123, 8131))

    def _log_in(self, authtoken):
        return self._make_request(
            dict(authtoken=authtoken,
                 cmd="login")
        )

    def _make_request(self, request: Dict) -> Dict:
        """ Make a request """

        # connect
        if not self._socket:
            self.connect()

        # log in
        if request.get('cmd') != 'login':
            self._log_in(request.pop('authtoken'))
        else:
            if ':' in request['authtoken']:
                request['username'], request['password'] = request['authtoken'].split(':',
                                                                                      maxsplit=1)
                del request['authtoken']

        return self._sendrecv(json.dumps(request))


class Service(SocketService):
    """ Main service class for deathbycaptcha.com """

    def _init_transport(self):  # pylint: disable=no-self-use
        return DBCSocketTransport()

    def _post_init(self):
        """ Init settings """

        for captcha_type in self._settings:
            self._settings[captcha_type].polling_delay = 2
            self._settings[captcha_type].polling_interval = 2
            self._settings[captcha_type].solution_timeout = 180


class Request(SocketRequestJSON):
    """ Base Request class """

    def prepare(self) -> Dict:
        """ Prepare request """

        request = super().prepare()
        request.update(
            dict(
                authtoken=self._service.api_key,
                version="Unicaps/Python v1.0"
            )
        )
        return request

    def parse_response(self, response) -> Dict:
        """ Parse response """

        response = super().parse_response(response)

        error_id = response.get('error')
        if not error_id:
            return response

        if error_id in ('not-logged-in', 'invalid-credentials'):
            raise exceptions.AccessDeniedError('Access denied, check your credentials')
        if error_id == 'banned':
            raise exceptions.AccessDeniedError('Access denied, account is suspended')
        if error_id == 'insufficient-funds':
            raise exceptions.LowBalanceError('CAPTCHA was rejected due to low balance')
        if error_id == 'invalid-captcha':
            raise exceptions.BadInputDataError('CAPTCHA is not valid')
        if error_id == 'service-overload':
            raise exceptions.CaptchaServiceTooBusy(
                'CAPTCHA was rejected due to service overload, try again later')

        raise exceptions.ServiceError(error_id)


class GetBalanceRequest(Request):
    """ GetBalance Request class """

    def prepare(self) -> Dict:
        request = super().prepare()
        request.update(dict(cmd="login"))
        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns balance """

        return {'balance': float(super().parse_response(response)['balance'])}


class GetStatusRequest(Request):
    """ GetStatus Request class """


class ReportGoodRequest(Request):
    """ ReportGood Request class """

    def prepare(self, solved_captcha) -> dict:
        """ Prepare request """

        return super().prepare()


class ReportBadRequest(Request):
    """ ReportBad Request class """

    def prepare(self, solved_captcha) -> dict:
        """ Prepare request """

        return super().prepare()


class TaskRequest(Request):
    """ Common Task Request class """

    def prepare(self) -> Dict:
        request = super().prepare()
        request.update(dict(cmd="upload"))
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return task_id """

        response_data = super().parse_response(response)

        return {"task_id": response_data["captcha"]}


class SolutionRequest(Request):
    """ Common Solution Request class """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepare request """

        self._task = task

        request = super().prepare()
        request.update(
            dict(cmd='captcha',
                 captcha=task.task_id)
        )
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return solution and cost """

        response_data = super().parse_response(response)

        # solution_data = response_data.pop("text")
        solution_class = self._task.captcha.get_solution_class()
        captcha_type = self._task.captcha.get_type()
        args = []
        kwargs = {}
        if captcha_type in (CaptchaType.IMAGE,):
            args.append(response_data.pop('text'))
        elif captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3):
            args.append(response_data.pop('text'))
        elif captcha_type in (CaptchaType.FUNCAPTCHA,):
            args.append(response_data.pop('solved'))
        else:
            kwargs.update(response_data)

        solution = solution_class(*args, **kwargs)

        return dict(
            solution=solution,
            cost=response_data.pop("cost"),
            extra=response_data
        )


class RecaptchaV2TaskRequest(TaskRequest):
    """ reCAPTCHA v2 task request """

    # pylint: disable=arguments-differ
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request.update(
            dict(
                type=4,
                token_params=json.dumps(
                    dict(googlekey=captcha.site_key,
                         pageurl=captcha.page_url)
                )
            )
        )

        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """ reCAPTCHA v2 solution request """


class RecaptchaV3TaskRequest(TaskRequest):
    """ reCAPTCHA v3 task request """

    # pylint: disable=arguments-differ
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()

        # set optional data if any
        token_params = dict(
            googlekey=captcha.site_key,
            pageurl=captcha.page_url
        )
        token_params.update(
            captcha.get_optional_data(
                min_score=('min_score', None),
                action=('action', None),
            )
        )

        request.update(dict(type=5, token_params=json.dumps(token_params)))

        return request


class RecaptchaV3SolutionRequest(SolutionRequest):
    """ reCAPTCHA v3 solution request """
