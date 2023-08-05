"""
Not finished
"""
import logging
import requests


logger = logging.getLogger(__name__)


class PortalDeTransparenciaSIU:
    
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.errors = []

    def get_fecha_actualizacion(self):
        pass

    def request(self, params={}):
        """ POST al portal 
            Params (ejemplo):
                path: /home/SIU-Wichi/Portal Transparencia/cda/1_presupuesto.cda
                dataAccessId: /home/SIU-Wichi/Portal Transparencia/cda/1_presupuesto.cda
                paramprm_ej_presup: 2020
                ...
            Return:
                data or None
                """
        
        # revisar los iterables y actualizar a lo que corresponda
        try:
            resp = requests.post(self.url,
                                 auth=(self.username, self.password),
                                 data=params) 
        except Exception, e:
            error = 'Request error \n\tURL: {}\n\tParams: {}\n\tError: {}'.format(self.url, params, e)
            logger.error(error)
            self.errors.append(error)
            return None
        
        try:
            data = resp.json()
        except Exception, e:
            error = 'JSON error. Response: {}\n\tURL: {}\n\tParams: {}\n\tError: {}'.format(resp.text, self.url, params, e)
            logger.error(error)
            self.errors.append(error)
            return None
        return data
    