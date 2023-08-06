import pandas as pd
import pendulum
from . import settings, brokers, indicators


@pd.api.extensions.register_dataframe_accessor("ParseTime")
class ParseTime:
    def __init__(self, klines_dataframe):
        self._klines = klines_dataframe

    def from_human_readable_to_timestamp(self):
        self._klines.loc[:, "Open_time"] = self._klines.apply(
            lambda date_time: ParseDateTime(
                date_time["Open_time"]
            ).from_human_readable_to_timestamp(),
            axis=1,
        )

        if "Close_time" in self._klines:
            self._klines.loc[:, "Close_time"] = self._klines.apply(
                lambda date_time: ParseDateTime(
                    date_time["Close_time"]
                ).from_human_readable_to_timestamp(),
                axis=1,
            )

    def from_timestamp_to_human_readable(self):
        self._klines.loc[:, "Open_time"] = self._klines.apply(
            lambda date_time: ParseDateTime(
                date_time["Open_time"]
            ).from_timestamp_to_human_readable(),
            axis=1,
        )

        if "Close_time" in self._klines:
            self._klines.loc[:, "Close_time"] = self._klines.apply(
                lambda date_time: ParseDateTime(
                    date_time["Close_time"]
                ).from_timestamp_to_human_readable(),
                axis=1,
            )


@pd.api.extensions.register_dataframe_accessor("save_to")
class SaveTo:
    def __init__(self, candles_dataframe):
        self._candles_dataframe = candles_dataframe

    def csv(self):
        pass

    def database(self):
        pass


@pd.api.extensions.register_dataframe_accessor("apply_indicator")
class ApplyIndicator:
    def __init__(self, candles_dataframe):
        self._candles_dataframe = candles_dataframe
        self.price = indicators.Price(self._candles_dataframe)
        self.trend = indicators.Trend(self._candles_dataframe)
        self.momentum = indicators.Momentum(self._candles_dataframe)
        self.volatility = indicators.Volatility(self._candles_dataframe)
        self.volume = indicators.Volume(self._candles_dataframe)


class ParseDateTime:
    fmt = "YYYY-MM-DD HH:mm:ss"

    def __init__(self, date_time_in):
        self.date_time_in = date_time_in

    def from_human_readable_to_timestamp(self):
        return pendulum.from_format(
            self.date_time_in, self.fmt, "UTC").int_timestamp

    def from_timestamp_to_human_readable(self):
        return pendulum.from_timestamp(
            self.date_time_in).to_datetime_string()


class KlinesFromBroker:
    """Dispondo basicamente de 3 métodos (oldest, newest, range), tem por 
    finalidade servir de fila para a solicitação de klines às corretoras,
    dividindo o número de requests a fim de respeitar os limites das mesmas e
    interrompendo os pedidos caso este limite esteja próximo de ser atingido,
    entregando ao cliente os candles sanitizados e formatados.
    """

    def __init__(self, broker: str, symbol: str, time_frame: str):

        self._symbol = symbol.upper()
        self._time_frame = time_frame
        self._broker = getattr(brokers, brokers.wrapper_for(broker))()
        self._oldest_open_time = self._broker._oldest_open_time(
            symbol=self._symbol, time_frame=self._time_frame
        )
        self._request_step = (
            self._broker.records_per_request *
            settings.TimeFrames().seconds_in(self._time_frame)
        )
        self._since = 1
        self._until = 2

    def _interporlate_missing(self):
        klines_in = self.klines
        klines_out = pd.DataFrame()
        since = klines_in.Open_time.iloc[0]
        step = settings.TimeFrames().seconds_in(self._time_frame)

        for open_time in range(since, self._until + 1, step):
            entry = klines_in.loc[klines_in.Open_time == open_time]

            if entry.empty:
                try:
                    data = {
                        "Open_time": [open_time],
                        "Open": [
                            klines_out.Open.rolling(3).mean().tail(1).item()],
                        "High": [
                            klines_out.High.rolling(3).mean().tail(1).item()],
                        "Low": [
                            klines_out.Low.rolling(3).mean().tail(1).item()],
                        "Close": [
                            klines_out.Close.rolling(3).mean().tail(1).item()],
                        "Volume": [
                            klines_out.Volume.rolling(3).mean().tail(1).item()]
                    }
                except:
                    data = {
                        "Open_time": [open_time],
                        "Open": [0.0],
                        "High": [0.0],
                        "Low": [0.0],
                        "Close": [0.0],
                        "Volume": [0.0]}
                finally:
                    entry = pd.DataFrame(data)
            klines_out = klines_out.append(entry, ignore_index=True)
        self.klines = klines_out

    def _klines_from_broker(self):
        self.klines = pd.DataFrame()
        for timestamp in range(
                self._since, self._until + 1, self._request_step):

            if self._broker.was_request_limit_reached():
                time.sleep(10)
                print("Sleeping cause request limit was hit.")

            self.klines = self.klines.append(self._broker.klines(
                symbol=self._symbol,
                time_frame=self._time_frame,
                since=timestamp
            ), ignore_index=True)

        self._interporlate_missing()
        self.klines.ParseTime.from_timestamp_to_human_readable()

        return self.klines

    def period(self, since: str, until: str) -> pd.DataFrame:
        now = (pendulum.now(tz="UTC")).int_timestamp
        self._since = ParseDateTime(
            since).from_human_readable_to_timestamp()
        self._until = ParseDateTime(
            until).from_human_readable_to_timestamp()

        if self._since < self._oldest_open_time:
            self._since = self._oldest_open_time
        if self._until > now:
            self._until = now

        return self._klines_from_broker()[:-1]

    def oldest(self, number_of_candles=1):
        now = (pendulum.now(tz="UTC")).int_timestamp
        self._since = self._oldest_open_time
        self._until = (
            (number_of_candles + 1) * (
                settings.TimeFrames().seconds_in(self._time_frame)
            ) + self._since)
        if self._until > now:
            self._until = now

        return self._klines_from_broker()[:number_of_candles]

    def newest(self, number_of_candles=1):
        now = (pendulum.now(tz="UTC")).int_timestamp
        self._until = now
        self._since = (
            self._until - (number_of_candles + 1) *
            (settings.TimeFrames().seconds_in(self._time_frame))
        )
        if self._since < self._oldest_open_time:
            self._since = self._oldest_open_time

        return self._klines_from_broker()[:number_of_candles]
