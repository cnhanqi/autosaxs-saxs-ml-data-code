# Central plotting settings
import matplotlib

DPI = 300
FIGSIZE = (6, 4)
DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_FONT_SCALE = 2.0


def apply(font_scale: float | None = None, font_family: str | None = None):
    """Apply global matplotlib rcParams for consistent plots.
    - font_scale: multiplies the base font size across axes/title/ticks/legend
    - font_family: preferred font family
    """
    base_font = float(matplotlib.rcParams.get('font.size', 10))
    fs = float(DEFAULT_FONT_SCALE if font_scale is None else font_scale)
    matplotlib.rcParams['font.size'] = base_font * fs
    for key in ('axes.labelsize', 'axes.titlesize', 'xtick.labelsize', 'ytick.labelsize', 'legend.fontsize'):
        matplotlib.rcParams[key] = matplotlib.rcParams['font.size']
    if font_family:
        matplotlib.rcParams['font.family'] = font_family

# ============== OLIGOMER plotting defaults (Step3) ==============
# Experimental curve (log-x figure)
OLIGO_EXP_COLOR = "0.5"
OLIGO_EXP_MARKER = "."
OLIGO_EXP_MARKERSIZE = 3.0

# Fit curve
OLIGO_FIT_COLOR = "#EC4706"
OLIGO_BASE_LINEWIDTH = 3.0
OLIGO_FIT_LINEWIDTH_MULT = 2.0

# Log-x ticks/labels
OLIGO_LOGX_TICKS = [0.01, 0.1, 0.2]
OLIGO_LOGX_TICKLABELS = ["0.01", "0.1", "0.2"]

# Annotations
OLIGO_ANNOT_FONTSIZE = 12

# Composition display order and colors
OLIGO_COMP_DISPLAY_ORDER = ["monomer", "dimer", "tetramer", "hexamer", "octamer"]
OLIGO_COMP_COLORS = {
    "monomer": "#749D65",
    "dimer": "#9366BC",
    "tetramer": "#5989B5",
    "hexamer": "#E37F48",
    "octamer": "#D4B833",
}

# Optional text positions
OLIGO_COMP_TEXT_POS = (0.02, 0.04)
OLIGO_TIME_LABEL_POS = (0.02, 0.7)
OLIGO_COMP_FONTSIZE = 9

# Composition table / text (v2)
OLIGO_COMP_TABLE_FONTSIZE = 10
OLIGO_COMP_TABLE_ROW_HEIGHT = 2.25  # equals 1.5 * 1.5
OLIGO_COMP_TABLE_BBOX = [0.02, 0.02, 0.6, 0.5]
OLIGO_COMP_TEXT_FONTSIZE = 9
OLIGO_COMP_TEXT_LINEHEIGHT = 1.3

# ============== CRYSTAL plotting defaults (Step3 --mode crystal) ==============
# By default crystal inherits the same visual settings as oligo.
# Override individual values here when the crystal figures need a different look.
CRYST_EXP_COLOR = OLIGO_EXP_COLOR
CRYST_EXP_MARKER = OLIGO_EXP_MARKER
CRYST_EXP_MARKERSIZE = OLIGO_EXP_MARKERSIZE
CRYST_FIT_COLOR = OLIGO_FIT_COLOR
CRYST_BASE_LINEWIDTH = OLIGO_BASE_LINEWIDTH
CRYST_FIT_LINEWIDTH_MULT = OLIGO_FIT_LINEWIDTH_MULT
CRYST_LOGX_TICKS = OLIGO_LOGX_TICKS
CRYST_LOGX_TICKLABELS = OLIGO_LOGX_TICKLABELS
CRYST_ANNOT_FONTSIZE = OLIGO_ANNOT_FONTSIZE
CRYST_COMP_DISPLAY_ORDER = OLIGO_COMP_DISPLAY_ORDER
CRYST_COMP_COLORS = dict(OLIGO_COMP_COLORS)
CRYST_COMP_TEXT_POS = OLIGO_COMP_TEXT_POS
CRYST_COMP_FONTSIZE = OLIGO_COMP_FONTSIZE
CRYST_TIME_LABEL_POS = OLIGO_TIME_LABEL_POS
CRYST_COMP_TABLE_FONTSIZE = OLIGO_COMP_TABLE_FONTSIZE
CRYST_COMP_TABLE_ROW_HEIGHT = OLIGO_COMP_TABLE_ROW_HEIGHT
CRYST_COMP_TABLE_BBOX = list(OLIGO_COMP_TABLE_BBOX)
CRYST_COMP_TEXT_FONTSIZE = OLIGO_COMP_TEXT_FONTSIZE
CRYST_COMP_TEXT_LINEHEIGHT = OLIGO_COMP_TEXT_LINEHEIGHT
