from datetime import datetime
from enum import IntEnum
from typing import Literal, Optional, Union

import pydantic


class Mode(IntEnum):
    unknown = 0
    no_fix = 1
    two_d_fix = 2
    three_d_fix = 3


class Watch(pydantic.BaseModel):
    class_: Literal["WATCH"] = pydantic.Field("WATCH", alias="class")
    enable: bool = True
    json_: bool = pydantic.Field(True, alias="json")
    split24: bool = False
    raw: int = 0

    class Config:
        extra = pydantic.Extra.allow


class Version(pydantic.BaseModel):
    class_: Literal["VERSION"] = pydantic.Field(alias="class")
    release: str
    rev: str
    proto_major: int
    proto_minor: int

    @property
    def proto(self) -> tuple[int, int]:
        return self.proto_major, self.proto_minor


class Device(pydantic.BaseModel):
    class_: Literal["DEVICE"] = pydantic.Field(alias="class")
    path: str
    driver: str
    subtype: str
    activated: datetime
    flags: int
    native: int
    bps: int
    parity: str
    stopbits: int
    cycle: float
    mincycle: float


class Devices(pydantic.BaseModel):
    class_: Literal["DEVICES"] = pydantic.Field(alias="class")
    devices: list[Device]


class TPV(pydantic.BaseModel):
    class_: Literal["TPV"] = pydantic.Field(alias="class")
    device: str
    mode: Mode
    time: datetime
    ept: float
    lat: float
    lon: float
    altHAE: float
    altMSL: float
    alt: float
    epx: float
    epy: float
    epv: float
    track: Optional[float]
    magtrack: Optional[float]
    magvar: float
    speed: float
    climb: float
    eps: float
    epc: float
    geoidSep: float
    eph: float
    sep: float


class PRN(pydantic.BaseModel):
    PRN: int
    el: float
    az: float
    ss: float
    used: bool
    gnssid: int
    svid: int


class Sky(pydantic.BaseModel):
    class_: Literal["SKY"] = pydantic.Field(alias="class")
    device: str
    xdop: float
    ydop: float
    vdop: float
    tdop: float
    hdop: float
    gdop: float
    nSat: int
    uSat: int
    satellites: list[PRN]


class Poll(pydantic.BaseModel):
    class_: Literal["POLL"] = pydantic.Field(alias="class")
    time: datetime
    active: int
    tpv: list[TPV]
    sky: list[Sky]

GSPD_MESSAGE = Union[Poll, Sky, TPV, Devices, Version, Watch]
GSPD_RUNTIME_MESSAGE = Union[Sky, TPV]

class Response(pydantic.BaseModel):
    message: GSPD_MESSAGE = pydantic.Field(discriminator="class_")
