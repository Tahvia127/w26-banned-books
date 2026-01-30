"""
Google Trends Data Collection Script
Collects search volume data for banned books
Author: Kevin (Google Trends Specialist)
"""

import pandas as pd
from pytrends.request import TrendReq
import time
from datetime import datetime, timedelta
import numpy as np
from tqdm import tqdm
import logging

'''
pandas: data tables (DataFrames).

pytrends: unofficial Google Trends API.

time: for sleep delays (avoids rate limits).

datetime/timedelta: for date math around ban dates.

numpy: numerical operations (mean, std, etc.).

tqdm: progress bars.

logging: records successes/failures to a log file.

'''

# Set up logging

'''
Creates a log file that:

Records timestamps,

Notes whether each book succeeds or fails,

Helps you debug errors later without printing everything to the console.

'''
logging.basicConfig(
    filename='data_collection.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize pytrends
''' 
hl: English (U.S.) interface
tz = timezone: for us in EST

'''
pytrends = TrendReq(hl='en-US', tz=360)

def get_trends_data(book_title, ban_date_str, retries=3):
    """
    Collect Google Trends data for a book around its ban date
    
    Parameters:
    - book_title: String, the book title to search
    - ban_date_str: String in format 'YYYY-MM-DD'
    - retries: Number of times to retry if request fails
    
    Returns:
    - Dictionary with before/after search volumes
    """
    
    # Convert ban date string to datetime: allows Python to actually work with our dates
    try:
        ban_date = datetime.strptime(ban_date_str, '%Y-%m-%d')
    except:
        logging.error(f"Invalid date format for {book_title}: {ban_date_str}")
        return None
    
    # Define time periods: analyzing 3 months (90 days) before and after ban.
    before_start = ban_date - timedelta(days=90)
    before_end = ban_date - timedelta(days=1)
    after_start = ban_date + timedelta(days=1)
    after_end = ban_date + timedelta(days=90)
    
    # Format dates for pytrends: in this format, our data is compatible with Google Trends
    before_timeframe = f"{before_start.strftime('%Y-%m-%d')} {before_end.strftime('%Y-%m-%d')}"
    after_timeframe = f"{after_start.strftime('%Y-%m-%d')} {after_end.strftime('%Y-%m-%d')}"
    
    # Try collecting data with retries (prevents script from crashing from a bad book)
    for attempt in range(retries):
        try:
            # Get BEFORE ban data
            '''
            Requests Google Trends interest for that book title.

            Restricts to the U.S.

            Returns a DataFrame with weekly search interest scores (0 - 100 scale). 

            '''
            pytrends.build_payload([book_title], timeframe=before_timeframe, geo='US')
            before_df = pytrends.interest_over_time()

            #If data exists, compute summary statistics. If Google returns nothing → treat as zero interest
            if not before_df.empty and book_title in before_df.columns:
                before_values = before_df[book_title].values
                before_avg = np.mean(before_values)
                before_max = np.max(before_values)
                before_min = np.min(before_values)
            else:
                before_avg = before_max = before_min = 0
            
            # Wait to avoid rate limiting
            time.sleep(12)
            
            # Get AFTER ban data, same process as before
            pytrends.build_payload([book_title], timeframe=after_timeframe, geo='US')
            after_df = pytrends.interest_over_time()
            
            if not after_df.empty and book_title in after_df.columns:
                after_values = after_df[book_title].values
                after_avg = np.mean(after_values)
                after_max = np.max(after_values)
                after_min = np.min(after_values)
            else:
                after_avg = after_max = after_min = 0
            
            # Calculate metrics (comparing search popularity)
            if before_avg > 0:
                percent_change = ((after_avg - before_avg) / before_avg) * 100
                absolute_change = after_avg - before_avg
            else:
                percent_change = 0 if after_avg == 0 else float('inf')
                absolute_change = after_avg
            
            # Calculate volatility (standard deviation)
            all_values = list(before_values) + list(after_values)
            volatility = np.std(all_values) if len(all_values) > 0 else 0
            
            logging.info(f"Successfully collected data for: {book_title}")
            
            return {
                'book_title': book_title,
                'ban_date': ban_date_str,
                'avg_search_before': round(before_avg, 2),
                'avg_search_after': round(after_avg, 2),
                'max_search_before': before_max,
                'max_search_after': after_max,
                'min_search_before': before_min,
                'min_search_after': after_min,
                'percent_change': round(percent_change, 2),
                'absolute_change': round(absolute_change, 2),
                'volatility': round(volatility, 2),
                'data_collected': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'collection_successful': True
            }
            
        except Exception as e:
            if attempt < retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed for {book_title}: {e}. Retrying...")
                time.sleep(20)  # Wait longer before retry
            else:
                logging.error(f"All attempts failed for {book_title}: {e}")
                return {
                    'book_title': book_title,
                    'ban_date': ban_date_str,
                    'avg_search_before': None,
                    'avg_search_after': None,
                    'max_search_before': None,
                    'max_search_after': None,
                    'min_search_before': None,
                    'min_search_after': None,
                    'percent_change': None,
                    'absolute_change': None,
                    'volatility': None,
                    'data_collected': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'collection_successful': False,
                    'error': str(e)
                }

# TEST FUNCTION (Week 1)
def test_collection():
    """Test the collection function with a few books"""
    test_books = [
        ("Gender Queer", "2022-09-01"),
        ("All Boys Aren't Blue", "2022-10-15"),
        ("The Bluest Eye", "2022-08-20")
    ]
    
    results = []
    for title, date in test_books:
        print(f"Testing: {title}")
        result = get_trends_data(title, date)
        results.append(result)
        print(f"Result: {result}\n")
    
    # Save test results
    test_df = pd.DataFrame(results)
    from pathlib import Path
    # Ensure folder exists at the correct location (project root)
    Path("../data/raw").mkdir(parents=True, exist_ok=True)
    # Save CSV in project root data/raw folder
    test_df.to_csv("../data/raw/test_results.csv", index=False)
    print("Test results saved to ../data/raw/test_results.csv")


# FULL COLLECTION FUNCTION (Week 2)
def collect_all_books(input_csv='pen_america_banned_books.csv', output_csv='data/raw/google_trends_complete.csv'):
    """
    Collect Google Trends data for all books in PEN America dataset
    
    Parameters:
    - input_csv: Path to PEN America CSV
    - output_csv: Path to save results
    """
    # Read input data
    books_df = pd.read_csv(input_csv)
    print(f"Found {len(books_df)} books to process")
    
    # Initialize results list
    all_results = []
    
    # Process each book with progress bar
    for index, row in tqdm(books_df.iterrows(), total=len(books_df), desc="Collecting data"):
        book_title = row['Book Title']  # Adjust column name as needed
        ban_date = row['Ban Date']       # Adjust column name as needed
        
        # Collect data
        result = get_trends_data(book_title, ban_date)
        if result:
            result['state'] = row.get('State', 'Unknown')  # Add state if available
            all_results.append(result)
        
        # Save progress every 10 books
        if (index + 1) % 10 == 0:
            temp_df = pd.DataFrame(all_results)
            temp_df.to_csv(output_csv.replace('.csv', '_temp.csv'), index=False)
            print(f"\nProgress saved: {index + 1}/{len(books_df)} books completed")
    
    # Save final results
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(output_csv, index=False)
    
    # Print summary statistics
    print("\n=== COLLECTION COMPLETE ===")
    print(f"Total books processed: {len(results_df)}")
    print(f"Successful collections: {results_df['collection_successful'].sum()}")
    print(f"Failed collections: {(~results_df['collection_successful']).sum()}")
    print(f"Average percent change: {results_df['percent_change'].mean():.2f}%")
    print(f"Results saved to: {output_csv}")
    
    return results_df

# Main execution
if __name__ == "__main__":
    # Week 1: Run test
    print("Running test collection...")
    test_collection()
    
    # Week 2: Uncomment this to run full collection
    # print("Running full collection...")
    # collect_all_books()
    