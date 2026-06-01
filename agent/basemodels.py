from typing import List,Set
from enum import Enum
from pydantic import BaseModel, Field, RootModel
from typing import Literal, Optional, Union

class ActionCategorizeNode(str, Enum):
    Get = "Get"
    Set = "Set"
    Chat = "Chat"
    Unknown = "Unknown"

class IntentCategorizeNode(BaseModel):
    sub_sentence: str
    reasoning: str
    needs_device_sensors_read_or_write: bool
    action: ActionCategorizeNode
    targets: List[str] = Field(default_factory=list, min_items=0)

class IntentsCategorizeNode(RootModel[List[IntentCategorizeNode]]):
    pass
"""
class RefrigeratorSetSensors(BaseModel):
    isSuperFrz: Optional[bool] = None
    isSuperRef: Optional[bool] = None
    isSleep: Optional[bool] = None
    crushOrcube: Optional[Literal["cube", "crush"]] = None
    isLight: Optional[bool] = None
    refTemp: Optional[int] = None
    frzTemp: Optional[int] = None
    isIceOn: Optional[bool] = None
    isChildLock: Optional[bool] = None
    isMagicZone: Optional[bool] = None
    isMute: Optional[bool] = None
    isVacation: Optional[bool] = None
    enviromentTemp: Optional[int] = None
    isFilterReset: Optional[bool] = None
    isFrzDoorOpen: Optional[bool] = None
    isRefDoorOpen: Optional[bool] = None
    filterTime: Optional[int] = None
    Unknown: Optional[bool] = None

class SetNodeRequest(BaseModel):
    reasoning: str
    isItInAllowedSensorsAndWeHaveValidValue: bool
    refrigerator: RefrigeratorSetSensors = Field(..., min_properties=1, max_properties=1)
    actionType: Literal["Set", "Up", "Down", "Max", "Min"]
"""
class IsSuperFrz(BaseModel):
    isSuperFrz: bool

class IsSuperRef(BaseModel):
    isSuperRef: bool

class IsSleep(BaseModel):
    isSleep: bool

class CrushOrCube(BaseModel):
    crushOrcube: Literal["cube", "crush"]

class IsLight(BaseModel):
    isLight: bool

class RefTemp(BaseModel):
    refTemp: int

class FrzTemp(BaseModel):
    frzTemp: int

class IsIceOn(BaseModel):
    isIceOn: bool

class IsChildLock(BaseModel):
    isChildLock: bool

class IsMagicZone(BaseModel):
    isMagicZone: bool

class IsMute(BaseModel):
    isMute: bool

class IsVacation(BaseModel):
    isVacation: bool

class IsFilterReset(BaseModel):
    isFilterReset: bool

class FilterTime(BaseModel):
    filterTime: int

class Unknown(BaseModel):
    Unknown: bool

RefrigeratorSetSensors = Union[
    IsSuperFrz,
    IsSuperRef,
    IsSleep,
    CrushOrCube,
    IsLight,
    RefTemp,
    FrzTemp,
    IsIceOn,
    IsChildLock,
    IsMagicZone,
    IsMute,
    IsVacation,
    IsFilterReset,
    FilterTime,
    Unknown,
]

class SetNodeRequest(BaseModel):
    reasoning: str
    isItInAllowedSensorsAndWeHaveValidValue: bool
    refrigerator: RefrigeratorSetSensors
    actionType: Literal["Set", "Up", "Down", "Max", "Min"]


class GetNodeRequest(BaseModel):
    reasoning: str
    isItInAllowedSensors: bool
    refrigerator: Set[Literal[
        "isSuperFrz", "isSuperRef", "isSleep", "crushOrcube", "isLight", "refTemp", "frzTemp",
        "isIceOn", "isChildLock", "isMagicZone", "isMute", "isVacation", "enviromentTemp",
        "isFilterReset", "isFrzDoorOpen", "isRefDoorOpen", "filterTime", "unknown"
    ]]

class GetChatNodeResponse(BaseModel):
    success_output: str
    failed_output: str


class SetChatNodeResponse(BaseModel):
    success_output: str
    failed_output: str
