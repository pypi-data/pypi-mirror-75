from typing import Callable, TypeVar, Dict, Union, List

from . import (
    TRACABSerializer,
    MetricaTrackingSerializer,
    EPTSSerializer,
    StatsBombSerializer,
    OptaSerializer,
)
from .domain import (
    Dataset,
    Frame,
    Event,
    TrackingDataset,
    Transformer,
    Orientation,
    PitchDimensions,
    Dimension,
    EventDataset,
    PassEvent,
    CarryEvent,
    PassResult,
    EventType,
    Player, DataRecord,
)


def load_tracab_tracking_data(
    metadata_filename: str, raw_data_filename: str, options: dict = None
) -> TrackingDataset:
    serializer = TRACABSerializer()
    with open(metadata_filename, "rb") as metadata, open(
        raw_data_filename, "rb"
    ) as raw_data:

        return serializer.deserialize(
            inputs={"metadata": metadata, "raw_data": raw_data},
            options=options,
        )


def load_metrica_tracking_data(
    raw_data_home_filename: str,
    raw_data_away_filename: str,
    options: dict = None,
) -> TrackingDataset:
    serializer = MetricaTrackingSerializer()
    with open(raw_data_home_filename, "rb") as raw_data_home, open(
        raw_data_away_filename, "rb"
    ) as raw_data_away:

        return serializer.deserialize(
            inputs={
                "raw_data_home": raw_data_home,
                "raw_data_away": raw_data_away,
            },
            options=options,
        )


def load_epts_tracking_data(
    metadata_filename: str, raw_data_filename: str, options: dict = None
) -> TrackingDataset:
    serializer = EPTSSerializer()
    with open(metadata_filename, "rb") as metadata, open(
        raw_data_filename, "rb"
    ) as raw_data:

        return serializer.deserialize(
            inputs={"metadata": metadata, "raw_data": raw_data},
            options=options,
        )


def load_statsbomb_event_data(
    event_data_filename: str, lineup_data_filename: str, options: dict = None
) -> EventDataset:
    serializer = StatsBombSerializer()
    with open(event_data_filename, "rb") as event_data, open(
        lineup_data_filename, "rb"
    ) as lineup_data:

        return serializer.deserialize(
            inputs={"event_data": event_data, "lineup_data": lineup_data},
            options=options,
        )


def load_opta_event_data(
    f24_data_filename: str, f7_data_filename: str, options: dict = None
) -> EventDataset:
    serializer = OptaSerializer()
    with open(f24_data_filename, "rb") as f24_data, open(
        f7_data_filename, "rb"
    ) as f7_data:

        return serializer.deserialize(
            inputs={"f24_data": f24_data, "f7_data": f7_data}, options=options,
        )


DatasetType = TypeVar("DatasetType")


def transform(
    dataset: DatasetType, to_orientation=None, to_pitch_dimensions=None
) -> DatasetType:
    if to_orientation and isinstance(to_orientation, str):
        to_orientation = Orientation[to_orientation]
    if to_pitch_dimensions and (
        isinstance(to_pitch_dimensions, list)
        or isinstance(to_pitch_dimensions, tuple)
    ):
        to_pitch_dimensions = PitchDimensions(
            x_dim=Dimension(*to_pitch_dimensions[0]),
            y_dim=Dimension(*to_pitch_dimensions[1]),
        )
    return Transformer.transform_dataset(
        dataset=dataset,
        to_orientation=to_orientation,
        to_pitch_dimensions=to_pitch_dimensions,
    )


def _frame_to_pandas_row_converter(frame: Frame) -> Dict:
    row = dict(
        period_id=frame.period.id if frame.period else None,
        timestamp=frame.timestamp,
        ball_state=frame.ball_state.value if frame.ball_state else None,
        ball_owning_team_id=frame.ball_owning_team.team_id
        if frame.ball_owning_team
        else None,
        ball_x=frame.ball_coordinates.x if frame.ball_coordinates else None,
        ball_y=frame.ball_coordinates.y if frame.ball_coordinates else None,
    )
    for player, coordinates in frame.players_coordinates.items():
        row.update(
            {
                f"{player.player_id}_x": coordinates.x,
                f"{player.player_id}_y": coordinates.y,
            }
        )

    return row


def _event_to_pandas_row_converter(event: Event) -> Dict:
    row = dict(
        event_id=event.event_id,
        event_type=(
            event.event_type.value
            if event.event_type != EventType.GENERIC
            else f"GENERIC:{event.event_name}"
        ),
        result=event.result.value if event.result else None,
        success=event.result.is_success if event.result else None,
        period_id=event.period.id,
        timestamp=event.timestamp,
        end_timestamp=None,
        ball_state=event.ball_state.value if event.ball_state else None,
        ball_owning_team=event.ball_owning_team.team_id
        if event.ball_owning_team
        else None,
        team_id=event.team.team_id,
        player_id=event.player.player_id,
        coordinates_x=event.coordinates.x if event.coordinates else None,
        coordinates_y=event.coordinates.y if event.coordinates else None,
    )
    if isinstance(event, PassEvent) and event.result == PassResult.COMPLETE:
        row.update(
            {
                "end_timestamp": event.receive_timestamp,
                "end_coordinates_x": event.receiver_coordinates.x,
                "end_coordinates_y": event.receiver_coordinates.y,
                "receiver_player_id": event.receiver_player.player_id
                if event.receiver_player
                else None,
            }
        )
    elif isinstance(event, CarryEvent):
        row.update(
            {
                "end_timestamp": event.end_timestamp,
                "end_coordinates_x": event.end_coordinates.x,
                "end_coordinates_y": event.end_coordinates.y,
            }
        )
    return row


def to_pandas(
    dataset: Union[Dataset, List[DataRecord]],
    _record_converter: Callable = None,
    additional_columns: Dict = None,
) -> "DataFrame":
    try:
        import pandas as pd
    except ImportError:
        raise Exception(
            "Seems like you don't have pandas installed. Please"
            " install it using: pip install pandas"
        )

    if isinstance(dataset, Dataset):
        records = dataset.records
    elif isinstance(dataset, list):

        records = dataset
    else:
        raise Exception("Unknown dataset type")

    if not _record_converter:
        if isinstance(dataset, TrackingDataset) or isinstance(records[0], Frame):
            _record_converter = _frame_to_pandas_row_converter
        elif isinstance(dataset, EventDataset) or isinstance(records[0], Event):
            _record_converter = _event_to_pandas_row_converter
        else:
            raise Exception("Don't know how to convert rows")

    def generic_record_converter(record: Union[Frame, Event]):
        row = _record_converter(record)
        if additional_columns:
            for k, v in additional_columns.items():
                if callable(v):
                    value = v(record)
                else:
                    value = v
                row.update({k: value})

        return row

    return pd.DataFrame.from_records(
        map(generic_record_converter, records)
    )


__all__ = [
    "load_tracab_tracking_data",
    "load_metrica_tracking_data",
    "load_epts_tracking_data",
    "load_statsbomb_event_data",
    "load_opta_event_data",
    "to_pandas",
    "transform",
]
