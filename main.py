from services.csv_transformer import create_type_1_csv, create_type_2_csv
from services.log_parser import parse_default_csv
from services.lstm_trainers.multivariate_lstm import MultiVariateTrainer
from services.lstm_trainers.univariate_lstm import UniVariateTrainer


def parse_input(location: str) -> None:
    summary = parse_default_csv(location)
    create_type_1_csv(summary, 'A1', True)
    create_type_2_csv(summary, 'A1', ['A2'])
    create_type_2_csv(summary, 'A1', file_name='type_2_all_workmates.csv')
    create_type_1_csv(summary, 'A1', False, file_name='type_1_default_interval.csv')
    create_type_1_csv(summary, 'A1', False, intervals=[('08:00', '12:00')], file_name='type_1_morning.csv')

def ai_single_productivity() -> None:
    ai = UniVariateTrainer('./data/generated/gen_1.csv', target_column=1)
    ai.run_model(new_model=True)

def ai_pair_productivity() -> None:
    ai = MultiVariateTrainer('./data/generated/type_2_all_workmates.csv', target_column=1, independent_columns=[2])
    ai.run_model(new_model=True)

def ai_multi_workmate_productivity() -> None:
    ai = MultiVariateTrainer('./data/generated/type_2_all_workmates.csv', target_column=1, independent_columns=[2, 3])
    ai.run_model(new_model=True)

def ai_interval_productivity() -> None:
    ai = UniVariateTrainer('./data/generated/type_1_default_interval.csv', target_column=4)
    ai.run_model(new_model=True)

if __name__ == "__main__":
    parse_input('./data/raw_input_2.csv')
    
    # ai_single_productivity()
    # ai_pair_productivity()
    # ai_interval_productivity()
    # ai_multi_workmate_productivity()
