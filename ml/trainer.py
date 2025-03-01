
from statsforecast import StatsForecast
from statsforecast.models import (
    AutoARIMA,
    AutoETS,
    HoltWinters,
    CrostonClassic as Croston, 
    HistoricAverage,
    DynamicOptimizedTheta as DOT,
    SeasonalNaive
)

def train_with_statsforecast(df_monthly):
    print("Training...")
    modelArima = AutoARIMA(
            season_length = 12, 
            # seasonal=True,
            trace=True,
            # approximation=False,
        )

    modelETS = AutoETS(
        season_length=12
    )
    
    models = [
        modelArima,
        modelETS,
        HoltWinters(season_length=12),
        # Croston(prediction_intervals=[90]),
        SeasonalNaive(season_length=12),
        HistoricAverage(),
        DOT(season_length=4)
    ]

    sf = StatsForecast(
        models=models,
        freq='MS'
    )
    sf.fit(df_monthly)
    
    return sf