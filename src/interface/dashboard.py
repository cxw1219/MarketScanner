"""
Real-time market scanner dashboard with ASCII interface.
"""

import os
import sys
from datetime import datetime
import pandas as pd
import numpy as np
from colorama import init, Fore, Style, Back
import logging
from typing import Dict, List, Tuple

# Initialize colorama
init()

class Dashboard:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.terminal_width = 180
        self.data_cache = {}
        self.analysis_cache = {}
        
        # Normal spread ranges for different instrument types
        self.spread_ranges = {
            'PRECIOUS_METALS': {'XAU_USD': 0.10, 'XAG_USD': 0.15, 'XPT_USD': 0.20, 'XPD_USD': 0.35},
            'ENERGY': {'BCO_USD': 0.05, 'WTICO_USD': 0.07, 'NATGAS_USD': 0.30},
            'AGRICULTURE': {'CORN_USD': 0.25, 'SOYBN_USD': 0.20, 'WHEAT_USD': 0.20, 'SUGAR_USD': 0.15}
        }
        
        # Instrument groups with pretty names
        self.groups = {
            'PRECIOUS METALS': ['XAU_USD', 'XAG_USD', 'XPT_USD', 'XPD_USD'],
            'ENERGY': ['BCO_USD', 'WTICO_USD', 'NATGAS_USD'],
            'AGRICULTURE': ['CORN_USD', 'SOYBN_USD', 'WHEAT_USD', 'SUGAR_USD']
        }

        # Column definitions
        self.columns = [
            ("Instrument", 12),
            ("Bid", 10),
            ("Ask", 10),
            ("Spread", 7),
            ("24h %", 7),
            ("Signal", 8),
            ("Direction", 9),
            ("Target", 10),
            ("Stop", 10),
            ("R/R", 5),
            ("ATR%", 6),
            ("Volume", 8),
            ("Conf%", 6)
        ]

    def get_normalized_atr(self, instrument: str, atr: float, price: float) -> float:
        """Normalize ATR to percentage of price."""
        return (atr / price) * 100 if price > 0 else 0

    def get_spread_color(self, instrument: str, spread: float) -> str:
        """Get color for spread based on normal ranges."""
        for group, ranges in self.spread_ranges.items():
            if instrument in ranges:
                normal_spread = ranges[instrument]
                if spread <= normal_spread * 0.8:
                    return Fore.GREEN
                elif spread > normal_spread * 1.2:
                    return Fore.RED
                return Fore.WHITE
        return Fore.WHITE

    def calculate_risk_reward(self, current: float, target: float, stop: float) -> float:
        """Calculate risk/reward ratio with realistic values."""
        if not all(isinstance(x, (int, float)) for x in [current, target, stop]):
            return 0
        risk = abs(current - stop)
        reward = abs(target - current)
        return reward / risk if risk > 0 else 0