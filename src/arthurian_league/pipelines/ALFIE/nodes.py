# Add in rudementary 'Fixture Rating' based on closeness of a game, also taking into account the total goals scored 
# Arthurian League Fixture Index Evaluation (ALFIE)
import numpy as np
from arthurian_league.pipelines.scrape_fixture_data.nodes import _save_as_csv

def _ALFIE_rating(df, new_col, homescore, awayscore):
    ttl_gls = df[homescore] + df[awayscore]
    gl_diff = np.abs(df[homescore] - df[awayscore])
    ttl_gls_rt = np.sqrt(ttl_gls/2)
    
    close_rating = np.where(gl_diff < 3.5, 3.5 - gl_diff, 
                                np.where(gl_diff > 4.5, -2, 0)) 

    ALFIE = np.abs(round(ttl_gls_rt + close_rating))
    df[new_col] = ALFIE
    return df

