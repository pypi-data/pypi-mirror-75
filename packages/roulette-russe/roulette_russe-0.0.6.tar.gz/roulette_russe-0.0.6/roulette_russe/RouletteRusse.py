import dns.resolver
import random
import boto3
import json


class RouletteRusse(object):
    """
    A class used to represent a Roulette Russe

    ...
    Attributes
    ----------
    proxy_domain : str
        the domain name that binds the proxy IP addresses in A rows
    proxy_username : str, optional
        the ursername of the proxy
    proxy_password : str, optional
        the password of the proxy. If not provided then the proxy is not protected by a username/password mechanism
    proxy_port : int, optional
        the proxy port. If not provided then the default value 3128 will be used
    """
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.client('s3')
        s3.download_file('hubfinanceconfiguration', 'RouletteRusseConfig.json', 'RouletteRusseConfig.json')
        with open('RouletteRusseConfig.json') as config_file:
            rr_config_file = json.load(config_file)
        self.ip_list = dns.resolver.resolve(rr_config_file['proxy_domain_name'], 'A')
        self.proxy_username = rr_config_file['username']
        self.proxy_password = rr_config_file['password']
        self.proxy_port = rr_config_file['proxy_port']
        self.config = rr_config_file

    def getRandomIPAddress(self) -> str:
        return self.ip_list[random.randint(0, len(self.ip_list)-1)]

    def getProxyCredentials(self):
        return {
            'username': self.proxy_username,
            'password': self.proxy_password
        }

    def getProxyConnectionString(self) -> str:
        if self.proxy_username is None or self.proxy_password is None:
            return 'http://' + str(self.getRandomIPAddress()) + ':' + str(self.proxy_port)
        return 'http://' + self.proxy_username + ':' + self.proxy_password + '@' + str(
            self.getRandomIPAddress()) + ':' + str(self.proxy_port)

    def getRandomMobileUserAgent(self):
        mobile_ua_list = self.config["useragents"]["mobile"]
        return mobile_ua_list[random.randint(0, len(mobile_ua_list)-1)]

    def getRandomLaptopUserAgent(self):
        laptop_ua_list = self.config["useragents"]["laptop"]
        return laptop_ua_list[random.randint(0, len(laptop_ua_list)-1)]
