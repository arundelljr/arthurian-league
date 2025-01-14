import numpy as np

# Add in rudementary 'Fixture Rating' based on closeness of a game, also taking into account the total goals scored 
# Arthurian League Fixture Index Evaluation (ALFIE)

def _ALFIE_rating(df, new_col, homescore, awayscore):
    
    ttl_gls = df[homescore] + df[awayscore] # Total goals
    gl_diff = np.abs(df[homescore] - df[awayscore]) # Goal difference
    
    ttl_gls_rt = np.sqrt(ttl_gls/2) # Sqaure root of half the total goals 
    close_rating = np.where(gl_diff < 3.5, 3.5 - gl_diff, 
                                np.where(gl_diff > 4.5, -2, 0)) # Points added for close games and taken away for one-sided games 

    ALFIE = np.abs(round(ttl_gls_rt + close_rating)) # Add these values to genereate ALFIE rating for each fixture
    df[new_col] = ALFIE # Input under new column
    return df

