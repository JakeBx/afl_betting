import betfairlightweight
import pandas as pd

def process_runner_books(runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    
    best_back_prices = [runner_book.ex.available_to_back[0].price
                        if runner_book.ex.available_to_back
                        else 1.01
                        for runner_book
                        in runner_books]
    best_back_sizes = [runner_book.ex.available_to_back[0].size
                       if runner_book.ex.available_to_back
                       else 1.01
                       for runner_book
                       in runner_books]

    best_lay_prices = [runner_book.ex.available_to_lay[0].price
                       if runner_book.ex.available_to_lay
                       else 1000.0
                       for runner_book
                       in runner_books]
    best_lay_sizes = [runner_book.ex.available_to_lay[0].size
                      if runner_book.ex.available_to_lay
                      else 1.01
                      for runner_book
                      in runner_books]
    
    selection_ids= [runner_book.selection_id for runner_book in runner_books]
    last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    total_matched = [runner_book.total_matched for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]
    scratching_datetimes = [runner_book.removal_date for runner_book in runner_books]
    adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'Selection ID': selection_ids,
        'Best Back Price': best_back_prices,
        'Best Back Size': best_back_sizes,
        'Best Lay Price': best_lay_prices,
        'Best Lay Size': best_lay_sizes,
        'Last Price Traded': last_prices_traded,
        'Total Matched': total_matched,
        'Status': statuses,
        'Removal Date': scratching_datetimes,
        'Adjustment Factor': adjustment_factors
    })
    
    return df


def get_markets(event, trading):
    market_catalogue_filter = betfairlightweight.filters.market_filter(event_ids=[event])

    market_catalogues = trading.betting.list_market_catalogue(
        filter=market_catalogue_filter,
        max_results='100',
        sort='FIRST_TO_START'
    )

    # Create a DataFrame for each market catalogue
    market_types_df = pd.DataFrame({
        'Market Name': [market_cat_object.market_name for market_cat_object in market_catalogues],
        'Market ID': [market_cat_object.market_id for market_cat_object in market_catalogues],
        'Total Matched': [market_cat_object.total_matched for market_cat_object in market_catalogues],
    })
    
    market_types_df['Event ID'] = event
    
    return market_types_df

team_mapping = {
    'Greater Western Sydney':'GWS',
    'Brisbane Lions':'Brisbane'
}
def name_convert(name):
    if name in team_mapping.keys():
        return team_mapping[name]
    else:
        return name
    

# Grab all event type ids. This will return a list which we will iterate over to print out the id and the name of the sport
def get_sport_id(trading, sport):
    event_types = trading.betting.list_event_types()

    sport_ids = pd.DataFrame({
        'Sport': [event_type_object.event_type.name for event_type_object in event_types],
        'ID': [event_type_object.event_type.id for event_type_object in event_types]
    }).set_index('Sport').sort_index()

    return int(sport_ids.loc[sport])