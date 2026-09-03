import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import csv
import os
import webbrowser
from io import BytesIO

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ============================================================
# PRODUCT SCOPE PRO
# NEXT-LEVEL STANDALONE PRODUCT SCRAPER
# Python 3.14 Compatible
# ============================================================


class ProductScraperPro:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "ProductScope Pro — Product Intelligence"
        )

        self.root.geometry(
            "1280x820"
        )

        self.root.minsize(
            1050,
            700
        )

        self.dark_mode = True

        self.products = []

        self.filtered_products = []

        self.image_cache = {}

        self.is_scraping = False

        self.colors = self.get_dark_colors()

        self.setup_styles()

        self.create_variables()

        self.create_interface()

        self.update_clock()

    # ========================================================
    # COLORS
    # ========================================================

    def get_dark_colors(self):

        return {
            "bg": "#080C18",
            "panel": "#10172A",
            "panel2": "#151E35",
            "input": "#1A2440",
            "primary": "#6C63FF",
            "primary_hover": "#827AFF",
            "secondary": "#202B49",
            "text": "#F4F7FF",
            "muted": "#8C98B8",
            "success": "#45E0A8",
            "danger": "#FF5D73",
            "warning": "#FFCA5C",
            "border": "#273354",
            "card": "#121B30"
        }

    def get_light_colors(self):

        return {
            "bg": "#EEF2F8",
            "panel": "#FFFFFF",
            "panel2": "#F4F6FB",
            "input": "#E8ECF5",
            "primary": "#5B50E8",
            "primary_hover": "#7066F5",
            "secondary": "#DDE3F0",
            "text": "#182033",
            "muted": "#66718A",
            "success": "#13A879",
            "danger": "#E63D58",
            "warning": "#D89500",
            "border": "#D4DBEA",
            "card": "#FFFFFF"
        }

    # ========================================================
    # VARIABLES
    # ========================================================

    def create_variables(self):

        self.url_var = tk.StringVar()

        self.search_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="Ready • Add product URLs to begin"
        )

        self.count_var = tk.StringVar(
            value="0"
        )

        self.success_var = tk.StringVar(
            value="0"
        )

        self.failed_var = tk.StringVar(
            value="0"
        )

        self.theme_var = tk.StringVar(
            value="☀ Light Mode"
        )

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            rowheight=38,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )

        style.configure(
            "Horizontal.TProgressbar",
            thickness=7
        )

    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def create_interface(self):

        self.root.configure(
            bg=self.colors["bg"]
        )

        # Main
        self.main = tk.Frame(
            self.root,
            bg=self.colors["bg"]
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        self.create_header()

        self.create_body()

        self.create_status_bar()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        self.header = tk.Frame(
            self.main,
            bg=self.colors["panel"],
            height=92
        )

        self.header.pack(
            fill="x"
        )

        self.header.pack_propagate(False)

        # Logo
        self.logo = tk.Label(
            self.header,
            text="◈",
            font=("Segoe UI", 30, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["panel"]
        )

        self.logo.pack(
            side="left",
            padx=(28, 12)
        )

        title_frame = tk.Frame(
            self.header,
            bg=self.colors["panel"]
        )

        title_frame.pack(
            side="left",
            pady=13
        )

        self.title_label = tk.Label(
            title_frame,
            text="ProductScope Pro",
            font=("Segoe UI", 21, "bold"),
            fg=self.colors["text"],
            bg=self.colors["panel"]
        )

        self.title_label.pack(
            anchor="w"
        )

        self.subtitle_label = tk.Label(
            title_frame,
            text="Product Intelligence • Scrape • Compare • Export",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["panel"]
        )

        self.subtitle_label.pack(
            anchor="w"
        )

        # Right side
        right = tk.Frame(
            self.header,
            bg=self.colors["panel"]
        )

        right.pack(
            side="right",
            padx=25
        )

        self.theme_button = tk.Button(
            right,
            textvariable=self.theme_var,
            command=self.toggle_theme,
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            activebackground=self.colors["primary"],
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        self.theme_button.pack(
            side="right",
            padx=(10, 0)
        )

        # Product counter
        counter = tk.Frame(
            right,
            bg=self.colors["panel2"]
        )

        counter.pack(
            side="right"
        )

        self.counter_number = tk.Label(
            counter,
            textvariable=self.count_var,
            font=("Segoe UI", 17, "bold"),
            fg=self.colors["success"],
            bg=self.colors["panel2"]
        )

        self.counter_number.pack(
            padx=16,
            pady=(6, 0)
        )

        self.counter_text = tk.Label(
            counter,
            text="PRODUCTS",
            font=("Segoe UI", 7, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["panel2"]
        )

        self.counter_text.pack(
            padx=16,
            pady=(0, 6)
        )

    # ========================================================
    # BODY
    # ========================================================

    def create_body(self):

        self.body = tk.Frame(
            self.main,
            bg=self.colors["bg"]
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=18
        )

        self.create_input_panel()

        self.create_statistics()

        self.create_search_toolbar()

        self.create_results()

    # ========================================================
    # INPUT PANEL
    # ========================================================

    def create_input_panel(self):

        self.input_panel = tk.Frame(
            self.body,
            bg=self.colors["panel"]
        )

        self.input_panel.pack(
            fill="x",
            pady=(0, 12)
        )

        label = tk.Label(
            self.input_panel,
            text="PRODUCT URLS",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["panel"]
        )

        label.pack(
            anchor="w",
            padx=18,
            pady=(13, 5)
        )

        row = tk.Frame(
            self.input_panel,
            bg=self.colors["panel"]
        )

        row.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        self.url_entry = tk.Entry(
            row,
            textvariable=self.url_var,
            font=("Segoe UI", 10),
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            bd=0
        )

        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 8)
        )

        self.add_button = self.make_button(
            row,
            "＋ ADD URL",
            self.add_url,
            self.colors["secondary"]
        )

        self.add_button.pack(
            side="left",
            padx=4
        )

        self.scrape_button = self.make_button(
            row,
            "⚡ SCRAPE ALL",
            self.start_scraping,
            self.colors["primary"]
        )

        self.scrape_button.pack(
            side="left",
            padx=(4, 0)
        )

        self.url_entry.bind(
            "<Return>",
            lambda event: self.add_url()
        )

        # URL list
        self.url_list_frame = tk.Frame(
            self.input_panel,
            bg=self.colors["panel2"]
        )

        self.url_list_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 14)
        )

        self.url_list_label = tk.Label(
            self.url_list_frame,
            text="No URLs added",
            font=("Segoe UI", 8),
            fg=self.colors["muted"],
            bg=self.colors["panel2"],
            anchor="w"
        )

        self.url_list_label.pack(
            fill="x",
            padx=10,
            pady=8
        )

        self.pending_urls = []

    # ========================================================
    # STATISTICS
    # ========================================================

    def create_statistics(self):

        stats = tk.Frame(
            self.body,
            bg=self.colors["bg"]
        )

        stats.pack(
            fill="x",
            pady=(0, 12)
        )

        self.create_stat_card(
            stats,
            "TOTAL PRODUCTS",
            self.count_var,
            self.colors["primary"]
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 7)
        )

        self.create_stat_card(
            stats,
            "SUCCESSFUL",
            self.success_var,
            self.colors["success"]
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        self.create_stat_card(
            stats,
            "FAILED",
            self.failed_var,
            self.colors["danger"]
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        self.create_stat_card(
            stats,
            "STATUS",
            self.status_var,
            self.colors["warning"]
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(7, 0)
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        title,
        variable,
        accent
    ):

        card = tk.Frame(
            parent,
            bg=self.colors["panel"],
            height=68
        )

        card.pack_propagate(False)

        line = tk.Frame(
            card,
            bg=accent,
            width=4
        )

        line.pack(
            side="left",
            fill="y"
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 7, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["panel"]
        )

        title_label.pack(
            anchor="w",
            padx=12,
            pady=(10, 1)
        )

        value_label = tk.Label(
            card,
            textvariable=variable,
            font=("Segoe UI", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["panel"],
            anchor="w"
        )

        value_label.pack(
            anchor="w",
            padx=12
        )

        return card

    # ========================================================
    # SEARCH TOOLBAR
    # ========================================================

    def create_search_toolbar(self):

        toolbar = tk.Frame(
            self.body,
            bg=self.colors["bg"]
        )

        toolbar.pack(
            fill="x",
            pady=(0, 10)
        )

        search_label = tk.Label(
            toolbar,
            text="🔎",
            font=("Segoe UI", 13),
            fg=self.colors["muted"],
            bg=self.colors["bg"]
        )

        search_label.pack(
            side="left",
            padx=(0, 6)
        )

        self.search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 9),
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            width=35
        )

        self.search_entry.pack(
            side="left",
            ipady=8
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.filter_products()
        )

        sort_button = self.make_button(
            toolbar,
            "↕ PRICE SORT",
            self.sort_by_price,
            self.colors["secondary"]
        )

        sort_button.pack(
            side="left",
            padx=8
        )

        copy_button = self.make_button(
            toolbar,
            "▣ COPY",
            self.copy_selected,
            self.colors["secondary"]
        )

        copy_button.pack(
            side="left",
            padx=3
        )

        delete_button = self.make_button(
            toolbar,
            "✕ DELETE",
            self.delete_selected,
            self.colors["secondary"]
        )

        delete_button.pack(
            side="left",
            padx=3
        )

        clear_button = self.make_button(
            toolbar,
            "CLEAR ALL",
            self.clear_all,
            self.colors["secondary"]
        )

        clear_button.pack(
            side="left",
            padx=3
        )

        excel_button = self.make_button(
            toolbar,
            "▣ EXCEL",
            self.export_excel,
            self.colors["success"]
        )

        excel_button.pack(
            side="right",
            padx=(4, 0)
        )

        csv_button = self.make_button(
            toolbar,
            "⇩ CSV",
            self.export_csv,
            self.colors["primary"]
        )

        csv_button.pack(
            side="right"
        )

    # ========================================================
    # RESULTS
    # ========================================================

    def create_results(self):

        self.results_panel = tk.Frame(
            self.body,
            bg=self.colors["panel"]
        )

        self.results_panel.pack(
            fill="both",
            expand=True
        )

        top = tk.Frame(
            self.results_panel,
            bg=self.colors["panel"]
        )

        top.pack(
            fill="x"
        )

        label = tk.Label(
            top,
            text="PRODUCT INTELLIGENCE",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["panel"]
        )

        label.pack(
            side="left",
            padx=17,
            pady=12
        )

        self.open_button = self.make_button(
            top,
            "↗ OPEN WEBSITE",
            self.open_selected_url,
            self.colors["secondary"]
        )

        self.open_button.pack(
            side="right",
            padx=15,
            pady=7
        )

        # Table
        table_frame = tk.Frame(
            self.results_panel,
            bg=self.colors["panel"]
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        columns = (
            "title",
            "price",
            "rating",
            "description",
            "image",
            "url"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "title": "PRODUCT",
            "price": "PRICE",
            "rating": "RATING",
            "description": "DESCRIPTION",
            "image": "IMAGE",
            "url": "SOURCE"
        }

        for column, heading in headings.items():

            self.tree.heading(
                column,
                text=heading
            )

        self.tree.column(
            "title",
            width=220,
            minwidth=150
        )

        self.tree.column(
            "price",
            width=110,
            minwidth=90,
            anchor="center"
        )

        self.tree.column(
            "rating",
            width=90,
            minwidth=70,
            anchor="center"
        )

        self.tree.column(
            "description",
            width=350,
            minwidth=200
        )

        self.tree.column(
            "image",
            width=250,
            minwidth=150
        )

        self.tree.column(
            "url",
            width=250,
            minwidth=150
        )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.pack(
            side="top",
            fill="both",
            expand=True
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.open_selected_url()
        )

    # ========================================================
    # STATUS BAR
    # ========================================================

    def create_status_bar(self):

        self.status_bar = tk.Frame(
            self.main,
            bg=self.colors["panel"],
            height=38
        )

        self.status_bar.pack(
            fill="x",
            side="bottom"
        )

        self.status_bar.pack_propagate(False)

        self.status_dot = tk.Label(
            self.status_bar,
            text="●",
            fg=self.colors["success"],
            bg=self.colors["panel"],
            font=("Segoe UI", 8)
        )

        self.status_dot.pack(
            side="left",
            padx=(18, 5)
        )

        self.status_text = tk.Label(
            self.status_bar,
            textvariable=self.status_var,
            fg=self.colors["muted"],
            bg=self.colors["panel"],
            font=("Segoe UI", 8)
        )

        self.status_text.pack(
            side="left"
        )

        self.clock_label = tk.Label(
            self.status_bar,
            fg=self.colors["muted"],
            bg=self.colors["panel"],
            font=("Segoe UI", 8)
        )

        self.clock_label.pack(
            side="right",
            padx=18
        )

        self.progress = ttk.Progressbar(
            self.status_bar,
            mode="determinate",
            length=180
        )

        self.progress.pack(
            side="right",
            padx=10
        )

    # ========================================================
    # BUTTON
    # ========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        bg
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 8, "bold"),
            bg=bg,
            fg=self.colors["text"],
            activebackground=self.colors["primary_hover"],
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7
        )

    # ========================================================
    # ADD URL
    # ========================================================

    def add_url(self):

        url = self.url_var.get().strip()

        if not url:

            return

        if not url.startswith(
            ("http://", "https://")
        ):

            messagebox.showwarning(
                "Invalid URL",
                "Please enter a URL beginning with http:// or https://"
            )

            return

        if url in self.pending_urls:

            messagebox.showinfo(
                "Duplicate URL",
                "This URL has already been added."
            )

            return

        self.pending_urls.append(
            url
        )

        self.url_var.set("")

        self.update_url_display()

        self.status_var.set(
            f"{len(self.pending_urls)} URL(s) waiting to be scraped"
        )

    # ========================================================
    # URL DISPLAY
    # ========================================================

    def update_url_display(self):

        if not self.pending_urls:

            self.url_list_label.config(
                text="No URLs added"
            )

            return

        if len(self.pending_urls) <= 3:

            text = "  •  ".join(
                self.pending_urls
            )

        else:

            text = (
                "  •  ".join(
                    self.pending_urls[:3]
                )
                + f"  •  +{len(self.pending_urls)-3} more"
            )

        self.url_list_label.config(
            text=text
        )

    # ========================================================
    # START SCRAPING
    # ========================================================

    def start_scraping(self):

        if self.is_scraping:

            return

        if not self.pending_urls:

            url = self.url_var.get().strip()

            if url:

                self.add_url()

            else:

                messagebox.showinfo(
                    "No URLs",
                    "Add one or more product URLs first."
                )

                return

        self.is_scraping = True

        self.scrape_button.config(
            state="disabled",
            text="⏳ SCRAPING..."
        )

        self.progress["value"] = 0

        self.success_var.set("0")

        self.failed_var.set("0")

        urls = self.pending_urls.copy()

        self.pending_urls.clear()

        self.update_url_display()

        thread = threading.Thread(
            target=self.scrape_all,
            args=(urls,),
            daemon=True
        )

        thread.start()

    # ========================================================
    # SCRAPE ALL
    # ========================================================

    def scrape_all(self, urls):

        total = len(urls)

        success = 0

        failed = 0

        for index, url in enumerate(urls):

            self.root.after(
                0,
                lambda i=index, t=total:
                self.update_progress(i, t)
            )

            try:

                product = self.scrape_product(
                    url
                )

                if product:

                    success += 1

                    self.root.after(
                        0,
                        lambda p=product:
                        self.add_product(p)
                    )

            except Exception as e:

                failed += 1

                print(
                    f"Scraping failed: {url}"
                )

                print(e)

        self.root.after(
            0,
            lambda:
            self.scraping_finished(
                success,
                failed
            )
        )

    # ========================================================
    # SCRAPE PRODUCT
    # ========================================================

    def scrape_product(self, url):

        headers = {

            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0 Safari/537.36",

            "Accept-Language":
                "en-US,en;q=0.9"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = self.extract_title(
            soup
        )

        price = self.extract_price(
            soup
        )

        rating = self.extract_rating(
            soup
        )

        description = self.extract_description(
            soup
        )

        image = self.extract_image(
            soup,
            url
        )

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "description": description,
            "image": image,
            "url": url
        }

    # ========================================================
    # TITLE
    # ========================================================

    def extract_title(self, soup):

        selectors = [

            "[itemprop='name']",

            "meta[property='og:title']",

            "#productTitle",

            ".product-title",

            ".product_name",

            ".product-name",

            "h1"
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if element:

                if element.name == "meta":

                    text = element.get(
                        "content",
                        ""
                    )

                else:

                    text = element.get_text(
                        " ",
                        strip=True
                    )

                if text:

                    return text[:250]

        if soup.title:

            return soup.title.get_text(
                " ",
                strip=True
            )[:250]

        return "Not found"

    # ========================================================
    # PRICE
    # ========================================================

    def extract_price(self, soup):

        # Schema price
        element = soup.select_one(
            "[itemprop='price']"
        )

        if element:

            value = (
                element.get("content")
                or element.get_text(
                    " ",
                    strip=True
                )
            )

            if value:

                return self.clean_price(
                    value
                )

        selectors = [

            ".price",

            ".product-price",

            ".product_price",

            ".sale-price",

            ".current-price",

            ".offer-price",

            "#priceblock_ourprice",

            "#priceblock_dealprice"
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if element:

                text = element.get_text(
                    " ",
                    strip=True
                )

                if text:

                    return self.clean_price(
                        text
                    )

        # Search text
        text = soup.get_text(
            " ",
            strip=True
        )

        patterns = [

            r"₹\s?[\d,]+(?:\.\d+)?",

            r"\$\s?[\d,]+(?:\.\d+)?",

            r"€\s?[\d,]+(?:\.\d+)?",

            r"£\s?[\d,]+(?:\.\d+)?"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                return match.group(0)

        return "Not found"

    # ========================================================
    # CLEAN PRICE
    # ========================================================

    def clean_price(self, text):

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        match = re.search(
            r"(₹|\$|€|£)?\s?[\d,]+(?:\.\d+)?",
            text
        )

        if match:

            return match.group(0)

        return text[:50]

    # ========================================================
    # RATING
    # ========================================================

    def extract_rating(self, soup):

        selectors = [

            "[itemprop='ratingValue']",

            ".rating",

            ".product-rating",

            ".review-rating",

            ".stars",

            ".a-icon-alt"
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if element:

                text = (
                    element.get(
                        "content",
                        ""
                    )
                    or
                    element.get_text(
                        " ",
                        strip=True
                    )
                )

                match = re.search(
                    r"\d+(?:\.\d+)?",
                    text
                )

                if match:

                    return match.group(0)

        return "N/A"

    # ========================================================
    # DESCRIPTION
    # ========================================================

    def extract_description(self, soup):

        meta = soup.find(
            "meta",
            attrs={
                "name": "description"
            }
        )

        if meta:

            content = meta.get(
                "content",
                ""
            )

            if content:

                return self.clean_description(
                    content
                )

        selectors = [

            "[itemprop='description']",

            ".product-description",

            ".product_description",

            "#productDescription",

            ".description"
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if element:

                text = element.get_text(
                    " ",
                    strip=True
                )

                if text:

                    return self.clean_description(
                        text
                    )

        return "Not found"

    # ========================================================
    # CLEAN DESCRIPTION
    # ========================================================

    def clean_description(self, text):

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        if len(text) > 350:

            text = (
                text[:347]
                + "..."
            )

        return text

    # ========================================================
    # IMAGE
    # ========================================================

    def extract_image(
        self,
        soup,
        base_url
    ):

        selectors = [

            "meta[property='og:image']",

            "[itemprop='image']",

            "#landingImage",

            "#imgBlkFront",

            ".product-image img",

            ".product-img img",

            ".product-image",

            "img"
        ]

        for selector in selectors:

            element = soup.select_one(
                selector
            )

            if element:

                src = (

                    element.get(
                        "content"
                    )

                    or

                    element.get(
                        "src"
                    )

                    or

                    element.get(
                        "data-src"
                    )

                )

                if src:

                    return urljoin(
                        base_url,
                        src
                    )

        return "Not found"

    # ========================================================
    # ADD PRODUCT
    # ========================================================

    def add_product(self, product):

        self.products.append(
            product
        )

        self.filtered_products = (
            self.products.copy()
        )

        self.refresh_table()

        self.count_var.set(
            str(len(self.products))
        )

    # ========================================================
    # REFRESH TABLE
    # ========================================================

    def refresh_table(self):

        for item in self.tree.get_children():

            self.tree.delete(
                item
            )

        for product in self.filtered_products:

            self.tree.insert(
                "",
                "end",
                values=(

                    product["title"],

                    product["price"],

                    product["rating"],

                    product["description"],

                    product["image"],

                    product["url"]
                )
            )

    # ========================================================
    # FILTER
    # ========================================================

    def filter_products(self):

        query = self.search_var.get().lower().strip()

        if not query:

            self.filtered_products = (
                self.products.copy()
            )

        else:

            self.filtered_products = [

                product

                for product in self.products

                if query in
                product["title"].lower()

                or

                query in
                product["description"].lower()

                or

                query in
                product["price"].lower()
            ]

        self.refresh_table()

    # ========================================================
    # SORT
    # ========================================================

    def sort_by_price(self):

        def price_value(product):

            text = product["price"]

            numbers = re.sub(
                r"[^\d.]",
                "",
                text.replace(",", "")
            )

            try:

                return float(
                    numbers
                )

            except:

                return float(
                    "inf"
                )

        self.filtered_products.sort(
            key=price_value
        )

        self.refresh_table()

        self.status_var.set(
            "Products sorted by price"
        )

    # ========================================================
    # UPDATE PROGRESS
    # ========================================================

    def update_progress(
        self,
        index,
        total
    ):

        percentage = (
            index / total
        ) * 100

        self.progress["value"] = (
            percentage
        )

        self.status_var.set(
            f"Scraping product {index + 1} of {total}..."
        )

    # ========================================================
    # FINISHED
    # ========================================================

    def scraping_finished(
        self,
        success,
        failed
    ):

        self.progress["value"] = 100

        self.success_var.set(
            str(success)
        )

        self.failed_var.set(
            str(failed)
        )

        self.is_scraping = False

        self.scrape_button.config(
            state="normal",
            text="⚡ SCRAPE ALL"
        )

        self.status_var.set(
            f"Completed • {success} successful • {failed} failed"
        )

    # ========================================================
    # SELECTED PRODUCT
    # ========================================================

    def get_selected_product(self):

        selected = self.tree.selection()

        if not selected:

            return None

        item = selected[0]

        values = self.tree.item(
            item,
            "values"
        )

        if not values:

            return None

        url = values[5]

        for product in self.products:

            if product["url"] == url:

                return product

        return None

    # ========================================================
    # COPY
    # ========================================================

    def copy_selected(self):

        product = (
            self.get_selected_product()
        )

        if not product:

            messagebox.showinfo(
                "Select Product",
                "Please select a product first."
            )

            return

        text = (

            f"PRODUCT\n"
            f"{product['title']}\n\n"

            f"PRICE\n"
            f"{product['price']}\n\n"

            f"RATING\n"
            f"{product['rating']}\n\n"

            f"DESCRIPTION\n"
            f"{product['description']}\n\n"

            f"IMAGE\n"
            f"{product['image']}\n\n"

            f"SOURCE\n"
            f"{product['url']}"
        )

        self.root.clipboard_clear()

        self.root.clipboard_append(
            text
        )

        self.status_var.set(
            "Product information copied"
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_selected(self):

        product = (
            self.get_selected_product()
        )

        if not product:

            messagebox.showinfo(
                "Select Product",
                "Please select a product first."
            )

            return

        self.products.remove(
            product
        )

        self.filter_products()

        self.count_var.set(
            str(len(self.products))
        )

        self.status_var.set(
            "Product removed"
        )

    # ========================================================
    # CLEAR ALL
    # ========================================================

    def clear_all(self):

        if not self.products:

            return

        answer = messagebox.askyesno(
            "Clear Products",
            "Remove all scraped products?"
        )

        if not answer:

            return

        self.products.clear()

        self.filtered_products.clear()

        self.refresh_table()

        self.count_var.set(
            "0"
        )

        self.success_var.set(
            "0"
        )

        self.failed_var.set(
            "0"
        )

        self.status_var.set(
            "All products cleared"
        )

    # ========================================================
    # OPEN WEBSITE
    # ========================================================

    def open_selected_url(self):

        product = (
            self.get_selected_product()
        )

        if not product:

            messagebox.showinfo(
                "Select Product",
                "Select a product first."
            )

            return

        webbrowser.open(
            product["url"]
        )

    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv(self):

        if not self.products:

            messagebox.showinfo(
                "No Data",
                "There are no products to export."
            )

            return

        path = filedialog.asksaveasfilename(

            title="Export Products",

            defaultextension=".csv",

            filetypes=[
                (
                    "CSV files",
                    "*.csv"
                )
            ],

            initialfile="products.csv"
        )

        if not path:

            return

        try:

            with open(
                path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "title",
                        "price",
                        "rating",
                        "description",
                        "image",
                        "url"
                    ]
                )

                writer.writeheader()

                writer.writerows(
                    self.products
                )

            self.status_var.set(
                "CSV exported successfully"
            )

            messagebox.showinfo(
                "Export Complete",
                "CSV file created successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

    # ========================================================
    # EXPORT EXCEL
    # ========================================================

    def export_excel(self):

        if not self.products:

            messagebox.showinfo(
                "No Data",
                "There are no products to export."
            )

            return

        try:

            from openpyxl import Workbook

        except ImportError:

            messagebox.showerror(
                "Missing Package",
                "Install openpyxl first:\n\n"
                "pip install openpyxl"
            )

            return

        path = filedialog.asksaveasfilename(

            title="Export Excel",

            defaultextension=".xlsx",

            filetypes=[
                (
                    "Excel files",
                    "*.xlsx"
                )
            ],

            initialfile="products.xlsx"
        )

        if not path:

            return

        try:

            workbook = Workbook()

            sheet = workbook.active

            sheet.title = "Products"

            headers = [

                "Product",

                "Price",

                "Rating",

                "Description",

                "Image URL",

                "Source URL"
            ]

            sheet.append(
                headers
            )

            for product in self.products:

                sheet.append([

                    product["title"],

                    product["price"],

                    product["rating"],

                    product["description"],

                    product["image"],

                    product["url"]
                ])

            # Adjust columns
            widths = [
                35,
                15,
                12,
                60,
                55,
                55
            ]

            for index, width in enumerate(
                widths,
                start=1
            ):

                sheet.column_dimensions[
                    chr(64 + index)
                ].width = width

            workbook.save(
                path
            )

            self.status_var.set(
                "Excel file exported successfully"
            )

            messagebox.showinfo(
                "Export Complete",
                "Excel file created successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Excel Error",
                str(e)
            )

    # ========================================================
    # THEME
    # ========================================================

    def toggle_theme(self):

        self.dark_mode = (
            not self.dark_mode
        )

        if self.dark_mode:

            self.colors = (
                self.get_dark_colors()
            )

            self.theme_var.set(
                "☀ Light Mode"
            )

        else:

            self.colors = (
                self.get_light_colors()
            )

            self.theme_var.set(
                "☾ Dark Mode"
            )

        self.rebuild_interface()

    # ========================================================
    # REBUILD THEME
    # ========================================================

    def rebuild_interface(self):

        # Save important data
        products = self.products.copy()

        pending = self.pending_urls.copy()

        search = self.search_var.get()

        # Remove UI
        for widget in self.root.winfo_children():

            widget.destroy()

        # Recreate
        self.setup_styles()

        self.create_variables()

        self.products = products

        self.filtered_products = (
            products.copy()
        )

        self.pending_urls = pending

        self.search_var.set(
            search
        )

        self.create_interface()

        self.refresh_table()

        self.count_var.set(
            str(len(self.products))
        )

        self.update_url_display()

    # ========================================================
    # CLOCK
    # ========================================================

    def update_clock(self):

        from datetime import datetime

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.clock_label.config(
            text=current_time
        )

        self.root.after(
            1000,
            self.update_clock
        )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ProductScraperPro(
        root
    )

    root.mainloop()