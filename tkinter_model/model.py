import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image

# Set application styling
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class MED3paApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MED3pa Workspace")
        self.geometry("1150x800")
        self.configure(fg_color="#FFFFFF")

        def on_closing(self):
        # Gracefully kill all background Matplotlib figures so the terminal doesn't freeze
            try:
                plt.close('all')
            except Exception:
                pass
                
            self.quit()     # Stops the Tcl background mainloop safely
            self.destroy()  # Deletes the widgets and frees up memory cleanly
            
        # Configure Grid Layout for Main Window
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.nav_buttons = {}
        self.frames = {}

        # ----------------------------------------------------
        # SIDEBAR NAVIGATION
        # ----------------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#F8F9FA", border_color="#E9ECEF", border_width=1)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Load the logo image
        logo_image = ctk.CTkImage(
            light_image=Image.open(r"C:\Users\thanh\Documents\Work\MEDomics\med3pa\tkinter_model\MEDomicsLabWithShadow700.png"),
            dark_image=Image.open(r"C:\Users\thanh\Documents\Work\MEDomics\med3pa\tkinter_model\MEDomicsLabWithShadow700.png"),
            size=(32, 32)  # Adjust size as needed
        )

        # Header frame to hold image + text + badge side by side
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(pady=(20, 20), padx=20, anchor="w")

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
        self.create_nav_item("Run MED3pa") # Decorative for now
        self.create_nav_item("MDR curves", target_frame="ResultsView")
        self.create_nav_item("Patient profiles", target_frame="ProfilesView")
        
        self.create_nav_header("Clinical Use")
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
        self.frames["LookupView"] = LookupView(parent=self, controller=self)
        self.frames["HistoryView"] = HistoryView(parent=self, controller=self)

        # Default to Overview
        self.show_frame("OverviewView")

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
        
        # Match the frame name back to the button text for highlighting
        frame_to_btn = {
            "OverviewView": "Overview", "UploadView": "Upload data", 
            "ResultsView": "MDR curves", "ProfilesView": "Patient profiles",
            "LookupView": "Patient lookup", "HistoryView": "Session history"
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
        
        # Top Bar
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Workspace Overview", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="System status and recent activity", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        # KPI Grid
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.create_kpi(cards_frame, 0, "Active Models Deployments", "3", "Running normally", "#0F6E56")
        self.create_kpi(cards_frame, 1, "Total Patients Scanned", "12,845", "Last 30 days", "#6C757D")
        self.create_kpi(cards_frame, 2, "System Alerts", "0", "No active warnings", "#6C757D")

        # Recent Activity Section
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
# TAB 2: UPLOAD & CONFIGURATION (Existing)
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

        # LEFT SIDE
        left_col = ctk.CTkFrame(grid_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        self.upload_zone = ctk.CTkFrame(left_col, fg_color="#F8F9FA", border_color="#CED4DA", border_width=1, corner_radius=8, height=180)
        self.upload_zone.pack(fill="x", pady=(0, 15))
        self.upload_zone.pack_propagate(False)
        ctk.CTkLabel(self.upload_zone, text="📁", font=ctk.CTkFont(size=32)).pack(pady=(25, 2))
        self.lbl_file_status = ctk.CTkLabel(self.upload_zone, text="Drag & drop cohort data here, or click to browse", font=ctk.CTkFont(size=13, weight="bold"), text_color="#495057")
        self.lbl_file_status.pack()
        ctk.CTkLabel(self.upload_zone, text="Supports CSV, PARQUET, or EHR extraction sheets (Max 50MB)", font=ctk.CTkFont(size=11), text_color="#6C757D").pack(pady=(2, 10))
        self.upload_zone.bind("<Button-1>", lambda e: self.trigger_file_browser())

        model_card = ctk.CTkFrame(left_col, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        model_card.pack(fill="x")
        ctk.CTkLabel(model_card, text="🤖 Select Baseline Prediction Model", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=12)
        ctk.CTkLabel(model_card, text="Base Model Source Architecture", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15)
        ctk.CTkComboBox(model_card, values=["MIMIC-IV Base Logistics Ensemble", "Hippo-EHR Transformers v4", "Custom Local XGBoost Checkpoint"], width=320, height=32).pack(anchor="w", padx=15, pady=(2, 12))
        ctk.CTkLabel(model_card, text="Target Target Classification Label", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15)
        ctk.CTkComboBox(model_card, values=["In-Hospital Mortality Risk Factor", "30-Day Readmission Diagnostic Index", "Septic Shock Onset Threshold"], width=320, height=32).pack(anchor="w", padx=15, pady=(2, 15))

        # RIGHT SIDE
        right_col = ctk.CTkFrame(grid_frame, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
        right_col.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(right_col, text="⚙️ Execution Parameters", font=ctk.CTkFont(size=13, weight="bold"), text_color="#185FA5").pack(anchor="w", padx=15, pady=12)
        ctk.CTkLabel(right_col, text="APC Decision Tree Depth", font=ctk.CTkFont(size=12), text_color="#495057").pack(anchor="w", padx=15, pady=(5, 0))
        slider_depth = ctk.CTkSlider(right_col, from_=1, to=10, number_of_steps=9, height=16)
        slider_depth.set(3)
        slider_depth.pack(fill="x", padx=15, pady=2)
        
        c1 = ctk.CTkCheckBox(right_col, text="Cross-validate internal cohorts (5-Fold Split)", font=ctk.CTkFont(size=12))
        c1.pack(anchor="w", padx=15, pady=8)
        c1.select()
        c2 = ctk.CTkCheckBox(right_col, text="Impute missing baseline BUN & GCS parameters", font=ctk.CTkFont(size=12))
        c2.pack(anchor="w", padx=15, pady=8)
        c2.select()
        ctk.CTkCheckBox(right_col, text="Generate SynthID verification Watermarks", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=8)

        ctk.CTkButton(right_col, text="⚡ Run Pipeline Execution", fg_color="#0F6E56", hover_color="#0A4D3C", text_color="#FFFFFF", height=40, font=ctk.CTkFont(weight="bold"), command=lambda: controller.show_frame("ResultsView")).pack(fill="x", padx=15, pady=(30, 15))

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

    def trigger_file_browser(self):
        path = filedialog.askopenfilename(filetypes=[("Data Matrices", "*.csv *.parquet *.xlsx")])
        if path:
            self.lbl_file_status.configure(text=f"Loaded: {path.split('/')[-1]}", text_color="#0F6E56")


# ====================================================================
# TAB 3: MDR CURVES / RESULTS (Existing + Fixes applied)
# ====================================================================
class ResultsReviewView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
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
        self.create_kpi(cards_frame, 0, "Patients analyzed", "4,476", "Evaluation set · MIMIC-IV", "#6C757D")
        self.create_kpi(cards_frame, 1, "Confident predictions", "93%", "▲ Suggested declaration rate", "#0F6E56")
        self.create_kpi(cards_frame, 2, "AUC improvement", "+5.1%", "▲ At DR = 93%", "#0F6E56")

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

    def create_kpi(self, p, col, l, v, d, c):
        card = ctk.CTkFrame(p, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8, height=100)
        card.grid(row=0, column=col, padx=6, sticky="nsew")
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=l, font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(card, text=v, font=ctk.CTkFont(size=24, weight="bold"), text_color="#212529").pack(anchor="w", padx=12)
        ctk.CTkLabel(card, text=d, font=ctk.CTkFont(size=11), text_color=c).pack(anchor="w", padx=12, pady=(2, 8))

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
        dr, auc, sens, spec, npv = [100, 97, 95, 93, 90, 85, 80, 75, 70, 60, 50], [0.76, 0.77, 0.78, 0.80, 0.79, 0.78, 0.76, 0.74, 0.71, 0.65, 0.60], [0.68, 0.70, 0.73, 0.78, 0.76, 0.74, 0.70, 0.67, 0.63, 0.55, 0.48], [0.74, 0.75, 0.75, 0.76, 0.78, 0.82, 0.86, 0.89, 0.92, 0.96, 0.98], [0.85, 0.86, 0.87, 0.89, 0.90, 0.92, 0.93, 0.94, 0.95, 0.97, 0.98]
        fig, ax = plt.subplots(figsize=(4.5, 2.5), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FFFFFF')
        x_labels = [f"{v}%" for v in dr]
        ax.plot(x_labels, auc, color='#378ADD', label='AUC', linewidth=2)
        ax.plot(x_labels, sens, color='#1D9E75', label='Sensitivity', linewidth=2)
        ax.plot(x_labels, spec, color='#BA7517', label='Specificity', linewidth=1.5, linestyle='--')
        ax.plot(x_labels, npv, color='#D85A30', label='NPV', linewidth=1.5, linestyle='--')
        ax.axvline(x="93%", color="#185FA5", linestyle=":", linewidth=1.5)
        ax.set_ylim(0.4, 1.0)
        ax.tick_params(axis='both', which='major', labelsize=8, colors='#888780')
        ax.grid(True, color='#888780', alpha=0.15, linestyle='-')
        for spine in ['top', 'right', 'left', 'bottom']: ax.spines[spine].set_visible(False)
        ax.legend(loc='lower left', bbox_to_anchor=(0, -0.1), ncol=4, frameon=False, fontsize=7)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 5))


# ====================================================================
# TAB 4: PATIENT PROFILES
# ====================================================================
class ProfilesView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top_bar.pack(fill="x", pady=(15, 15))
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        ctk.CTkLabel(title_frame, text="Patient Profiles", font=ctk.CTkFont(size=18, weight="bold"), text_color="#212529").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="APC Decision Tree Subgroups", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w")

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        # Mock Profiles generated from decision tree logic
        profiles = [
            ("Profile Node A", "BUN ≤ 25.5 mg/dL", "1,240 pts", "High Confidence", "#1D9E75"),
            ("Profile Node B", "GCS ≥ 10, Temp normal", "890 pts", "High Confidence", "#378ADD"),
            ("Profile Node C", "Age 40–65, no comorbidity", "750 pts", "Moderate Confidence", "#378ADD"),
            ("Profile Node D", "BUN 25.5–30.8 mg/dL", "420 pts", "Low Confidence", "#EF9F27"),
        ]

        for i, (title, crit, count, conf, color) in enumerate(profiles):
            card = ctk.CTkFrame(grid, fg_color="#FFFFFF", border_color="#E9ECEF", border_width=1, corner_radius=8)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color="#212529").pack(anchor="w", padx=15, pady=(15, 5))
            ctk.CTkLabel(card, text=f"Criteria: {crit}", font=ctk.CTkFont(size=12), text_color="#495057").pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=f"Cohort size: {count}", font=ctk.CTkFont(size=12), text_color="#6C757D").pack(anchor="w", padx=15, pady=(2, 10))
            badge = ctk.CTkLabel(card, text=conf, fg_color=color, text_color="#FFFFFF", corner_radius=10, font=ctk.CTkFont(size=11, weight="bold"), height=22)
            badge.pack(anchor="w", padx=15, pady=(0, 15))


# ====================================================================
# TAB 5: PATIENT LOOKUP
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

        # Search Box
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Patient ID (e.g., PT-9482)", width=300, height=36)
        self.search_entry.pack(side="left", padx=(0, 10))
        ctk.CTkButton(search_frame, text="Search", fg_color="#185FA5", text_color="#FFFFFF", width=80, height=36).pack(side="left")

        # Dummy Result Card
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
# TAB 6: SESSION HISTORY
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