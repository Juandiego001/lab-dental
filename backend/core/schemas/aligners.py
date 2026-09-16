from marshmallow import Schema
from apiflask.fields import Boolean, DateTime, String, String, List, Nested, String
from core.schemas.utils import BaseSchema


class VersionSchema(Schema):
    semantic = String()
    meta = String()


class BoardFeaturesSchema(Schema):
    numCameras = String()
    numAccel = String()
    isDDAligner = Boolean()


class SpecsSchema(Schema):
    month = String()
    year = String()
    name = String()


class SpecsExpirationSchema(Schema):
    month = String()
    year = String()

# --- Sub-esquemas de Geolocation ---


class AsnSchema(Schema):
    asn = String()
    name = String()
    domain = String()
    route = String()
    type = String()


class LanguageSchema(Schema):
    name = String()
    native = String()
    code = String()


class CurrencySchema(Schema):
    name = String()
    code = String()
    symbol = String()
    native = String()


class TimeZoneSchema(Schema):
    name = String()
    abbr = String()
    offset = String()
    is_dst = Boolean()
    current_time = String()


class ThreatSchema(Schema):
    is_tor = Boolean()
    is_icloud_relay = Boolean()
    is_proxy = Boolean()
    is_datacenter = Boolean()
    is_anonymous = Boolean()
    is_known_attacker = Boolean()
    is_known_abuser = Boolean()
    is_threat = Boolean()
    is_bogon = Boolean()
    blocklists = List(String())


class GeolocationSchema(Schema):
    ip = String()
    is_eu = Boolean()
    city = String()
    region = String()
    region_code = String()
    region_type = String()
    country_name = String()
    country_code = String()
    continent_name = String()
    continent_code = String()
    latitude = String()
    longitude = String()
    postal = String()
    calling_code = String()
    flag = String()
    emoji_flag = String()
    emoji_unicode = String()
    asn = Nested(AsnSchema)
    languages = List(Nested(LanguageSchema))
    currency = Nested(CurrencySchema)
    time_zone = Nested(TimeZoneSchema)
    threat = Nested(ThreatSchema)
    count = String()

# --- Sub-esquemas de UpdateState ---


class SoftwareSpecsBoolSchema(Schema):
    """Esquema reutilizable para diccionarios con {software: bool, specs: bool}"""
    software = Boolean()
    specs = Boolean()


class SoftwareSpecsProgressSchema(Schema):
    """Esquema reutilizable para progresos que pueden ser nulos"""
    software = String(allow_none=True)
    specs = String(allow_none=True)


class UpdateStateSchema(Schema):
    state = String()
    error = String(allow_none=True)
    powerLow = Boolean()
    firstInstall = Boolean()
    cloudAvailable = Boolean()
    checkingCloud = Boolean()
    found = Nested(SoftwareSpecsBoolSchema)
    softwareUpdateDownload = String(allow_none=True)
    specsUpdateDownload = String(allow_none=True)
    downloading = Nested(SoftwareSpecsBoolSchema)
    downloadProgress = Nested(SoftwareSpecsProgressSchema)
    downloaded = Nested(SoftwareSpecsBoolSchema)
    readyToInstall = Nested(SoftwareSpecsBoolSchema)
    installing = Nested(SoftwareSpecsBoolSchema)
    installProgress = Nested(SoftwareSpecsProgressSchema)
    installed = Nested(SoftwareSpecsBoolSchema)


class AlignerOut(Schema):
    id = String()
    version = Nested(VersionSchema)
    boardFeatures = Nested(BoardFeaturesSchema)
    specs = Nested(SpecsSchema)
    specsExpiration = Nested(SpecsExpirationSchema)
    geolocation = Nested(GeolocationSchema)

    language = String()
    systemClass = String()
    boardClass = String()
    family = String()
    serialNumber = String()
    address = String()

    # Podrías usar DateTime() si garantizas que los strings vienen en formato ISO-8601 válido
    updatedAt = String()
    createdAt = String()

    openSupportTickets = String()
    closedSupportTickets = String()
    connected = Boolean()
    connectCount = String()
    port = String()
    logLevel = String()
    currentProcedure = String()

    # Se usa String() o Dict() permitiendo nulos ya que el JSON original muestra "null"
    pendingSoftwareDownload = String(allow_none=True)
    updateState = Nested(UpdateStateSchema)
    favorite = Boolean()


class VersionOut(Schema):
    semantic = String()
    path = String()
