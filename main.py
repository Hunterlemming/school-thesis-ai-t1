from services.csv_transformer import create_type_1_csv, create_type_2_csv
from services.log_parser import parse_default_csv


if __name__ == "__main__":
    summary = parse_default_csv('./data/raw_input_2.csv')
    # print(summary)
    # print(summary.get_day_by_date('2022-02-18'))
    create_type_1_csv(summary, 'A1', True)
    create_type_2_csv(summary, 'A1', ['A2'])
    create_type_2_csv(summary, 'A1', file_name='type_2_all_workmates.csv')
    create_type_1_csv(summary, 'A1', False, file_name='type_1_default_interval.csv')
    create_type_1_csv(summary, 'A1', False, intervals=[('08:00', '12:00')], file_name='type_1_morning.csv')
