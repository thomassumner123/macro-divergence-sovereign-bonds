"""
data_loader.py
==============
Reusable data loading functions for the Macro Divergence and Sovereign Bond Value project.
All processed CSVs are loaded from /data/processed/ relative to the project root.

Usage in notebooks:
    import sys
    sys.path.append("..")
    from src.data_loader import load_yields, load_macro, load_boe_nominal ...

Author: Thomas Sumner
Date: May 2026
"""

import pandas as pd
import os

# Path to processed data directory
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def _load(filename, **kwargs):
    """Internal helper -- loads a CSV from the processed directory."""
    path = os.path.join(PROCESSED_DIR, filename)
    return pd.read_csv(path, index_col=0, parse_dates=True, **kwargs)


# ---------------------------------------------------------------
# FRED Series
# ---------------------------------------------------------------

def load_yields():
    """
    Nominal sovereign yield curves from FRED.
    Daily frequency. Columns: US_2Y, US_5Y, US_10Y, US_30Y,
    EUR_BUND_10Y, JPN_JGB_10Y.
    Note: EUR and JPN columns are monthly series -- significant NaN gaps.
    Use load_macro() for monthly EUR/JPN yield data.
    """
    return _load("yields_daily.csv")


def load_real_yields():
    """
    US TIPS real yields and 10Y breakeven inflation from FRED.
    Daily frequency. Columns: US_TIPS_5Y, US_TIPS_10Y, US_TIPS_30Y,
    US_BREAKEVEN_10Y.
    """
    return _load("real_yields_daily.csv")


def load_fx():
    """
    FX spot rates from FRED. Daily frequency.
    Columns: GBPUSD, EURUSD, USDJPY.
    """
    return _load("fx_daily.csv")


def load_credit():
    """
    ICE BofA OAS credit spreads from FRED.
    Daily frequency. Columns: US_IG_OAS, US_HY_OAS, EUR_HY_OAS.
    Note: Data available from May 2023 only -- pre-2023 history behind paywall.
    UK IG OAS not available on FRED -- omitted.
    """
    return _load("credit_daily.csv")


def load_market():
    """
    Market and risk series from FRED. Daily frequency.
    Columns: VIX, BRENT, US_FED_FUNDS_DAILY, EUR_ECB_RATE.
    Note: Series extends beyond 2015 start -- filter to project sample where required.
    """
    return _load("market_daily.csv")


def load_macro():
    """
    Monthly macroeconomic series from FRED.
    Columns: US_CPI, US_CPI_CORE, US_PCE, US_PCE_CORE, US_UNEMPLOYMENT,
    US_FED_FUNDS, EUR_CPI, EUR_UNEMPLOYMENT, EUR_BUND_10Y,
    JPN_CPI, JPN_JGB_10Y, JPN_BOJ_RATE.
    Note: JPN_CPI has ~58 missing observations -- data limitation acknowledged.
    EUR_UNEMPLOYMENT incomplete post-2023 -- use load_ecb_unemployment() instead.
    """
    return _load("macro_monthly.csv")


def load_gdp():
    """
    US real GDP from FRED. Quarterly frequency.
    Columns: US_GDP_REAL.
    """
    return _load("gdp_quarterly.csv")


def load_equities():
    """
    Equity indices and commodities from yfinance. Daily frequency.
    Columns: SP500, FTSE100, EUROSTOXX, NIKKEI, GOLD, BRENT_YF.
    """
    return _load("equities_commodities_daily.csv")


# ---------------------------------------------------------------
# Bank of England Series
# ---------------------------------------------------------------

def load_boe_nominal():
    """
    UK nominal gilt spot curve from BoE Statistical Interactive Database.
    Daily frequency. Columns: 2Y, 5Y, 10Y, 30Y.
    Note: 30Y NaN prior to January 2016 -- BoE curve extended only to 25Y before that date.
    """
    return _load("boe_nominal_daily.csv")


def load_boe_real():
    """
    UK real gilt spot curve from BoE Statistical Interactive Database.
    Daily frequency. Columns: 5Y, 10Y, 30Y.
    Note: Curve begins at 5Y -- no short-maturity index-linked gilts issued.
    30Y NaN prior to January 2016.
    """
    return _load("boe_real_daily.csv")


def load_boe_inflation():
    """
    UK inflation breakeven curve from BoE Statistical Interactive Database.
    Daily frequency. Columns: 5Y, 10Y, 30Y.
    Note: Curve begins at 5Y. 30Y NaN prior to January 2016.
    """
    return _load("boe_inflation_daily.csv")


# ---------------------------------------------------------------
# ONS Series
# ---------------------------------------------------------------

def load_ons_monthly():
    """
    UK macroeconomic series from ONS. Monthly frequency.
    Columns: UK_CPI, UK_CPI_CORE, UK_CPI_SERVICES, UK_UNEMPLOYMENT.
    """
    return _load("ons_monthly.csv")


def load_ons_gdp():
    """
    UK GDP chained volume measure from ONS. Quarterly frequency.
    Columns: UK_GDP.
    """
    return _load("ons_gdp_quarterly.csv")


# ---------------------------------------------------------------
# ECB Series
# ---------------------------------------------------------------

def load_ecb_hicp():
    """
    Eurozone HICP inflation components from ECB Statistical Data Warehouse.
    Monthly frequency. Annual rate of change.
    Columns: EUR_HICP_HEADLINE, EUR_HICP_CORE, EUR_HICP_SERVICES, EUR_HICP_ENERGY.
    Use for inflation decomposition analysis -- preferred over FRED EUR_CPI series.
    """
    return _load("ecb_hicp_monthly.csv")


def load_ecb_aaa_yields():
    """
    ECB AAA-rated Eurozone government bond spot curve.
    Daily frequency. Columns: EUR_AAA_2Y, EUR_AAA_5Y, EUR_AAA_10Y, EUR_AAA_30Y.
    Note: NOT a pure German Bund series -- modelled curve fitted to AAA-rated
    Eurozone sovereigns (predominantly Germany, Netherlands, Finland).
    Use for yield curve shape and rate differential analysis only.
    Use FRED EUR_BUND_10Y as primary sovereign benchmark in relative value analysis.
    """
    return _load("ecb_aaa_yields_daily.csv")


def load_ecb_unemployment():
    """
    Eurozone unemployment rate from ECB Statistical Data Warehouse.
    Monthly frequency, seasonally adjusted, age 15-74.
    Columns: EUR_UNEMPLOYMENT_ECB.
    Preferred over FRED EUR_UNEMPLOYMENT which is incomplete post-2023.
    """
    return _load("ecb_unemployment_monthly.csv")


# ---------------------------------------------------------------
# IMF Series
# ---------------------------------------------------------------

def load_imf_output_gap():
    """
    Output gap estimates (% of potential GDP) from IMF WEO April 2026 vintage.
    Annual frequency. Columns: UK, US, Germany, Japan.
    Covers 2015-2026 including IMF forward projections from 2025.
    Note: Output gap estimates are uncertain and subject to revision between vintages.
    """
    return _load("imf_output_gap_annual.csv")
