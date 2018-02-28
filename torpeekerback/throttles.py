from rest_framework.throttling import AnonRateThrottle

class HighLoadAnonRateThrottle(AnonRateThrottle):
    scope = "high_load_anon"

class MediumLoadAnonRateThrottle(AnonRateThrottle):
    scope = "medium_load_anon"
