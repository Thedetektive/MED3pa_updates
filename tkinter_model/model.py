import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.cm as cm

# Set application styling
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class MED3paApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MED3pa Workspace")
        self.geometry("1150x800")
        self.configure(fg_color="#FFFFFF")

        # Configure Grid Layout for Main Window
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.nav_buttons = {}
        self.frames = {}

        # Handle graceful exit on window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ----------------------------------------------------
        # SIDEBAR NAVIGATION
        # ----------------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#F8F9FA", border_color="#E9ECEF", border_width=1)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Load the logo image
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open(r"tkinter_model/MEDomicsLabWithShadow700.png"),
                dark_image=Image.open(r"tkinter_model/MEDomicsLabWithShadow700.png"),
                size=(32, 32)
            )
        except Exception:
            logo_image = None

        # Header frame to hold image + text + badge side by side
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(pady=(20, 20), padx=20, anchor="w")

        if logo_image:
            self.logo_image_label = ctk.CTkLabel(self.logo_frame, image=logo_image, text="")
            self.logo_image_label.pack(side="left", padx=(0, 6))

        self.logo_label = ctk.CTkLabel(self.logo_frame, text="MED3pa", font=ctk.CTkFont(family="Arial", size=16, weight="bold"), text_color="#185FA5")
        self.logo_label.pack(side="left")

        self.version_badge = ctk.CTkLabel(self.logo_frame, text="v1", font=ctk.CTkFont(size=10, weight="bold"), fg_color="#185FA5", text_color="#E6F1FB", corner_radius=10, width=30, height=18)
        self.version_badge.pack(side="left", padx=(6, 0))

        # Nav Sections & Items mapped to their respective frames
        self.create_nav_header("Workspace")
        self.create_nav_item("Overview", target_frame="OverviewView")
        
        self.create_nav_header("Analysis")
        self.create_nav_item("Upload data", target_frame="UploadView")
        self.create_nav_item("MDR curves", target_frame="ResultsView")
        self.create_nav_item("Patient profiles", target_frame="ProfilesView")
        
        self.create_nav_header("Clinical Use")
        self.create_nav_item("Run Model", target_frame="RunView")
        self.create_nav_item("Patient lookup", target_frame="LookupView")
        self.create_nav_item("Session history", target_frame="HistoryView")

        self.sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_footer.pack(side="bottom", fill="x", pady=15, padx=10)
        ctk.CTkButton(self.sidebar_footer, text="⚙ Settings", fg_color="transparent", text_color="#495057", hover_color="#E9ECEF", anchor="w", height=32).pack(fill="x")

        # ----------------------------------------------------
        # VIEW REGISTRATION
        # ----------------------------------------------------
        self.frames["OverviewView"] = OverviewView(parent=self, controller=self)
        self.frames["UploadView"] = UploadConfigurationView(parent=self, controller=self)
        self.frames["ResultsView"] = ResultsReviewView(parent=self, controller=self)
        self.frames["ProfilesView"] = ProfilesView(parent=self, controller=self)
        self.frames["RunView"] = RunModelView(parent=self, controller=self)
        self.frames["LookupView"] = LookupView(parent=self, controller=self)
        self.frames["HistoryView"] = HistoryView(parent=self, controller=self)

        # Default to Overview
        self.show_frame("OverviewView")

    def on_closing(self):
        try:
            plt.close('all')
        except Exception:
            pass
        self.quit()
        self.destroy()

    def create_nav_header(self, text):
        ctk.CTkLabel(self.sidebar, text=text.upper(), font=ctk.CTkFont(size=10, weight="bold"), text_color="#ADB5BD").pack(anchor="w", padx=15, pady=(12, 4))

    def create_nav_item(self, text, target_frame=None):
        def cmd():
            if target_frame:
                self.show_frame(target_frame)
        btn = ctk.CTkButton(self.sidebar, text=f"  {text}", fg_color="transparent", text_color="#495057", 
                            font=ctk.CTkFont(size=13), anchor="w", height=32, corner_radius=6, hover_color="#E9ECEF", command=cmd)
        btn.pack(fill="x", padx=10, pady=1)
        self.nav_buttons[text] = btn

    def show_frame(self, page_name):
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent", text_color="#495057", font=ctk.CTkFont(size=13, weight="normal"))
        
        for frame in self.frames.values():
            frame.grid_remove()

        active_frame = self.frames[page_name]
        active_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=0)
        
        frame_to_btn = {
            "OverviewView": "Overview", "UploadView": "Upload data", 
            "ResultsView": "MDR curves", "ProfilesView": "Patient profiles",
            "RunView": "Run Model", "LookupView": "Patient lookup", "HistoryView": "Session history"
        }
        active_btn_text = frame_to_btn.get(page_name)
        if active_btn_text in self.nav_buttons:
            self.nav_buttons[active_btn_text].configure(fg_color="#FFFFFF", text_color="#185FA5", font=ctk.CTkFont(size=13, weight="bold"))


# ====================================================================
# TAB 1: OVERVIEW DASHBOARD
# ====================================================================
class OverviewView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Workspace Overview", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="System status and recent activity", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.create_kpi(cards_frame, 0, "Active Models Deployments", "3", "Running normally", "#0F6E56")
        self.create_kpi(cards_frame, 1, "Total Patients Scanned", "12,845", "Last 30 days", "#6C757D")
        self.create_kpi(cards_frame, 2, "System Alerts", "0", "No active warnings", "#6C757D")

        activity_card = ctk.CTkFrame(self, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        activity_card.pack(fill="x", pady=10)
        ctk.CTkLabel(activity_card, text="Recent Activity", font=ctk.CTkFont(size=14, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        
        self.add_activity_row(activity_card, "Model Training Completed", "ICU Mortality BaseModel v2 finished training on MIMIC-IV cohort.", "2 hours ago")
        self.add_activity_row(activity_card, "Data Uploaded", "User uploaded 'q3_cohort_eval.parquet' (45MB).", "Yesterday")
        self.add_activity_row(activity_card, "Threshold Adjusted", "Declaration rate for Model A reduced to 93%.", "3 days ago")

    def create_kpi(self, parent, col, title, value, sub, sub_color):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8, height=100)
        card.grid(row=0, column=col, padx=6, sticky="nsew")
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color="#212529").pack(anchor="w", padx=12)
        ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=11), text_color=sub_color).pack(anchor="w", padx=12, pady=(2, 8))

    def add_activity_row(self, parent, title, desc, time):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=8)
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(row, text=desc, font=ctk.CTkFont(size=12), text_color="#495057").pack(anchor="w")
        ctk.CTkLabel(row, text=time, font=ctk.CTkFont(size=11), text_color="#ADB5BD").pack(anchor="w")


# ====================================================================
# TAB 2: UPLOAD & CONFIGURATION
# ====================================================================
class UploadConfigurationView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        self.controller = controller

        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Analysis workspace", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="ICU in-hospital mortality · Configure Inputs", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        ctk.CTkButton(top_bar, text="Next step  →", fg_color="#185FA5", hover_color="#124A80", text_color="#FFFFFF", width=120, height=34, command=lambda: controller.show_frame("ResultsView")).pack(side="right", padx=5)

        self.draw_step_bar()

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 20))
        grid_frame.grid_columnconfigure(0, weight=3, uniform="main_split")
        grid_frame.grid_columnconfigure(1, weight=2, uniform="main_split")

        # ── LEFT COLUMN ──────────────────────────────────────────────
        left_col = ctk.CTkFrame(grid_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        model_card = ctk.CTkFrame(left_col, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        model_card.pack(fill="x")
        ctk.CTkLabel(model_card, text="🤖 Select Baseline Prediction Model", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=12)
        ctk.CTkLabel(model_card, text="Base Model Source Architecture", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15)
        ctk.CTkComboBox(model_card, values=["MIMIC-IV Base Logistics Ensemble", "Hippo-EHR Transformers v4", "Custom Local XGBoost Checkpoint"], width=320, height=32).pack(anchor="w", padx=15, pady=(2, 12))
        ctk.CTkLabel(model_card, text="Target Classification Label", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15)
        ctk.CTkComboBox(model_card, values=["In-Hospital Mortality Risk Factor", "30-Day Readmission Diagnostic Index", "Septic Shock Onset Threshold"], width=320, height=32).pack(anchor="w", padx=15, pady=(2, 15))

        # ── RIGHT COLUMN — collapsible IPC / APC / MPC sections ──────
        right_col = ctk.CTkFrame(grid_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        right_col.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        ctk.CTkLabel(right_col, text="Confidence Method Configuration",
                    font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5"
                    ).pack(anchor="w", padx=15, pady=(12, 8))

        self._build_ipc_section(right_col)
        self._build_apc_section(right_col)
        self._build_mpc_section(right_col)

        ctk.CTkButton(
            right_col, text="⚡ Run Pipeline Execution",
            fg_color="#0F6E56", hover_color="#0A4D3C", text_color="#FFFFFF",
            height=40, font=ctk.CTkFont(weight="bold"),
            command=lambda: controller.show_frame("ResultsView")
        ).pack(fill="x", padx=15, pady=(16, 15))

    # ── Collapsible section helper ────────────────────────────────────
    def _make_collapsible(self, parent, title, subtitle, accent):
        """Returns (outer_frame, body_frame, toggle_state_dict).
        Clicking the header toggles body_frame visibility."""
        state = {"open": False}

        outer = ctk.CTkFrame(parent, fg_color="#F8F9FA", border_color="#E9ECEF",
                            border_width=1, corner_radius=6)
        outer.pack(fill="x", padx=15, pady=(0, 8))

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=8)

        indicator = ctk.CTkLabel(header, text="▶", font=ctk.CTkFont(size=11),
                                text_color="#6C757D", width=14)
        indicator.pack(side="left", padx=(0, 6))

        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(title_block, text=title, font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=accent).pack(anchor="w")
        ctk.CTkLabel(title_block, text=subtitle, font=ctk.CTkFont(size=10),
                    text_color="#6C757D").pack(anchor="w")

        body = ctk.CTkFrame(outer, fg_color="transparent")
        # body is NOT packed yet — starts collapsed

        def toggle(e=None):
            if state["open"]:
                body.pack_forget()
                indicator.configure(text="▶")
                state["open"] = False
            else:
                body.pack(fill="x", padx=10, pady=(0, 10))
                indicator.configure(text="▼")
                state["open"] = True

        for widget in (header, indicator, title_block):
            widget.bind("<Button-1>", toggle)
        for child in title_block.winfo_children():
            child.bind("<Button-1>", toggle)

        return outer, body

    # ── IPC section ───────────────────────────────────────────────────
    def _build_ipc_section(self, parent):
        _, body = self._make_collapsible(
            parent,
            "IPC — Individualized Predictive Confidence",
            "Per-sample confidence estimation via algorithm hyperparameters",
            "#185FA5"
        )

        # Algorithm hyperparameters
        ctk.CTkLabel(body, text="Algorithm-Specific Hyperparameters",
                    font=ctk.CTkFont(size=11, weight="bold"), text_color="#495057"
                    ).pack(anchor="w", pady=(4, 2))

        hp_grid = ctk.CTkFrame(body, fg_color="transparent")
        hp_grid.pack(fill="x")
        hp_grid.grid_columnconfigure((0, 1), weight=1, uniform="ipc_hp")

        ctk.CTkLabel(hp_grid, text="n_estimators", font=ctk.CTkFont(size=11),
                    text_color="#6C757D").grid(row=0, column=0, sticky="w", pady=(2, 0))
        ctk.CTkEntry(hp_grid, placeholder_text="e.g. 100", height=28
                    ).grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(0, 6))

        ctk.CTkLabel(hp_grid, text="max_depth", font=ctk.CTkFont(size=11),
                    text_color="#6C757D").grid(row=0, column=1, sticky="w", pady=(2, 0))
        ctk.CTkEntry(hp_grid, placeholder_text="e.g. 5", height=28
                    ).grid(row=1, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(hp_grid, text="min_samples_split", font=ctk.CTkFont(size=11),
                    text_color="#6C757D").grid(row=2, column=0, sticky="w")
        ctk.CTkEntry(hp_grid, placeholder_text="e.g. 2", height=28
                    ).grid(row=3, column=0, sticky="ew", padx=(0, 6), pady=(0, 6))

        # Confidence metric formulation
        ctk.CTkLabel(body, text="Confidence Metric Formulation  (cᵢ)",
                    font=ctk.CTkFont(size=11, weight="bold"), text_color="#495057"
                    ).pack(anchor="w", pady=(6, 4))
        ctk.CTkLabel(body,
                    text="Choose how the per-sample target variable is defined.",
                    font=ctk.CTkFont(size=10), text_color="#6C757D", wraplength=240
                    ).pack(anchor="w", pady=(0, 4))

        self.ipc_metric_var = ctk.StringVar(value="continuous")
        ctk.CTkRadioButton(body, text="(1 − |ŷᵢ − yᵢ|)",
                        font=ctk.CTkFont(size=11), variable=self.ipc_metric_var,
                        value="continuous").pack(anchor="w", pady=(2, 4))
        ctk.CTkRadioButton(body, text="Custom function",
                        font=ctk.CTkFont(size=11), variable=self.ipc_metric_var,
                        value="custom", command=self._toggle_ipc_custom
                        ).pack(anchor="w", pady=(2, 4))

        self.ipc_custom_frame = ctk.CTkFrame(body, fg_color="transparent")
        ctk.CTkLabel(self.ipc_custom_frame, text="f(ŷᵢ, yᵢ) =",
                    font=ctk.CTkFont(size=11), text_color="#6C757D"
                    ).pack(anchor="w")
        self.ipc_custom_entry = ctk.CTkEntry(
            self.ipc_custom_frame,
            placeholder_text="e.g.  (1 − |ŷᵢ − yᵢ|)",
            height=30
        )
        self.ipc_custom_entry.pack(fill="x", pady=(2, 4))
     

    def _toggle_ipc_custom(self):
        if self.ipc_metric_var.get() == "custom":
            self.ipc_custom_frame.pack(fill="x", padx=0, pady=(0, 4))
        else:
            self.ipc_custom_frame.pack_forget()


    # ── APC section ───────────────────────────────────────────────────
    def _build_apc_section(self, parent):
        _, body = self._make_collapsible(
            parent,
            "APC — Aggregate Predictive Confidence",
            "Group-level confidence via decision tree complexity controls",
            "#0F6E56"
        )

        # Tree depth slider
        self.apc_depth_label = ctk.CTkLabel(body, text="Tree Depth  (max_depth)  —  3",
                                            font=ctk.CTkFont(size=11, weight="bold"),
                                            text_color="#495057")
        self.apc_depth_label.pack(anchor="w", pady=(4, 0))
        self.slider_depth = ctk.CTkSlider(
            body, from_=1, to=10, number_of_steps=9, height=16,
            command=lambda v: self.apc_depth_label.configure(
                text=f"Tree Depth  (max_depth)  —  {int(v)}")
        )
        self.slider_depth.set(3)
        self.slider_depth.pack(fill="x", pady=(2, 10))

        # Complexity controls
        ctk.CTkLabel(body, text="Complexity Control",
                    font=ctk.CTkFont(size=11, weight="bold"), text_color="#495057"
                    ).pack(anchor="w", pady=(2, 2))

        cc_grid = ctk.CTkFrame(body, fg_color="transparent")
        cc_grid.pack(fill="x")
        cc_grid.grid_columnconfigure((0, 1), weight=1, uniform="apc_cc")

        ctk.CTkLabel(cc_grid, text="min_samples_leaf", font=ctk.CTkFont(size=11),
                    text_color="#6C757D").grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(cc_grid, placeholder_text="e.g. 5", height=28
                    ).grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(0, 6))

        ctk.CTkLabel(cc_grid, text="ccp_alpha", font=ctk.CTkFont(size=11),
                    text_color="#6C757D").grid(row=0, column=1, sticky="w")
        ctk.CTkEntry(cc_grid, placeholder_text="e.g. 0.01", height=28
                    ).grid(row=1, column=1, sticky="ew", pady=(0, 6))

    # ── MPC section ───────────────────────────────────────────────────
    def _build_mpc_section(self, parent):
        _, body = self._make_collapsible(
            parent,
            "MPC — Mixed Predictive Confidence",
            "Combine IPC and APC scores into a single confidence signal",
            "#6A3FA0"
        )

        ctk.CTkLabel(body, text="Combination Strategy",
                    font=ctk.CTkFont(size=11, weight="bold"), text_color="#495057"
                    ).pack(anchor="w", pady=(4, 4))

        self.mpc_strategy_var = ctk.StringVar(value="average")

        ctk.CTkRadioButton(body, text="Average  — mean(IPC, APC)",
                        font=ctk.CTkFont(size=11), variable=self.mpc_strategy_var,
                        value="average", command=self._toggle_mpc_custom
                        ).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(body, text="Minimum  — min(IPC, APC)",
                        font=ctk.CTkFont(size=11), variable=self.mpc_strategy_var,
                        value="minimum", command=self._toggle_mpc_custom
                        ).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(body, text="Custom function",
                        font=ctk.CTkFont(size=11), variable=self.mpc_strategy_var,
                        value="custom", command=self._toggle_mpc_custom
                        ).pack(anchor="w", pady=(2, 4))

        self.mpc_custom_frame = ctk.CTkFrame(body, fg_color="transparent")
        ctk.CTkLabel(self.mpc_custom_frame, text="f(IPC, APC) =",
                    font=ctk.CTkFont(size=11), text_color="#6C757D"
                    ).pack(anchor="w")
        self.mpc_custom_entry = ctk.CTkEntry(
            self.mpc_custom_frame,
            placeholder_text="e.g.  0.6 * IPC + 0.4 * APC",
            height=30
        )
        self.mpc_custom_entry.pack(fill="x", pady=(2, 4))
        # hidden by default (custom not selected)

    def _toggle_mpc_custom(self):
        if self.mpc_strategy_var.get() == "custom":
            self.mpc_custom_frame.pack(fill="x", padx=0, pady=(0, 4))
        else:
            self.mpc_custom_frame.pack_forget()

    # ── Step bar ──────────────────────────────────────────────────────
    def draw_step_bar(self):
        sb_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        sb_frame.pack(fill="x", pady=(0, 20))
        steps = [("1", "Upload data", "active"), ("2", "Configure model", "todo"), ("3", "Review results", "todo"), ("4", "Set threshold", "todo"), ("5", "Deploy", "todo")]
        for idx, (num, name, state) in enumerate(steps):
            sf = ctk.CTkFrame(sb_frame, fg_color="transparent")
            sf.pack(side="left", fill="y")
            dot = ctk.CTkLabel(sf, text=num, width=24, height=24, corner_radius=12, fg_color="#185FA5" if state == "active" else "#E9ECEF", text_color="#FFFFFF" if state == "active" else "#6C757D", font=ctk.CTkFont(size=11, weight="bold"))
            dot.pack(side="left", padx=(0, 6))
            ctk.CTkLabel(sf, text=name, text_color="#212529" if state == "active" else "#6C757D", font=ctk.CTkFont(size=12, weight="bold" if state == "active" else "normal")).pack(side="left")
            if idx < len(steps) - 1:
                ctk.CTkFrame(sb_frame, height=1, fg_color="#E9ECEF", width=40).pack(side="left", fill="x", expand=True, padx=10)

# ====================================================================
# TAB 3: MDR CURVES / RESULTS
# ====================================================================
class ResultsReviewView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        self.metric_data = {
            "AUC": {
            "title": "AUC improvement",
            "value": "+5.1%",
            "subtext": "▲ At DR = 93%",
            "optimal_dr": 93
        },
        "Sensitivity": {
            "title": "Sensitivity improvement",
            "value": "+4.3%",
            "subtext": "▲ At DR = 85%",
            "optimal_dr": 85
        },
        "Specificity": {
            "title": "Specificity improvement",
            "value": "+6.8%",
            "subtext": "▲ At DR = 70%",
            "optimal_dr": 70
        },
        "NPV": {
            "title": "NPV improvement",
            "value": "+3.9%",
            "subtext": "▲ At DR = 75%",
            "optimal_dr": 75
        }

    }
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Analysis workspace", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="ICU in-hospital mortality · MIMIC-IV BaseModel", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        ctk.CTkButton(top_bar, text="▶ Run analysis", fg_color="#185FA5", hover_color="#124A80", text_color="#FFFFFF", width=120, height=34).pack(side="right", padx=5)
        ctk.CTkButton(top_bar, text="⬇ Export report", fg_color="#FFFFFF", border_color="#CED4DA", border_width=1, text_color="#495057", hover_color="#F8F9FA", width=120, height=34).pack(side="right", padx=5)

        self.draw_step_bar()

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        # List of metrics we can rotate through on Card 2
        self.available_metrics = ["AUC", "Sensitivity", "Specificity", "NPV"]
        self.current_metric_index = 0

        # Card 0: Static total count
        self.create_kpi(cards_frame, 0, "Patients analyzed", "4,476", "Evaluation set · MIMIC-IV", "#6C757D")

        # Card 1: Confident predictions (DR Card) - Save labels to update dynamically
        self.dr_val_lbl, self.dr_sub_lbl, self.dr_title_lbl= self.create_kpi(
            cards_frame, 1, "Confident predictions", "93%", "▲ Suggested declaration rate", "#0F6E56"
        )

        # Card 2: The Switchable Metric Card - Bind to rotation command
        # self.metric_title_lbl = ctk.CTkLabel(cards_frame, text="AUC improvement") # Split out title logic if needed, or update dynamically
        self.metric_val_lbl, self.metric_sub_lbl, self.metric_title_lbl = self.create_kpi(
            cards_frame, 2, "AUC improvement", "+5.1%", "▲ At DR = 93%", "#0F6E56", 
            command=self.cycle_metric
        )

        split_frame = ctk.CTkFrame(self, fg_color="transparent")
        split_frame.pack(fill="x", pady=(0, 20))
        split_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        chart_card = ctk.CTkFrame(split_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        chart_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(chart_card, text="📈 Metrics by declaration rate", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        self.embed_mdr_chart(chart_card)

        profile_card = ctk.CTkFrame(split_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        profile_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(profile_card, text="🌿 Confidence by patient profile", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        self.create_profile_row(profile_card, "BUN ≤ 25.5 mg/dL", 0.84, "#1D9E75")
        self.create_profile_row(profile_card, "GCS ≥ 10, Temp normal", 0.79, "#378ADD")
        self.create_profile_row(profile_card, "Age 40–65, no comorbidity", 0.71, "#378ADD")
        self.create_profile_row(profile_card, "BUN 25.5–30.8 mg/dL", 0.52, "#EF9F27")
        self.create_profile_row(profile_card, "GCS < 7.5, Temp > 38.1°C", 0.31, "#D85A30")
        ctk.CTkLabel(profile_card, text="Profiles generated by APC decision tree · depth 3", font=ctk.CTkFont(size=10), text_color="#9CA3AF").pack(anchor="w", padx=15, pady=(6, 10))
        
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        table_card.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(table_card, text="👤 Patient-level predictions", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        
        self.table_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        self.table_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.table_frame.grid_columnconfigure((0,1,2,3,4), weight=1, uniform="table")

        for idx, header in enumerate(["Patient", "BaseModel pred.", "MPC confidence", "Profile", "Recommendation"]):
            ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").grid(row=0, column=idx, sticky="w" if idx < 4 else "e", pady=5)

        self.add_pt_row(1, "Pt. 1", "Positive", "0.28", "BUN 25–31", "Reject", "#FAECE7", "#993C1D")
        self.add_pt_row(2, "Pt. 2", "Positive", "0.55", "GCS < 7.5", "Caution", "#FAEEDA", "#854F0B")
        self.add_pt_row(3, "Pt. 3", "Negative", "0.91", "BUN ≤ 25.5", "Accept", "#EAF3DE", "#3B6D11")

    def draw_step_bar(self):
        sb_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        sb_frame.pack(fill="x", pady=(0, 20))
        steps = [("✓", "Upload data", "done"), ("✓", "Configure model", "done"), ("3", "Review results", "active"), ("4", "Set threshold", "todo"), ("5", "Deploy", "todo")]
        for idx, (num, name, state) in enumerate(steps):
            sf = ctk.CTkFrame(sb_frame, fg_color="transparent")
            sf.pack(side="left", fill="y")
            dot_color = "#0F6E56" if state == "done" else ("#185FA5" if state == "active" else "#E9ECEF")
            ctk.CTkLabel(sf, text=num, width=24, height=24, corner_radius=12, fg_color=dot_color, text_color="#FFFFFF" if state in ["done", "active"] else "#6C757D", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(sf, text=name, text_color="#212529" if state == "active" else "#6C757D", font=ctk.CTkFont(size=12, weight="bold" if state == "active" else "normal")).pack(side="left")
            if idx < len(steps) - 1:
                ctk.CTkFrame(sb_frame, height=1, fg_color="#E9ECEF", width=40).pack(side="left", fill="x", expand=True, padx=10)

    def create_kpi(self, parent, col, title, value, sub, sub_color, command=None):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8, height=100)
        card.grid(row=0, column=col, padx=6, sticky="nsew")
        card.pack_propagate(False)

        title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="#6C757D")
        title_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        
        val_lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color="#212529")
        val_lbl.pack(anchor="w", padx=12)
        
        sub_lbl = ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=11), text_color=sub_color)
        sub_lbl.pack(anchor="w", padx=12, pady=(2, 8))
        if command:
            # Change cursor to hand to show clickability
            card.configure(cursor="hand2")
            # Bind the click action to the frame itself and all internal elements
            for widget in (card, title_lbl, val_lbl, sub_lbl):
                widget.bind("<Button-1>", lambda e: command())
            
    # Return references to the labels so we can change their text later
        return val_lbl, sub_lbl, title_lbl
    def cycle_metric(self):
        # 1. Advance to the next metric index
        self.current_metric_index = (self.current_metric_index + 1) % len(self.available_metrics)
        next_metric_name = self.available_metrics[self.current_metric_index]
        
        # 2. Extract configuration from state map
        config = self.metric_data[next_metric_name]
        target_dr = config["optimal_dr"]
        
        # 3. Update the Switchable Card UI elements
        self.metric_title_lbl.configure(text=config["title"])
        self.metric_val_lbl.configure(text=config["value"])
        self.metric_sub_lbl.configure(text=config["subtext"])
        
        # 4. Update the Dependent DR Card UI elements automatically
        self.dr_val_lbl.configure(text=f"{target_dr}%")
        self.dr_sub_lbl.configure(text=f"▲ Suggested DR for {next_metric_name}")
        
        # 5. Update the Matplotlib Dotted Line
        self.update_chart_line(target_dr)
    def update_chart_line(self, target_dr):
        # Remove previous lines to avoid stacking duplicates
        for line in list(self.ax_mdr.lines):
            if line.get_linestyle() == ':': # targets the dotted indicator line
                line.remove()
        
        # Draw new line using the string formatted match from your chart x-labels
        self.ax_mdr.axvline(x=target_dr, color="#185FA5", linestyle=":", linewidth=1.5)
        
        # Force the canvas interface widget to re-render visually
        self.canvas_mdr.draw()
    def create_profile_row(self, p, l, v, c):
        row = ctk.CTkFrame(p, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(row, text=l, font=ctk.CTkFont(size=12), text_color="#495057").pack(side="top", anchor="w")
        bar_f = ctk.CTkFrame(row, fg_color="transparent")
        bar_f.pack(side="bottom", fill="x", pady=(2, 0))
        p_bar = ctk.CTkProgressBar(bar_f, height=8, progress_color=c, fg_color="#E9ECEF")
        p_bar.set(v)
        p_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(bar_f, text=f"{v:.2f}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#212529").pack(side="right")

    def add_pt_row(self, r, pt, b, m, p, rec, bg, tc):
        f = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        f.grid(row=r, column=0, sticky="w", pady=6)
        ctk.CTkLabel(f, text=pt[:2], width=26, height=26, corner_radius=13, fg_color="#B5D4F4", text_color="#0C447C", font=ctk.CTkFont(size=10, weight="bold")).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(f, text=pt, text_color="#495057", font=ctk.CTkFont(size=13)).pack(side="left")
        ctk.CTkLabel(self.table_frame, text=b, text_color="#993C1D" if b == "Positive" else "#3B6D11", font=ctk.CTkFont(size=13)).grid(row=r, column=1, sticky="w")
        ctk.CTkLabel(self.table_frame, text=m, text_color="#212529", font=ctk.CTkFont(size=13)).grid(row=r, column=2, sticky="w")
        ctk.CTkLabel(self.table_frame, text=p, text_color="#6C757D", font=ctk.CTkFont(size=12)).grid(row=r, column=3, sticky="w")
        ctk.CTkLabel(self.table_frame, text=rec, width=65, height=20, corner_radius=10, fg_color=bg, text_color=tc, font=ctk.CTkFont(size=11, weight="bold")).grid(row=r, column=4, sticky="e")

    def embed_mdr_chart(self, parent):
        # Keep arrays as pure numeric data
        self.dr_vals = [50, 60, 70, 75, 80, 85, 90, 93, 95, 97, 100]
        auc = [0.60, 0.65, 0.71, 0.74, 0.76, 0.78, 0.79, 0.80, 0.78, 0.77, 0.76]
        sens = [0.48, 0.55, 0.63, 0.67, 0.70, 0.74, 0.76, 0.78, 0.73, 0.70, 0.68]
        spec = [0.98, 0.96, 0.92, 0.89, 0.86, 0.82, 0.78, 0.76, 0.75, 0.75, 0.74]
        npv = [0.98, 0.97, 0.95, 0.94, 0.93, 0.92, 0.90, 0.89, 0.87, 0.86, 0.85]
        
        # Bind figure and axes to self so they can be accessed anywhere in the class
        self.fig_mdr, self.ax_mdr = plt.subplots(figsize=(4.5, 2.5), dpi=100)
        self.fig_mdr.patch.set_facecolor('#FFFFFF')
        self.ax_mdr.set_facecolor('#FFFFFF')
        
        # Plot using numeric data for X-axis instead of string array x_labels
        self.ax_mdr.plot(self.dr_vals, auc, color='#378ADD', label='AUC', linewidth=2)
        self.ax_mdr.plot(self.dr_vals, sens, color='#1D9E75', label='Sensitivity', linewidth=2)
        self.ax_mdr.plot(self.dr_vals, spec, color='#BA7517', label='Specificity', linewidth=1.5, linestyle='--')
        self.ax_mdr.plot(self.dr_vals, npv, color='#D85A30', label='NPV', linewidth=1.5, linestyle='--')
        
        # Place initial line using numeric value 93
        self.ax_mdr.axvline(x=93, color="#185FA5", linestyle=":", linewidth=1.5)
        
        # Set explicitly numeric boundaries and labels
        self.ax_mdr.set_xlim(50, 100)
        self.ax_mdr.set_ylim(0.4, 1.0)
        self.ax_mdr.set_xticks(self.dr_vals)
        self.ax_mdr.set_xticklabels([f"{v}%" for v in self.dr_vals])
        
        self.ax_mdr.tick_params(axis='both', which='major', labelsize=8, colors='#888780')
        self.ax_mdr.grid(True, color='#888780', alpha=0.15, linestyle='-')
        
        for spine in ['top', 'right', 'left', 'bottom']: 
            self.ax_mdr.spines[spine].set_visible(False)
            
        self.ax_mdr.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=4, frameon=False, fontsize=7)
        self.fig_mdr.tight_layout()
        
        # Save a reference to the canvas object wrapper as well
        self.canvas_mdr = FigureCanvasTkAgg(self.fig_mdr, master=parent)
        self.canvas_mdr.draw()
        self.canvas_mdr.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 5))

# ====================================================================
# TAB 4: PATIENT PROFILES (Interactive Dashboard Mod)
# ====================================================================
class ProfilesView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
        self.current_dr = 93.0  # Track initial slider state

        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Patient Profiles", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="APC Decision Tree Subgroups & Live Thresholding", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")
        ctk.CTkButton(top_bar, text="▶ Save Threshold", fg_color="#185FA5", hover_color="#124A80", text_color="#FFFFFF", width=120, height=34).pack(side="right", padx=5)
        
        self.draw_step_bar()

        # Dynamic Threshold Controller Card
        slider_card = ctk.CTkFrame(self, fg_color="#F8F9FA", border_color="#E9ECEF", border_width=1, corner_radius=8)
        slider_card.pack(fill="x", pady=(0, 20))
        
        self.slider_label = ctk.CTkLabel(slider_card, text=f"🎯 Active Declaration Rate (DR) Threshold: {int(self.current_dr)}%", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5")
        self.slider_label.pack(anchor="w", padx=15, pady=(10, 2))
        
        self.slider_dr = ctk.CTkSlider(slider_card, from_=50, to=100, number_of_steps=50, height=16, command=self.on_slider_move)
        self.slider_dr.set(self.current_dr)
        self.slider_dr.pack(fill="x", padx=15, pady=(2, 12))
        
        # Split layout container
        split_frame = ctk.CTkFrame(self, fg_color="transparent")
        split_frame.pack(fill="x", pady=(0, 20))
        split_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        chart_card = ctk.CTkFrame(split_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        chart_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(chart_card, text="📈 Dynamic Metrics Window", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        
        # Init plots
        self.fig_mdr, self.ax_mdr = plt.subplots(figsize=(4.5, 2.8), dpi=100)
        self.canvas_mdr = FigureCanvasTkAgg(self.fig_mdr, master=chart_card)
        self.canvas_mdr.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 5))

        tree_card = ctk.CTkFrame(split_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        tree_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(tree_card, text="🌿 APC Hierarchical Decision Tree (Fades when DR drops)", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        
        self.fig_tree, self.ax_tree = plt.subplots(figsize=(4.5, 2.8), dpi=100)
        self.canvas_tree = FigureCanvasTkAgg(self.fig_tree, master=tree_card)
        self.canvas_tree.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 5))
        # Initial Render
        self.draw_mdr()
        self.draw_tree()

    def on_slider_move(self, value):
        self.current_dr = float(value)
        self.slider_label.configure(text=f"🎯 Active Declaration Rate (DR) Threshold: {int(self.current_dr)}%")
        if hasattr(self, 'cbar') and self.cbar is not None:
            try:
                self.cbar.remove()
            except Exception:
                pass
        self.cbar = None
        self.ax_tree.set_subplotspec(plt.GridSpec(1, 1)[0, 0])
        self.ax_tree.set_position(self.ax_tree.get_subplotspec().get_position(self.fig_tree))
        self.draw_mdr()
        self.draw_tree()
        

    def draw_mdr(self):
            self.ax_mdr.clear()
            self.fig_mdr.patch.set_facecolor('#FFFFFF')
            self.ax_mdr.set_facecolor('#FFFFFF')
            
            dr_vals = [50, 60, 70, 75, 80, 85, 90, 93, 95, 97, 100]
            auc = [0.60, 0.65, 0.71, 0.74, 0.76, 0.78, 0.79, 0.80, 0.78, 0.77, 0.76]
            sens = [0.48, 0.55, 0.63, 0.67, 0.70, 0.74, 0.76, 0.78, 0.73, 0.70, 0.68]
            spec = [0.98, 0.96, 0.92, 0.89, 0.86, 0.82, 0.78, 0.76, 0.75, 0.75, 0.74]
            npv = [0.98, 0.97, 0.95, 0.94, 0.93, 0.92, 0.90, 0.89, 0.87, 0.86, 0.85]
            
            self.ax_mdr.plot(dr_vals, auc, color='#378ADD', label='AUC', linewidth=2)
            self.ax_mdr.plot(dr_vals, sens, color='#1D9E75', label='Sensitivity', linewidth=2)
            self.ax_mdr.plot(dr_vals, spec, color='#BA7517', label='Specificity', linewidth=1.5, linestyle='--')
            self.ax_mdr.plot(dr_vals, npv, color='#D85A30', label='NPV', linewidth=1.5, linestyle='--')
            
            # Line location synced directly to slider coordinate state
            self.ax_mdr.axvline(x=self.current_dr, color="#185FA5", linestyle=":", linewidth=2)
            
            # Shift the bottom spine (x-axis) up to y=0.4 to create an empty area below
            self.ax_mdr.spines['bottom'].set_position(('data', 0.4))
            self.ax_mdr.set_ylim(0.20, 1.0) # Extend y-axis downwards to 0.20 for the bar
            self.ax_mdr.set_yticks([0.4, 0.6, 0.8, 1.0]) # Keep ticks only on the main chart
            
            # Draw the secondary timeline axis line
            self.ax_mdr.hlines(y=0.30, xmin=50, xmax=100, color='#E9ECEF', linewidth=4, zorder=1)
            
            # Points where nodes drop (Node A, Node B1, Node B2)
            drop_pts = [60, 78, 92]
            drop_labels = ["Node A Fades", "Node B1 Fades", "Node B2 Fades"]
            drop_colors = ['#1D9E75', '#185FA5', '#D85A30'] # Matches tree node colors
            
            # Plot timeline points and labels
            self.ax_mdr.scatter(drop_pts, [0.30]*3, color=drop_colors, s=40, zorder=5)
            for pt, label, color in zip(drop_pts, drop_labels, drop_colors):
                self.ax_mdr.text(pt, 0.26, label, ha='center', va='top', fontsize=7, color=color, weight='bold')

            self.ax_mdr.set_xlim(50, 100)
            self.ax_mdr.set_xticks(dr_vals)
            self.ax_mdr.set_xticklabels([f"{v}%" for v in dr_vals])
            self.ax_mdr.tick_params(axis='both', which='major', labelsize=8, colors='#888780')
            self.ax_mdr.grid(True, color='#888780', alpha=0.15, linestyle='-')
            
            for spine in ['top', 'right', 'left']: self.ax_mdr.spines[spine].set_visible(False)
            
            # Move the legend to the top so it doesn't overlap the new timeline bar
            self.ax_mdr.legend(loc='lower left', bbox_to_anchor=(-.2, 1.02), ncol=4, frameon=False, fontsize=7)
            # self.fig_mdr.tight_layout()
            self.canvas_mdr.draw()

    def draw_tree(self):
        self.ax_tree.clear()
        self.fig_tree.patch.set_facecolor('#FFFFFF')
        self.ax_tree.set_facecolor('#FFFFFF')
        self.ax_tree.axis('off')
        self.ax_tree.set_xlim(0, 100)
        self.ax_tree.set_ylim(0, 100)

        # Base structure styles
        box_root = dict(boxstyle="round,pad=0.4",facecolor="#F8F9FA",edgecolor="#FFD700",lw=1.5)
        box_green = dict(boxstyle="round,pad=0.4", facecolor="#EAF3DE", edgecolor="#1D9E75", lw=1)
        box_grey = dict(boxstyle="round,pad=0.4", facecolor="#F2F4F4", edgecolor="#A9A9A9", lw=1, alpha=0.2)
        box_orange = dict(boxstyle="round,pad=0.4", facecolor="#FAECE7", edgecolor="#D85A30", lw=1)
        arrow_style = dict(arrowstyle="->", color="#ADB5BD", lw=1.5)

        # Dynamic visibility checkpoints configured against DR
        show_node_a = self.current_dr >= 60.0
        show_node_b1 = self.current_dr >= 78.0
        show_node_b2 = self.current_dr >= 92.0

        # Layer 1: Root Node (Always visible)
        self.ax_tree.text(50, 88, f"All Cohorts\nDR = {int(self.current_dr)}%\nAUC: 0.80", ha='center', va='center', size=8, bbox=box_root)

        # Layer 2: Node A
        if show_node_a:
            self.ax_tree.text(25, 54, "Node A\nBUN ≤ 25.5\nSize: 1,240 pts\nConf: High", ha='center', va='center', size=7, bbox=box_green)
            self.ax_tree.annotate("", xy=(25, 65), xytext=(45, 80), arrowprops=arrow_style)
            self.ax_tree.text(31, 74, "True", size=7, color="#1D9E75", weight="bold")
        else:
            self.ax_tree.text(25, 54, "Node A\nBUN ≤ 25.5\nSize: 1,240 pts\nConf: High", ha='center', va='center', size=7, bbox=box_grey, alpha=0.2)
            self.ax_tree.annotate("", xy=(25, 65), xytext=(45, 80), arrowprops=arrow_style)
            self.ax_tree.text(31, 74, "True", size=7, color="#A9A9A9", weight="bold", alpha=0.2)

        # Layer 2: Node B (Always visible)
        self.ax_tree.text(75, 54, "Node B\nBUN > 25.5\nSize: 3,236 pts\nConf: Evaluate", ha='center', va='center', size=7, bbox=box_root)
        self.ax_tree.annotate("", xy=(75, 65), xytext=(55, 80), arrowprops=arrow_style)
        self.ax_tree.text(64, 74, "False", size=7, color="#D85A30", weight="bold")

        # Layer 3: Terminal Children from Node B
        if show_node_b1:
            self.ax_tree.text(60, 18, "Node B1\nGCS ≥ 10\nSize: 2,145 pts\nConf: Mod", ha='center', va='center', size=7, bbox=box_root)
            self.ax_tree.annotate("", xy=(60, 30), xytext=(70, 44), arrowprops=arrow_style)
        else:
            self.ax_tree.text(60, 18, "Node B1\nGCS ≥ 10\nSize: 2,145 pts\nConf: Mod", ha='center', va='center', size=7, bbox=box_grey,alpha=.2)
            self.ax_tree.annotate("", xy=(60, 30), xytext=(70, 44), arrowprops=arrow_style)

        if show_node_b2:
            self.ax_tree.text(90, 18, "Node B2\nGCS < 7.5\nSize: 1,091 pts\nConf: Low", ha='center', va='center', size=7, bbox=box_orange)
            self.ax_tree.annotate("", xy=(90, 30), xytext=(80, 44), arrowprops=arrow_style)
        else:
            self.ax_tree.text(90, 18, "Node B2\nGCS < 7.5\nSize: 1,091 pts\nConf: Low", ha='center', va='center', size=7, bbox=box_grey,alpha=0.2)
            self.ax_tree.annotate("", xy=(90, 30), xytext=(80, 44), arrowprops=arrow_style)

        sm = plt.cm.ScalarMappable(cmap=cm.RdYlGn, norm=plt.Normalize(vmin=0, vmax=1))
        sm.set_array([])

        self.cbar = plt.colorbar(sm, ax=self.ax_tree, shrink=0.6)

        self.cbar.set_label("APC Confidence", fontsize=8)
        self.cbar.ax.tick_params(labelsize=7)
        self.cbar.outline.set_edgecolor('#E9ECEF')

        self.fig_tree.tight_layout()
        self.canvas_tree.draw()

    def draw_step_bar(self):
        sb_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        sb_frame.pack(fill="x", pady=(0, 20))
        steps = [("✓", "Upload data", "done"), ("✓", "Configure model", "done"), ("✓", "Review results", "done"), ("4", "Set threshold", "active"), ("5", "Deploy", "todo")]
        for idx, (num, name, state) in enumerate(steps):
            sf = ctk.CTkFrame(sb_frame, fg_color="transparent")
            sf.pack(side="left", fill="y")
            dot_color = "#0F6E56" if state == "done" else ("#185FA5" if state == "active" else "#E9ECEF")
            ctk.CTkLabel(sf, text=num, width=24, height=24, corner_radius=12, fg_color=dot_color, text_color="#FFFFFF" if state in ["done", "active"] else "#6C757D", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(sf, text=name, text_color="#212529" if state == "active" else "#6C757D", font=ctk.CTkFont(size=12, weight="bold" if state == "active" else "normal")).pack(side="left")
            if idx < len(steps) - 1:
                ctk.CTkFrame(sb_frame, height=1, fg_color="#E9ECEF", width=40).pack(side="left", fill="x", expand=True, padx=10)


# ====================================================================
# TAB 5: RUN MODEL LAYOUT (Mock Execution Space)
# ====================================================================
import customtkinter as ctk
from tkinter import filedialog

class RunModelView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Run Live Inference Pipeline", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Real-time validation tracking using BaseModel + MED3pa Confidence verification", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 20))
        grid_frame.grid_columnconfigure(0, weight=2, uniform="run_split")
        grid_frame.grid_columnconfigure(1, weight=3, uniform="run_split")

        # LEFT SIDE: CONTROL CONTROLLER CARD
        left_col = ctk.CTkFrame(grid_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        left_col.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(left_col, text="⚡ Pipeline Configurations", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=12)
        
        ctk.CTkLabel(left_col, text="Select Base Model", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15)
        ctk.CTkComboBox(left_col, values=[
            "Breast Cancer Histopathology CNN Classifier",
            "Lung Nodule Malignancy Prediction Model",
            "Colorectal Cancer Risk Stratification Engine",
            "Skin Lesion Melanoma Detection Network",
            "Prostate Cancer Gleason Score Predictor",
            "Multi-Omics Tumor Classification Model",
            "Radiogenomic Cancer Detection Pipeline",
            "Early Pancreatic Cancer Screening Predictor"
        ], width=280, height=32).pack(anchor="w", padx=15, pady=(2, 12))
        
        ctk.CTkLabel(left_col, text="Deployment Validation Profile", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15)
        ctk.CTkComboBox(left_col, values=["Base Logistics Ensemble [Threshold = 93%]", "Hippo-EHR Transformers [Threshold = 85%]"], width=280, height=32).pack(anchor="w", padx=15, pady=(2, 15))

        c1 = ctk.CTkCheckBox(left_col, text="Inject real-time fallback route alerts", font=ctk.CTkFont(size=12))
        c1.pack(anchor="w", padx=15, pady=6)
        c1.select()
        
        c2 = ctk.CTkCheckBox(left_col, text="Log predictions to global lookup database", font=ctk.CTkFont(size=12))
        c2.pack(anchor="w", padx=15, pady=6)
        c2.select()

        # ctk.CTkButton(left_col, text="▶ Initiate Inference Stream", fg_color="#0F6E56", hover_color="#0A4D3C", text_color="#FFFFFF", height=38, font=ctk.CTkFont(weight="bold")).pack(fill="x", padx=15, pady=(25, 15))

        # RIGHT SIDE: STREAM PREVIEW MONITOR
        right_col = ctk.CTkFrame(grid_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        right_col.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        ctk.CTkLabel(right_col, text="📺 Active Inference Feed Preview", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=10)
        
        table_frame = ctk.CTkFrame(right_col, fg_color="transparent")
        table_frame.pack(fill="x", padx=15, pady=10)
        table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="live_table")

        headers = ["Patient ID", "Base Model Risk", "MED3pa Trust", "Routing Status"]
        for idx, h in enumerate(headers):
            ctk.CTkLabel(table_frame, text=h, font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").grid(row=0, column=idx, sticky="w" if idx < 3 else "e", pady=5)

        self.add_mock_row(table_frame, 1, "PT-0841", "88% Positive", "0.94 (High)", "Accept Prediction", "#EAF3DE", "#3B6D11")
        self.add_mock_row(table_frame, 2, "PT-1940", "64% Positive", "0.31 (Low)", "Flag for Human Audit", "#FAECE7", "#993C1D")
        self.add_mock_row(table_frame, 3, "PT-3329", "12% Negative", "0.89 (High)", "Accept Prediction", "#EAF3DE", "#3B6D11")
        self.add_mock_row(table_frame, 4, "PT-5511", "71% Positive", "0.55 (Mod)", "Caution / Flag", "#FAEEDA", "#854F0B")

        # BOTTOM SECTION: PATIENT DATA INPUT
        self.setup_data_input_section()

    def add_mock_row(self, parent, r, pid, risk, trust, status, bg, tc):
        ctk.CTkLabel(parent, text=pid, font=ctk.CTkFont(size=12, weight="bold"), text_color="#212529").grid(row=r, column=0, sticky="w", pady=6)
        ctk.CTkLabel(parent, text=risk, font=ctk.CTkFont(size=12), text_color="#495057").grid(row=r, column=1, sticky="w", pady=6)
        ctk.CTkLabel(parent, text=trust, font=ctk.CTkFont(size=12), text_color="#495057").grid(row=r, column=2, sticky="w", pady=6)
        ctk.CTkLabel(parent, text=status, width=110, height=20, corner_radius=10, fg_color=bg, text_color=tc, font=ctk.CTkFont(size=10, weight="bold")).grid(row=r, column=3, sticky="e", pady=6)

    def setup_data_input_section(self):
        input_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        input_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(input_frame, text="📝 Patient Data Input", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=(12, 5))
        
        # Tabs for Batch vs Single Input
        self.tabs = ctk.CTkTabview(input_frame, fg_color="#F8F9FA", segmented_button_selected_color="#0F6E56", segmented_button_selected_hover_color="#0A4D3C", height=350)
        self.tabs.pack(fill="x", padx=15, pady=(0, 15))
        
        self.tabs.add("Batch Processing (CSV)")
        self.tabs.add("Single Patient (Manual Entry)")
        
        # --- BATCH TAB ---
        batch_tab = self.tabs.tab("Batch Processing (CSV)")
        ctk.CTkLabel(batch_tab, text="Select a CSV file containing structured patient data for batch model inference.", font=ctk.CTkFont(size=12), text_color="#495057").pack(anchor="w", padx=10, pady=(15, 10))
        
        csv_control_frame = ctk.CTkFrame(batch_tab, fg_color="transparent")
        csv_control_frame.pack(fill="x", padx=10, pady=5)
        
        self.csv_path_var = ctk.StringVar(value="No file selected...")
        ctk.CTkButton(csv_control_frame, text="📂 Browse CSV...", command=self.select_csv_file, width=140, fg_color="#495057", hover_color="#343A40").pack(side="left", padx=(0, 15))
        ctk.CTkLabel(csv_control_frame, textvariable=self.csv_path_var, font=ctk.CTkFont(size=12, slant="italic"), text_color="#6C757D").pack(side="left")

        ctk.CTkButton(batch_tab, text="Run Batch Inference", fg_color="#0F6E56", hover_color="#0A4D3C", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=30)

        # --- SINGLE PATIENT TAB ---
        manual_tab = self.tabs.tab("Single Patient (Manual Entry)")
        
        fields = [
            "stay_id", "hospitalid", "deceased", "age", "bicarbonate_min", "bicarbonate_max",
            "bilirubin_min", "bilirubin_max", "potassium_min", "potassium_max", "sodium_min",
            "sodium_max", "bun_min", "bun_max", "wbc_min", "wbc_max", "pao2fio2", "cpap",
            "vent", "gcs_min", "hr_min", "hr_max", "tempc_min", "tempc_max", "sbp_min",
            "sbp_max", "uo", "aids", "hem", "mets", "admissiontype"
        ]

        grid_container = ctk.CTkFrame(manual_tab, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure 5 equal columns for density
        for i in range(5):
            grid_container.grid_columnconfigure(i, weight=1, uniform="input_col")

        self.patient_entries = {}
        for idx, field in enumerate(fields):
            row = (idx // 5) * 2
            col = idx % 5
            
            # Format label string elegantly
            lbl_text = field.replace("_", " ").title() + ":"
            
            ctk.CTkLabel(grid_container, text=lbl_text, font=ctk.CTkFont(size=11, weight="bold"), text_color="#495057").grid(row=row, column=col, sticky="w", padx=5, pady=(5, 0))
            
            ent = ctk.CTkEntry(grid_container, height=28)
            ent.grid(row=row+1, column=col, sticky="ew", padx=5, pady=(0, 5))
            self.patient_entries[field] = ent

        btn_frame = ctk.CTkFrame(manual_tab, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        ctk.CTkButton(btn_frame, text="▶ Run Single Inference", fg_color="#0F6E56", hover_color="#0A4D3C", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)
        ctk.CTkButton(btn_frame, text="Clear Fields", fg_color="transparent", text_color="#D9534F", border_width=1, border_color="#D9534F", hover_color="#FDF2F2").pack(side="right", padx=10)

    def select_csv_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Patient Data CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filepath:
            self.csv_path_var.set(filepath)

# ====================================================================
# TAB 6: PATIENT LOOKUP
# ====================================================================
class LookupView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Patient Lookup", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Query individual clinical predictions", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Patient ID (e.g., PT-9482)", width=300, height=36)
        self.search_entry.pack(side="left", padx=(0, 10))
        ctk.CTkButton(search_frame, text="Search", fg_color="#185FA5", text_color="#FFFFFF", width=80, height=36).pack(side="left")

        result_card = ctk.CTkFrame(self, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        result_card.pack(fill="x", pady=10)
        
        header = ctk.CTkFrame(result_card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="PT-9482", font=ctk.CTkFont(size=20, weight="bold"), text_color="#212529").pack(side="left")
        ctk.CTkLabel(header, text="Admitted: 2026-05-18", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(side="right")

        details = ctk.CTkFrame(result_card, fg_color="transparent")
        details.pack(fill="x", padx=20, pady=(0, 20))
        details.grid_columnconfigure((0,1,2), weight=1)

        self.add_detail(details, 0, "Base Model Prediction", "Positive", "#993C1D")
        self.add_detail(details, 1, "MPC Confidence", "0.28 (Low)", "#993C1D")
        self.add_detail(details, 2, "Action Recommendation", "Reject (Manual Review)", "#993C1D")

    def add_detail(self, parent, col, title, val, color):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=0, column=col, sticky="w")
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")
        ctk.CTkLabel(f, text=val, font=ctk.CTkFont(size=14, weight="bold"), text_color=color).pack(anchor="w")


# ====================================================================
# TAB 7: SESSION HISTORY
# ====================================================================
class HistoryView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Session History", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Log of previous pipeline executions", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        table_card.pack(fill="x", pady=10)
        
        table_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        table_frame.pack(fill="x", padx=15, pady=15)
        table_frame.grid_columnconfigure((0,1,2,3), weight=1, uniform="hist")

        for idx, header in enumerate(["Date", "Target Model", "Dataset", "Status"]):
            ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(size=12, weight="bold"), text_color="#6C757D").grid(row=0, column=idx, sticky="w", pady=(0, 10))

        history = [
            ("2026-05-19 08:14", "ICU Mortality Base", "mimic_iv_eval.csv", "Completed"),
            ("2026-05-17 14:22", "Septic Shock Onset", "cohort_b_q2.parquet", "Completed"),
            ("2026-05-15 09:05", "Readmission Index", "local_extract.xlsx", "Failed (Missing Cols)")
        ]

        for i, (date, model, data, status) in enumerate(history, start=1):
            color = "#3B6D11" if "Completed" in status else "#993C1D"
            ctk.CTkLabel(table_frame, text=date, font=ctk.CTkFont(size=12), text_color="#212529").grid(row=i, column=0, sticky="w", pady=6)
            ctk.CTkLabel(table_frame, text=model, font=ctk.CTkFont(size=12), text_color="#495057").grid(row=i, column=1, sticky="w", pady=6)
            ctk.CTkLabel(table_frame, text=data, font=ctk.CTkFont(size=12), text_color="#495057").grid(row=i, column=2, sticky="w", pady=6)
            ctk.CTkLabel(table_frame, text=status, font=ctk.CTkFont(size=12, weight="bold"), text_color=color).grid(row=i, column=3, sticky="w", pady=6)


if __name__ == "__main__":
    app = MED3paApp()
    app.mainloop()