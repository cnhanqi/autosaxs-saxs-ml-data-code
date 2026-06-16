# Numeric thresholds and default parameters for analysis/plots
# Step1 pseudo-Rg window (q^2)
MIN_Q: float = 0.001
MAX_Q: float = 0.008

# Guinier overlay expansion on Y
OVERLAY_Y_EXPAND: float = 3.0

# Grid layout defaults
GRID_COLS: int = 6
GRID_ROWS = None  # keep None to auto-compute

# Log-SAXS grouped+offset defaults
GROUP_SIZE: int = 6
LAYOUT_B_DPI: int = 100
LAYOUT_B_COLS: int = 6
LAYOUT_B_ROWS: int = 2
LAYOUT_B_SUBPLOT_HEIGHT: float = 5.0
LAYOUT_B_CURVE_COLOR = None
LAYOUT_B_LINEWIDTH: float = 1.0
LAYOUT_B_X_MIN: float = 0.01
LAYOUT_B_X_MAX: float = 0.4

# Step3 (OLIGOMER) fit-quality thresholds — oligo mode
OLIGO_CHI2_OK_MAX: float = 200.0
OLIGO_CHI2_BORDERLINE_MAX: float = 1000.0
OLIGO_CONST_ONLY_CONST_MIN: float = 0.99
OLIGO_CONST_ONLY_OTHER_MAX: float = 1e-6

# Step3 (OLIGOMER) fit-quality thresholds — crystal mode
# Crystal fits are typically noisier, so the OK/Borderline bounds are wider.
CRYST_CHI2_OK_MAX: float = 1000.0
CRYST_CHI2_BORDERLINE_MAX: float = 2000.0
CRYST_CONST_ONLY_CONST_MIN: float = 0.99
CRYST_CONST_ONLY_OTHER_MAX: float = 1e-6

# Step3 plotting defaults (shared by both modes)
OLIGO_PLOT_NCOLS: int = 6
OLIGO_PLOT_NROWS: int = 9
OLIGO_PLOT_DPI: int = 300
