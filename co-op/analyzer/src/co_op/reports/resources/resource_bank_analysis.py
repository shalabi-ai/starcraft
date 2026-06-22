from pandas import DataFrame
from reports.resources.resource_bank_analysis_model import ResourceBankAnalysisModel


class ResourceBankAnalysis:
    def __init__(self, player_df: DataFrame):
        p = (
            player_df
            .sort_values("seconds")
            .reset_index(drop=True)
            .copy()
        )
        p["float_score"] = (
                p["minerals_current"]
                + 2.0 * p["vespene_current"]
        )
        self.player_df = p

    def __economy_grade(self, avg_float):
        if avg_float < 1000:
            return "A"
        elif avg_float < 2000:
            return "B"
        elif avg_float < 4000:
            return "C"
        elif avg_float < 8000:
            return "D"
        else:
            return "F"
    def get_resource_bank(self)->ResourceBankAnalysisModel:
        p = self.player_df
        model = ResourceBankAnalysisModel()
        model.avg_float = p["float_score"].mean()
        model.grade = self.__economy_grade(model.avg_float)

        model.avg_minerals = p["minerals_current"].mean()
        model.avg_gas = p["vespene_current"].mean()

        #max_minerals = p["minerals_current"].max()
        #max_gas = p["vespene_current"].max()

        model.final_minerals = p["minerals_current"].iloc[-1]
        model.final_gas = p["vespene_current"].iloc[-1]

        # Float Area (integral)
        #dt = p["seconds"].diff().fillna(0)  # compute Changes over time
        #float_area = (
        #        p["float_score"] * dt
        #).sum()
        #game_length = max(p["seconds"].max(), 1)
        #model.float_score = (
        #                      (float_area / game_length) * 60
        #              ) / 1000
        #model.grade = __economy_grade(model.float_score)

        # Collection Rate = resources/minute
        # ÷ 60            = resources/second
        # × dt            = resources collected during interval
        # 1200 minerals/min
        # 20 seconds
        #
        # becomes:
        #
        # 1200 / 60 = 20 minerals/sec
        #
        # 20 × 20 = 400 minerals collected
        dt = p["seconds"].diff().fillna(0)  # compute Changes over time
        model.total_minerals_collected = (
                (p["minerals_collection_rate"] / 60) * dt
        ).sum()
        model.total_gas_collected = (
                (p["vespene_collection_rate"] / 60) * dt
        ).sum()

        #final_bank = (
        #        model.final_minerals +
        #        model.final_gas
        #)

        #total_collected = (
        #        model.total_minerals_collected +
        #        model.total_gas_collected
        #)

        weighted_bank = (
                model.final_minerals +
                2 * model.final_gas
        )
        weighted_collected = (
                model.total_minerals_collected +
                2 * model.total_gas_collected
        )
        if weighted_collected > 0:
            model.spend_efficiency = (
                    100 *
                    (1 - weighted_bank / weighted_collected)
            )
        else:
            model.spend_efficiency = 0

        model.peak_minerals_collection_rate = p["minerals_collection_rate"].max()
        model.peak_gas_collection_rate = p["vespene_collection_rate"].max()

        model.game_minutes = p["seconds"].max() / 60

        model.spent_minerals = model.total_minerals_collected - model.final_minerals
        model.spent_gas = model.total_gas_collected - model.final_gas

        return model
