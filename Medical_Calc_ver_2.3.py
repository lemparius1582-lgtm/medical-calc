import tkinter as tk
import tkinter.font as tkfont
import webbrowser
import json
import os
import re
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tkcalendar import Calendar

# ============================================================
# КОНСТАНТЫ
# ============================================================
# код картинки - логотипа. 
LOGO_BASE64 = "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"

# код QR-кода

QR_BASE64 = "ТУТ_БЫЛ_QR_КОД_АВТОРА"

DONATION_URL = "https://pay.cloudtips.ru/p/61064256"
# Ссылки для блока "Обновления и связь"
YANDEX_DISK_FILE = "https://disk.yandex.ru/d/MfIWdGoYsam6qA"
YANDEX_DISK_FOLDER = "https://disk.yandex.ru/d/O-fXEJZTPFi2ew"
GITHUB_REPO = "https://github.com/lemparius1582-lgtm/medical-calc"
GITHUB_DISCUSSIONS = "https://github.com/lemparius1582-lgtm/medical-calc/discussions"


SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".medical_calc_settings.json")

# Системные темы ttk. Ключ — как показываем в UI, значение — системное имя.
# Если тема недоступна на текущей ОС, она автоматически отфильтруется.
NATIVE_THEMES = {
    "Windows (системная)":        "vista",
    "Windows классическая":       "winnative",
    "Кроссплатформенная светлая": "clam",
    "Серая минималистичная":      "alt",
    "Системная тёмная":           "xpnative",
}

DEFAULT_THEME_NAME = "Windows (системная)"


# ============================================================
# УТИЛИТЫ
# ============================================================

def pluralize(number, titles):
    cases = [2, 0, 1, 1, 1, 2]
    return f"{number} {titles[2 if (number % 100 > 4 and number % 100 < 20) else cases[min(number % 10, 5)]]}"


def make_copyable(label, get_text_fn=None):
    def on_click(event):
        text = get_text_fn() if get_text_fn else label.cget("text")
        if not text or not text.strip():
            return
        label.clipboard_clear()
        label.clipboard_append(text)
        original_cursor = label.cget("cursor") if "cursor" in label.keys() else ""
        label.config(cursor="hand2")
        label.after(150, lambda: label.config(cursor=original_cursor))

    label.bind("<Button-1>", on_click)
    label.configure(cursor="hand2")
    return label


# ============================================================
# КОМПОНЕНТ: DateInput — три поля ДД . ММ . ГГГГ
# ============================================================

class DateInput(ttk.Frame):
    def __init__(self, parent, initial=None, **kw):
        super().__init__(parent, **kw)
        self.d = ttk.Entry(self, width=4,) # justify="center")
        self.m = ttk.Entry(self, width=4,) # justify="center")
        self.y = ttk.Entry(self, width=6,) #justify="center")

        self.d.pack(side="left")
        ttk.Label(self, text=".").pack(side="left")
        self.m.pack(side="left")
        ttk.Label(self, text=".").pack(side="left")
        self.y.pack(side="left")

        for w in (self.d, self.m, self.y):
            w.bind("<KeyRelease>", self._on_key)
            w.bind("<<Paste>>", self._on_paste)
            w.bind("<FocusIn>", self._on_focus_in)

        self.d.bind("<Tab>", lambda e: (self.m.focus_set(), "break")[1])
        self.m.bind("<Tab>", lambda e: (self.y.focus_set(), "break")[1])
        self.y.bind("<Tab>", lambda e: "break")

        if initial is not None:
            self.set_date(initial)
        else:
            self.set_date(datetime.today().date())

    def _on_focus_in(self, event):
        """При фокусе: если поле не пустое — выделяем всё,
        чтобы новая цифра заменила старое значение."""
        w = event.widget
        if w.get():
            w.select_range(0, tk.END)
            w.icursor(tk.END)

    def _on_key(self, event):
        w = event.widget

        # Backspace: если поле пустое — уходим назад
        if event.keysym == "BackSpace":
            if not w.get():
                if w is self.m:
                    self.d.focus_set(); self.d.icursor(tk.END)
                elif w is self.y:
                    self.m.focus_set(); self.m.icursor(tk.END)
            return

        # Оставляем только цифры
        cleaned = ''.join(c for c in w.get() if c.isdigit())
        if cleaned != w.get():
            w.delete(0, tk.END)
            w.insert(0, cleaned)

        max_len = 2 if w in (self.d, self.m) else 4

        # Если поле УЖЕ заполнено и пользователь НЕ выделил текст —
        # заменяем содержимое на последнюю введённую цифру
        if len(w.get()) > max_len:
            w.delete(0, tk.END)
            w.insert(0, event.char if event.char.isdigit() else "")

        # Автопереход
        if w is self.d and len(w.get()) == 2:
            self.m.focus_set()
            self.m.select_range(0, tk.END)
        elif w is self.m and len(w.get()) == 2:
            self.y.focus_set()
            self.y.select_range(0, tk.END)

    def _on_paste(self, event):
        try:
            data = event.widget.clipboard_get()
        except Exception:
            return
        nums = re.findall(r"\d+", data)
        if len(nums) >= 3:
            try:
                d = int(nums[0]); m = int(nums[1]); y = int(nums[2])
                if y < 100:
                    y += 2000 if y < 50 else 1900
                self.set_date(datetime(y, m, d).date())
            except Exception:
                pass
        elif len(nums) == 1 and len(nums[0]) == 8:
            s = nums[0]
            try:
                self.set_date(datetime(int(s[4:]), int(s[2:4]), int(s[:2])).date())
            except Exception:
                pass

    def get_date(self):
        try:
            d = int(self.d.get()); m = int(self.m.get()); y = int(self.y.get())
            return datetime(y, m, d).date()
        except (ValueError, TypeError):
            return None

    def set_date(self, date_obj):
        self.d.delete(0, tk.END); self.d.insert(0, f"{date_obj.day:02d}")
        self.m.delete(0, tk.END); self.m.insert(0, f"{date_obj.month:02d}")
        self.y.delete(0, tk.END); self.y.insert(0, str(date_obj.year))

    def is_filled(self):
        return bool(self.d.get()) and bool(self.m.get()) and bool(self.y.get())


def open_calendar_popup(date_input: DateInput):
    popup = tk.Toplevel()
    popup.title("Выбор даты")
    popup.geometry("+%d+%d" % (date_input.winfo_rootx(), date_input.winfo_rooty() + 30))
    popup.resizable(False, False)
    popup.transient(date_input.winfo_toplevel())
    popup.grab_set()

    current_date = date_input.get_date() or datetime.today().date()

    cal = Calendar(
        popup,
        selectmode="day",
        year=current_date.year,
        month=current_date.month,
        day=current_date.day,
        locale="ru_RU",
        date_pattern="dd.mm.yyyy"
    )
    cal.pack(padx=10, pady=10)

    def on_date_select(event=None):
        try:
            selected = cal.selection_get()
            date_input.set_date(selected)
            popup.destroy()
        except Exception:
            pass

    cal.bind("<<CalendarSelected>>", on_date_select)
    ttk.Button(popup, text="Выбрать", command=on_date_select).pack(pady=(0, 10))
    popup.bind("<Escape>", lambda e: popup.destroy())


def set_today(date_input: DateInput):
    date_input.set_date(datetime.today().date())


# ============================================================
# БАЗОВЫЙ КЛАСС ДЛЯ ВКЛАДОК
# ============================================================

class TabBase(ttk.Frame):
    """
    Каркас ничего не знает о смысле вкладки.
    Вкладка сама решает, что сохранять и как реагировать на тему.
    """
    title = "Вкладка"
    settings_key = "tab"

    def get_settings(self) -> dict:
        return {}

    def apply_settings(self, data: dict):
        pass

    def apply_theme(self, style):
        pass


# ============================================================
# ВКЛАДКА: Койко-дни
# ============================================================

class MedicalTab(TabBase):
    title = "🏥 Койко-дни"
    settings_key = "medical"

    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Дата поступления:").grid(
            row=0, column=0, sticky="w", padx=15, pady=10)
        self.date_start = DateInput(self, initial=datetime(2022, 6, 7).date())
        self.date_start.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        ttk.Button(self, text="📅", width=3,
                   command=lambda: open_calendar_popup(self.date_start)
                   ).grid(row=0, column=2, padx=2)
        ttk.Button(self, text="Сегодня", width=8,
                   command=lambda: set_today(self.date_start)
                   ).grid(row=0, column=3, padx=5)

        ttk.Label(self, text="Дата выписки:").grid(
            row=1, column=0, sticky="w", padx=15, pady=5)
        self.date_end = DateInput(self, initial=datetime(2026, 9, 8).date())
        self.date_end.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self, text="📅", width=3,
                   command=lambda: open_calendar_popup(self.date_end)
                   ).grid(row=1, column=2, padx=2)
        ttk.Button(self, text="Сегодня", width=8,
                   command=lambda: set_today(self.date_end)
                   ).grid(row=1, column=3, padx=5)

        self.is_day_hospital = tk.BooleanVar(value=False)
        self.chk_day = ttk.Checkbutton(
            self,
            text="Дневной стационар",
            variable=self.is_day_hospital,
            command=self._toggle_day_options
        )
        self.chk_day.grid(row=2, column=0, columnspan=4, padx=15, pady=(10, 0), sticky="w")

        self.day_options_frame = ttk.Frame(self)
        ttk.Label(self.day_options_frame, text="Формула койко-дней:").pack(
            side="left", padx=(15, 5))
        self.day_type_var = tk.StringVar(
            value="+2 (день поступления и день выписки — каждый за 1)")
        self.day_type_combo = ttk.Combobox(
            self.day_options_frame,
            textvariable=self.day_type_var,
            values=[
                "+2 (день поступления и день выписки — каждый за 1)",
                "+1 (по внутреннему учёту учреждения)",
            ],
            state="readonly",
            width=58,
        )
        self.day_type_combo.pack(side="left", padx=5)
        self.day_options_frame.grid(row=3, column=0, columnspan=4, padx=15, pady=(0, 5), sticky="w")
        self.day_options_frame.grid_remove()

        ttk.Button(self, text="Рассчитать", command=self.calculate).grid(
            row=4, column=0, columnspan=4, pady=10)

        self.lbl_res = ttk.Label(self, text="", justify="left")
        self.lbl_res.grid(row=5, column=0, columnspan=4, padx=15, sticky="w")
        make_copyable(self.lbl_res)
        ttk.Label(self, text="(клик по результату — копировать)",
                  foreground="gray").grid(
            row=6, column=0, columnspan=4, padx=15, sticky="w")

    def _toggle_day_options(self):
        if self.is_day_hospital.get():
            self.day_options_frame.grid()
        else:
            self.day_options_frame.grid_remove()

    def calculate(self):
        d1 = self.date_start.get_date()
        d2 = self.date_end.get_date()
        if not d1 or not d2:
            messagebox.showerror("Ошибка", "Введите корректные даты в формате ДД.ММ.ГГГГ")
            return
        if d1 > d2:
            messagebox.showerror("Ошибка", "Дата поступления не может быть позже даты выписки")
            return

        sick_days = (d2 - d1).days + 1

        if self.is_day_hospital.get():
            offset = 2 if self.day_type_var.get().startswith("+2") else 1
            hospital_days = (d2 - d1).days + offset
            type_str = "дневной стационар"
        else:
            hospital_days = max((d2 - d1).days, 1)
            type_str = "круглосуточный стационар"

        self.lbl_res.config(
            text=f"• Больничный лист: {pluralize(sick_days, ['календарный день', 'календарных дня', 'календарных дней'])}\n"
                 f"• Койко-дни ({type_str}): {pluralize(hospital_days, ['койко-день', 'койко-дня', 'койко-дней'])}"
        )

    def get_settings(self):
        d1 = self.date_start.get_date()
        d2 = self.date_end.get_date()
        return {
            "start": d1.strftime("%d.%m.%Y") if d1 else "",
            "end": d2.strftime("%d.%m.%Y") if d2 else "",
            "is_day_hospital": self.is_day_hospital.get(),
            "day_type": self.day_type_var.get(),
        }

    def apply_settings(self, data):
        def parse(s):
            try:
                return datetime.strptime(s, "%d.%m.%Y").date()
            except (ValueError, TypeError):
                return None
        d = parse(data.get("start", ""))
        if d: self.date_start.set_date(d)
        d = parse(data.get("end", ""))
        if d: self.date_end.set_date(d)
        if "is_day_hospital" in data:
            self.is_day_hospital.set(data["is_day_hospital"])
            self._toggle_day_options()
        if "day_type" in data and data["day_type"] in self.day_type_combo["values"]:
            self.day_type_var.set(data["day_type"])


# ============================================================
# ВКЛАДКА: Возраст
# ============================================================

class AgeTab(TabBase):
    title = "👶 Возраст"
    settings_key = "age"

    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Дата рождения:").grid(
            row=0, column=0, sticky="w", padx=15, pady=10)
        self.date_birth = DateInput(self, initial=datetime(1990, 1, 1).date())
        self.date_birth.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        ttk.Button(self, text="📅", width=3,
                   command=lambda: open_calendar_popup(self.date_birth)
                   ).grid(row=0, column=2, padx=2)
        ttk.Button(self, text="Сегодня", width=8,
                   command=lambda: set_today(self.date_birth)
                   ).grid(row=0, column=3, padx=5)

        ttk.Label(self, text="Расчёт на дату:").grid(
            row=1, column=0, sticky="w", padx=15, pady=5)
        self.date_target = DateInput(self, initial=datetime.today().date())
        self.date_target.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self, text="📅", width=3,
                   command=lambda: open_calendar_popup(self.date_target)
                   ).grid(row=1, column=2, padx=2)
        ttk.Button(self, text="Сегодня", width=8,
                   command=lambda: set_today(self.date_target)
                   ).grid(row=1, column=3, padx=5)

        ttk.Button(self, text="Рассчитать", command=self.calculate).grid(
            row=2, column=0, columnspan=4, pady=15)

        self.lbl_res = ttk.Label(self, text="", justify="left")
        self.lbl_res.grid(row=4, column=0, columnspan=4, padx=15, sticky="w")
        make_copyable(self.lbl_res)
        ttk.Label(self, text="(клик по результату — копировать)",
                  foreground="gray").grid(
            row=5, column=0, columnspan=4, padx=15, sticky="w")

    def calculate(self):
        d1 = self.date_birth.get_date()
        d2 = self.date_target.get_date()
        if not d1 or not d2:
            messagebox.showerror("Ошибка", "Введите корректные даты в формате ДД.ММ.ГГГГ")
            return
        if d1 > d2:
            messagebox.showerror("Ошибка", "Дата рождения не может быть позже целевой даты")
            return
        diff = relativedelta(d2, d1)
        self.lbl_res.config(
            text=f"Возраст на дату {d2.strftime('%d.%m.%Y')}:\n"
                 f"• {pluralize(diff.years, ['год', 'года', 'лет'])}\n"
                 f"• {pluralize(diff.months, ['месяц', 'месяца', 'месяцев'])}\n"
                 f"• {pluralize(diff.days, ['день', 'дня', 'дней'])}"
        )

    def get_settings(self):
        d1 = self.date_birth.get_date()
        d2 = self.date_target.get_date()
        return {
            "birth": d1.strftime("%d.%m.%Y") if d1 else "",
            "target": d2.strftime("%d.%m.%Y") if d2 else "",
        }

    def apply_settings(self, data):
        def parse(s):
            try:
                return datetime.strptime(s, "%d.%m.%Y").date()
            except (ValueError, TypeError):
                return None
        d = parse(data.get("birth", ""))
        if d: self.date_birth.set_date(d)
        d = parse(data.get("target", ""))
        if d: self.date_target.set_date(d)


# ============================================================
# ВКЛАДКА: Аналитика
# ============================================================

class PeriodTab(TabBase):
    title = "📅 Аналитика"
    settings_key = "period"

    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Прямой расчёт (интервал между датами)",
                  font=("", 10, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(10, 5))

        ttk.Label(self, text="Дата начала:").grid(
            row=1, column=0, sticky="w", padx=15, pady=5)
        self.date_start = DateInput(self, initial=datetime(2022, 6, 7).date())
        self.date_start.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self, text="📅", width=3,
                   command=lambda: open_calendar_popup(self.date_start)
                   ).grid(row=1, column=2, padx=2)
        ttk.Button(self, text="Сегодня", width=8,
                   command=lambda: set_today(self.date_start)
                   ).grid(row=1, column=3, padx=5)

        ttk.Label(self, text="Дата окончания:").grid(
            row=2, column=0, sticky="w", padx=15, pady=5)
        self.date_end = DateInput(self, initial=datetime(2026, 9, 8).date())
        self.date_end.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self, text="📅", width=3,
                   command=lambda: open_calendar_popup(self.date_end)
                   ).grid(row=2, column=2, padx=2)
        ttk.Button(self, text="Сегодня", width=8,
                   command=lambda: set_today(self.date_end)
                   ).grid(row=2, column=3, padx=5)

        ttk.Button(self, text="Рассчитать период",
                   command=self.calculate).grid(
            row=3, column=0, columnspan=4, pady=10, sticky="w", padx=15)

        self.lbl_res = ttk.Label(self, text="", justify="left")
        self.lbl_res.grid(row=4, column=0, columnspan=4, padx=15, sticky="w")
        make_copyable(self.lbl_res)
        ttk.Label(self, text="(клик по результату — копировать)",
                  foreground="gray").grid(
            row=5, column=0, columnspan=4, padx=15, sticky="w")

    def calculate(self):
        d1 = self.date_start.get_date()
        d2 = self.date_end.get_date()
        if not d1 or not d2:
            messagebox.showerror("Ошибка", "Введите корректные даты в формате ДД.ММ.ГГГГ")
            return
        if d1 > d2:
            messagebox.showerror("Ошибка", "Дата начала не может быть позже даты окончания")
            return
        diff = relativedelta(d2, d1)
        total_months = diff.years * 12 + diff.months
        total_days = (d2 - d1).days
        self.lbl_res.config(
            text=f"• Перевод: {pluralize(diff.years, ['год', 'года', 'лет'])}, "
                 f"{pluralize(diff.months, ['месяц', 'месяца', 'месяцев'])}, "
                 f"{pluralize(diff.days, ['день', 'дня', 'дней'])}\n"
                 f"• Полных месяцев: {total_months}\n"
                 f"• Всего дней в периоде: {total_days}"
        )

    def get_settings(self):
        d1 = self.date_start.get_date()
        d2 = self.date_end.get_date()
        return {
            "start": d1.strftime("%d.%m.%Y") if d1 else "",
            "end": d2.strftime("%d.%m.%Y") if d2 else "",
        }

    def apply_settings(self, data):
        def parse(s):
            try:
                return datetime.strptime(s, "%d.%m.%Y").date()
            except (ValueError, TypeError):
                return None
        d = parse(data.get("start", ""))
        if d: self.date_start.set_date(d)
        d = parse(data.get("end", ""))
        if d: self.date_end.set_date(d)


# ============================================================
# ВКЛАДКА: О программе
# ============================================================

class AboutTab(TabBase):
    title = "ℹ О программе"
    settings_key = "about"

    def __init__(self, parent):
        super().__init__(parent)

        # Скроллируемая обёртка
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = ttk.Frame(self.canvas)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        self._wrap_labels = []
        padx_side = 20

        # ---------- Заголовок ----------
        ttk.Label(self.inner, text="ℹ️ О программе",
                  font=("", 11, "bold")).pack(padx=padx_side, pady=(20, 10), anchor="w")

        header_frame = ttk.Frame(self.inner)
        header_frame.pack(padx=padx_side, pady=(0, 15), fill="x", anchor="w")

        text_title = "🏥 Медицинский календарный калькулятор\nВерсия: 2.3 (Open Source)"
        self.lbl_title = tk.Label(header_frame, text=text_title, justify="left",
                                  font=("", 10, "bold"), fg="darkblue")
        self.lbl_title.pack(side="left", anchor="w")

        self.lbl_logo = None
        try:
            self.logo_img = tk.PhotoImage(data=LOGO_BASE64)
            self.lbl_logo = tk.Label(header_frame, image=self.logo_img)
            self.lbl_logo.image = self.logo_img
            self.lbl_logo.pack(side="left", padx=15, anchor="center")
        except Exception:
            pass

        # ---------- Описание ----------
        text_description = (
            "Универсальный инструмент для автоматизации расчётов в работе "
            "медицинского персонала, кадровиков и экспертов.\n\n"
            "• Койко-дни и больничные: расчёт листка нетрудоспособности "
            "(включительно) и койко-дней.\n"
            "• Дневной стационар: выбор формулы учёта койко-дней (+2 или +1).\n"
            "• Калькулятор возраста: расчёт возраста пациента в годах, "
            "месяцах и днях на любую дату.\n"
            "• Аналитика периодов: перевод временных интервалов в полные "
            "года, месяцы и дни.\n"
        )
        self._add_wrapped_label(text_description, padx_side, (0, 0))

        # ---------- Обновления и связь ----------
        text_updates = (
            "📢 ОБНОВЛЕНИЯ И СВЯЗЬ:\n"
            "Актуальная версия программы и обсуждение — на GitHub.\n"
            "Скачать последнюю версию можно там же или напрямую:"
        )
        self._add_wrapped_label(text_updates, padx_side, (10, 5))

        # Ссылки-«кнопки»
        links_frame = ttk.Frame(self.inner)
        links_frame.pack(padx=padx_side, pady=(0, 10), anchor="w")

        self.lbl_github = tk.Label(
            links_frame,
            text="→ Страница проекта и обсуждение (GitHub)",
            font=("", 10, "underline"), fg="blue", cursor="hand2"
        )
        self.lbl_github.pack(anchor="w", pady=1)
        self.lbl_github.bind("<Button-1>", lambda e: webbrowser.open_new(GITHUB_DISCUSSIONS))

        self.lbl_disk_file = tk.Label(
            links_frame,
            text="→ Скачать Medic_Calc_ver_2.3.exe (Яндекс.Диск)",
            font=("", 10, "underline"), fg="blue", cursor="hand2"
        )
        self.lbl_disk_file.pack(anchor="w", pady=1)
        self.lbl_disk_file.bind("<Button-1>", lambda e: webbrowser.open_new(YANDEX_DISK_FILE))

        self.lbl_disk_folder = tk.Label(
            links_frame,
            text="→ Все файлы: исходник, README, LICENSE (Яндекс.Диск)",
            font=("", 10, "underline"), fg="blue", cursor="hand2"
        )
        self.lbl_disk_folder.pack(anchor="w", pady=1)
        self.lbl_disk_folder.bind("<Button-1>", lambda e: webbrowser.open_new(YANDEX_DISK_FOLDER))

        # ---------- Email ----------
        text_email = (
            "Нашли баг, есть идея или предложение? Напишите на почту:"
        )
        self._add_wrapped_label(text_email, padx_side, (5, 0))

        self.email_str = "alexbobrov_medproect@list.ru"
        self.lbl_email = tk.Label(self.inner, text=self.email_str,
                                  font=("", 10, "underline"),
                                  fg="darkgreen", cursor="hand2")
        self.lbl_email.pack(padx=padx_side, pady=(0, 10), anchor="w")
        self.lbl_email.bind("<Button-1>", self.copy_email)

        # ---------- Поддержка проекта ----------
        text_middle = (
            "Программа полностью бесплатна. Если калькулятор сэкономил ваше "
            "время, вы можете поддержать автора добровольным донатом:"
        )
        self._add_wrapped_label(text_middle, padx_side, (5, 0))

        donate_frame = ttk.Frame(self.inner)
        donate_frame.pack(padx=padx_side, pady=(10, 15), anchor="w")

        try:
            self.qr_img = tk.PhotoImage(data=QR_BASE64)
            self.qr_img = self.qr_img.subsample(3, 3)
            self.lbl_qr = tk.Label(donate_frame, image=self.qr_img)
            self.lbl_qr.image = self.qr_img
            self.lbl_qr.pack(side="left", padx=(0, 15), anchor="n")
        except Exception as e:
            print(f"QR-код не загружен: {e}")
            self.lbl_qr = None

        donate_text_frame = ttk.Frame(donate_frame)
        donate_text_frame.pack(side="left", anchor="n")

        ttk.Label(donate_text_frame,
                  text="Поддержать проект (СБП):",
                  justify="left").pack(anchor="w", pady=(0, 5))

        self.lbl_donate_link = tk.Label(
            donate_text_frame,
            text="pay.cloudtips.ru/p/61064256",
            font=("", 10, "underline"),
            fg="blue", cursor="hand2"
        )
        self.lbl_donate_link.pack(anchor="w", pady=(0, 5))
        self.lbl_donate_link.bind("<Button-1>", self.open_donation)

        ttk.Label(donate_text_frame,
                  text="Наведите камеру телефона на QR-код\nили кликните по ссылке.",
                  justify="left", foreground="gray").pack(anchor="w")

        # ---------- Примечание ----------
        text_note = (
            "📌 ПРИМЕЧАНИЕ ПО КОЙКО-ДНЯМ ДНЕВНОГО СТАЦИОНАРА:\n"
            "Стандартное правило учёта в дневном стационаре — день поступления "
            "и день выписки считаются каждый за 1 день (формула +2). Однако "
            "в отдельных учреждениях действуют внутренние правила (формула +1). "
            "В спорных случаях ориентируйтесь на локальные нормативные документы."
        )
        self._add_wrapped_label(text_note, padx_side, (5, 10))

        # ---------- Дисклеймер ----------
        text_bottom = (
            "⚖️ ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ:\n"
            "Программное обеспечение предоставляется на условиях «КАК ЕСТЬ» "
            "(AS IS), без каких-либо гарантий. Автор не несёт ответственности "
            "за любые ошибки в расчётах или иные последствия, возникшие в "
            "результате использования ПО. Перед подачей официальных документов "
            "всегда проверяйте данные вручную."
        )
        self._add_wrapped_label(text_bottom, padx_side, (5, 20))

    def _add_wrapped_label(self, text, padx, pady):
        lbl = ttk.Label(self.inner, text=text, justify="left", wraplength=540)
        lbl.pack(padx=padx, pady=pady, anchor="w", fill="x")
        self._wrap_labels.append((lbl, padx))
        return lbl

    def _on_canvas_resize(self, event):
        self.canvas.itemconfigure(self.inner_id, width=event.width)
        for lbl, padx in self._wrap_labels:
            new_wrap = max(200, event.width - 2 * padx - 20)
            lbl.configure(wraplength=new_wrap)

    def _bind_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        else:
            delta = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(delta, "units")

    def open_donation(self, event=None):
        webbrowser.open_new(DONATION_URL)

    def copy_email(self, event):
        self.clipboard_clear()
        self.clipboard_append(self.email_str)
        self.update()
        messagebox.showinfo("Успешно", "Email скопирован в буфер обмена!")

    def apply_theme(self, style):
        bg = style.lookup("TFrame", "background") or self.cget("bg")
        for attr in ("lbl_title", "lbl_email", "lbl_donate_link",
                     "lbl_qr", "lbl_github", "lbl_disk_file", "lbl_disk_folder"):
            lbl = getattr(self, attr, None)
            if lbl is not None:
                try:
                    lbl.configure(bg=bg)
                except Exception:
                    pass

# ============================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ (КАРКАС)
# ============================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Медицинский календарный калькулятор")
        self.geometry("760x600")
        self.minsize(380, 300)

        self.style = ttk.Style()
        self._native_theme_name = self.style.theme_use()

        # Доступные системные темы (отфильтрованные по текущей ОС)
        available = set(self.style.theme_names())
        self.available_themes = {
            name: sys_name
            for name, sys_name in NATIVE_THEMES.items()
            if sys_name in available
        }

        # Цвета выделения текста в Entry — чтобы он был читаемым
        self.style.map("TEntry",
                       selectbackground=[("focus", "#3399ff"), ("!focus", "#c0c0c0")],
                       selectforeground=[("focus", "#ffffff"), ("!focus", "#000000")])

        # Если по какой-то причине ни одной темы из списка нет — оставим нативную
        if not self.available_themes:
            self.available_themes = {"Системная": self._native_theme_name}

        # ---------- Верхняя панель ----------
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(self.top_frame, text="Тема:").pack(side="left", padx=(0, 5))

        default_theme = (DEFAULT_THEME_NAME
                         if DEFAULT_THEME_NAME in self.available_themes
                         else list(self.available_themes.keys())[0])
        self.theme_var = tk.StringVar(value=default_theme)

        self.theme_combo = ttk.Combobox(
            self.top_frame,
            textvariable=self.theme_var,
            values=list(self.available_themes.keys()),
            state="readonly",
            width=28,
        )
        self.theme_combo.pack(side="left", padx=(0, 15))
        self.theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        ttk.Label(self.top_frame, text="Размер шрифта:").pack(side="left", padx=(0, 5))

        self.FONT_PRESETS = {
            "Мелкий (10)": 10,
            "Обычный (12)": 12,
            "Крупный (14)": 14,
            "Очень крупный (16)": 16,
        }
        self.font_var = tk.StringVar(value="Обычный (12)")
        self.font_combo = ttk.Combobox(
            self.top_frame,
            textvariable=self.font_var,
            values=list(self.FONT_PRESETS.keys()),
            state="readonly",
            width=18,
        )
        self.font_combo.pack(side="left")
        self.font_combo.bind("<<ComboboxSelected>>", self.on_font_change)

        # ---------- Notebook ----------
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.tabs = []
        self._register_default_tabs()

        # Применяем тему и настройки
        self.load_settings()
        self.apply_current_theme()
        self.apply_font_size(self.FONT_PRESETS.get(self.font_var.get(), 10))
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _register_default_tabs(self):
        for cls in (MedicalTab, AgeTab, PeriodTab, AboutTab):
            tab = cls(self.notebook)
            self.tabs.append(tab)
            self.notebook.add(tab, text=tab.title)

    # ---------- Темы ----------

    def on_theme_change(self, event=None):
        self.apply_current_theme()

    def apply_current_theme(self):
        name = self.theme_var.get()
        sys_name = self.available_themes.get(name, self._native_theme_name)
        try:
            self.style.theme_use(sys_name)
        except Exception:
            pass
        # Даём вкладкам возможность перекрасить свои tk.Label
        for tab in self.tabs:
            try:
                tab.apply_theme(self.style)
            except Exception:
                pass

    # ---------- Шрифт ----------

    def on_font_change(self, event=None):
        size = self.FONT_PRESETS.get(self.font_var.get(), 10)
        self.apply_font_size(size)

    def apply_font_size(self, size):
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont",
                     "TkHeadingFont", "TkCaptionFont", "TkSmallCaptionFont",
                     "TkIconFont", "TkTooltipFont"):
            try:
                tkfont.nametofont(name).configure(size=size)
            except Exception:
                pass

    # ---------- Настройки ----------

    def save_settings(self):


        data = {
            "font_preset": self.font_var.get(),
            "theme": self.theme_var.get(),
        }
       
        for tab in self.tabs:
            data[tab.settings_key] = tab.get_settings()
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Не удалось сохранить настройки: {e}")

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            return
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return

        # Тема — только если доступна
        if data.get("theme") in self.available_themes:
            self.theme_var.set(data["theme"])

        # Размер шрифта (пресет)
        if data.get("font_preset") in self.FONT_PRESETS:
            self.font_var.set(data["font_preset"])

        # Вкладки сами разбирают свои данные
        for tab in self.tabs:
            if tab.settings_key in data and isinstance(data[tab.settings_key], dict):
                try:
                    tab.apply_settings(data[tab.settings_key])
                except Exception as e:
                    print(f"Не удалось загрузить настройки вкладки {tab.settings_key}: {e}")

    def on_close(self):
        self.save_settings()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()