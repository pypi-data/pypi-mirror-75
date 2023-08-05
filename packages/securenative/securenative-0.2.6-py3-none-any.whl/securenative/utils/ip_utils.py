import ipaddress
import re
import socket


class IpUtils(object):
    VALID_IPV4_PATTERN = re.compile("(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.){3}([01]?\\d\\d?|2[0-4]\\d|25[0-5])")
    VALID_IPV6_PATTERN = re.compile("([0-9a-f]{1,4}:){7}([0-9a-f]){1,4}")

    @staticmethod
    def is_ip_address(ip_address):
        if IpUtils.VALID_IPV4_PATTERN.match(ip_address):
            return True
        if IpUtils.VALID_IPV6_PATTERN.match(ip_address):
            return True
        return False

    @staticmethod
    def is_valid_public_ip(ip_address):
        try:
            socket.inet_aton(ip_address)
        except socket.error:
            return False

        ip = ipaddress.IPv4Address(ip_address)
        if ip.is_loopback \
                or not ip.is_global \
                or ip.is_private \
                or ip.is_link_local \
                or ip.is_multicast \
                or ip.is_reserved \
                or ip.is_unspecified:
            return False
        return True

    @staticmethod
    def is_loop_back(ip_address):
        return ipaddress.IPv4Address(ip_address).is_loopback
