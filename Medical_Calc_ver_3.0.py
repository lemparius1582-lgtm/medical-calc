# ============================================================
# Medical_Calc_ver_3.0.py
# Медицинский календарный калькулятор
#
# Изменения относительно 2.4/2.5:
#   - Обратный расчёт (дни → годы/месяцы/дни) во вкладке "Аналитика";
#   - новая вкладка "Високосные года" (справочник 1900–2100);
#   - убраны стрелки Up/Down в DateInput (стандартное поведение);
#   - опциональное запоминание размера окна;
#   - подготовка к кроссплатформенности (Windows / Linux / macOS).
# ============================================================

import sys
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

# Логотип в base64 (код картинки).
LOGO_BASE64 = "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"

# QR-код автора в base64
QR_BASE64 = "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nl2effbZ+jVz5szyzDPPlLfeequ88cYbZcaMGeXtt99+1387duzYsswyy5Sll166rLTSSmXixIll3LhxZa211iobbrhh2WCDDcqqq65a/z3+HAAWlqAB4H0iVB5++OEaKk8//XQNmBdffLHMmjWrvPzyy2XevHnvfM2dO7d+RcRE1HzQyEj8fvzdN998s7z++uv1ssaMGVOeeOKJcs8995TllluuLLXUUmXZZZetYbPaaquVtddeu6y77rpljTXWqH8GAB9E0ABQXnnllRolr776annhhRfK7373u3LzzTeXhx56qNx77731z4ciYue1116rX/E9/pgImS233LJss802ZaONNirrrbdejZwJEybUuFliiSUKAARBA9DnYsTliiuuKNdff30NmWnTptW46XQ6NUTeO32sF5588skyffr0ctlll9XRnTXXXLNst912Za+99irbbrttmTRpUh3NAQBBA9CHIhjuuOOOcuedd9YRmFgXE2tfYp3M/PnzR/rqvRNSCxYsqP/++OOP11Gi+++/v05Pi8DZdddda+BMnjy5ANC/BA1An4g1LLGA/4EHHii33nprnVJ222231TUyGcRUuPgacN9999U1OBE266+/fllnnXXK+PHjCwD9RdAA9IE5c+bUeDn33HPrNK4YkckuRpji6wc/+EHZb7/9ytSpU8tOO+1U19kA0D8EDcAoE7uMxfqXENO2ImD++7//u9x4443lqaeeKi+99FIZTWLHtEsuuaTccsstZbPNNit77LFH+cxnPlN3SRsw+D4BYHQRNACjTHxwj0X9sR1yjGDEh/1rr732XdO1RpuB6WgPPvhgjbYYgdp5553LlClT6nQ0MQMwegkagFEkRiJiVCZ2LDvrrLPKxRdfXHcx6yexU1t8xajUMcccU44++ui6vgaA0UnQAIwisVPZt771rboNcyyYj7Uz/eqxxx4r//Vf/1XD5oQTTijHHnvsO39mChrA6CFoRrm2/8D+oBPF26Tp+6/fbm/b779O8g+0gz+Ux05lMSpx1VVXlQsuuCDNzmXDZeAMnVmzZtWv0047rY5U7bLLLmWLLbYo48aNG+mr2Hevj7a//8GH4fncLoIGIKmBD5yzZ8+uU8t+8pOf1LUyvP/Dxg033FC3eT7ssMPKUUcdVcNmscUWKwDkJ2gAEosF8KeeemqNmdGwFfNwit3dfvjDH5bnnnuuHtK5//77FwDyEzQAScX0sgsvvLBceumlYmYhLViwoFx99dV1bdFDDz1UPve5z5U111yzAJCXoAFIZmBL5u9///t1qtm8efPq78cUNPO6/7g4t+byyy+vWzzHffbZz362Rk3HJgEAKQkagERihCG2ZD7ppJPKtGnT3omZIGY+nMcff7x885vfLA8//HD5+te/XlZddVVRA5CQoAFIInbtOvvss8uZZ55ZD8ycP39+YWhmzpxZLrroojrq9dd//ddl8803LwDkImgAEoiRmGuuuaacc845djJr2PTp08t5551X1lhjjbL44ouXTTbZpACQh6ABSODee+8t//qv/1puvfXWQvMiGL/73e/WKX3/+I//WJZeeukCQA6CBqCFBh+aGbuZxYn3sWbm9ddfLwyP559/vu4aF/f73//935dlllnmXY8DAO0kaABaaOBDdEyH+tWvflW3ZrZmZvjFzmcXXHBB2Wabbco+++xTowaAdhM0AC0VB0DGmpnf/OY3YqaHYtez0047rYwZM6YcfPDBBYB2EzQALRQjM7/85S/rB+tHHnmk0Duxm1xE5Pjx4+sIzW677VbGjh1bAGgnQQPQQrfffnsdnRmIGYdm9lbc17Gb3PLLL1+23HLLMnHixAJAOwkagJZ56KGHymWXXVZuvPHGd35PzPReTPmLx2H//fcve+65Z5kwYUIBoH0EDUCLvPXWW+Ub3/hGnW7GyJs1a1b553/+57qe5oADDigAtI+gAWiJV155pR6eecstt5Q5c+YURt4bb7xR7rrrrvLrX/+6rLfeemXzzTcvALSLoAFoiXvuuaecccYZZcaMGYV2ufrqq8tqq61W1l9//bLUUksVANpD0AC0wJtvvll+97vflYsuuqjQPg888EC5/PLLy+c///kyefJkh20CtIigAWiBK664olx11VWF9orNGk4//fTyla98pUyaNKkA0A6CZoia3nmo7f/Xz+0dmqZvb7/tfNX2+29Rr1+MzsT//b/++usL7fX888+XCy+8sOywww6NBE2321/vp6P19UsOXTtFjmqCBmAExa5mTzzxRLnpppvK7NmzC+0Vj1WcC3TDDTfUs2k23HDDAsDIEzQAI+iZZ56pB2hOnz69kENMD1xnnXUEDUBLCBqAERSjM7/4xS/KzJkzCzncfffd5brrrqsbBEycOLEAMLIEDcAIefXVV8u0adPqF81YbLHFytixY+tBmANrImLufKxTijNlmhBTz+677756XtDHPvaxMmHChALAyBE0ACPkyiuvLBdffHGhOcsvv3w9/DIW7Y8fP76GzGuvvVbP+IlwjH9uQmwQEFPPNt10U0EDMMIEDcAIiA/a1157bf1i6Lbeeus6WhKL9VdfffWy4oorlo985CPl7bffrvf1c889Vx5++OFy880310X9jz/++JC+XwTN//7v/5YvfOELZb311isAjBxBA9BjCxYsKE899VQdNZgzZ07JKqZ2jRs3riy55JLv/Bq/F9O+Bnv99ddrVMTX3Llz61f8XhMiWrbaaqty+OGHl0MPPbSstdZaf/Dv33jjjWXNNdcsl156aZ02Fo/Foojpa/fff3+NpG222abebgBGhqAB6LH58+fX6U+vvPJKySymdcX0rs0226z+Grt+rbbaajVuYv1KfMX6lccee6zMmDGjbnwQQXHbbbfVQypffPHFIV+H/fbbr3z5y18uu+++ew2qP2b77bev08S222678rWvfa08+eSTi/y9Y/pabA6w/vrrlx133LEAMDIEDUCPxQjFNddcU55++umSwUCYhKWXXrpMmTKlfOITnyjbbrttHe2INSQrrLBCWW655d43OhMieGJa1rx58+p/GyET21X/9re/LVdddVXdNezDXpf4PgcddFD5kz/5k3pdFiZmQvx3cX0//vGPl7/7u78r3/nOd2pcLYq4HnfccUc9aFPQAIwcQQPQY7Ge4/rrr0+zVfNAQMRIxE477VQ++clPlj333LOuVVkY8d/GAv34GrzNcYzqrLHGGuWyyy6rI1ZxvyzMdYl42XnnncuXvvSlGiYxIvRhrbLKKnX9S0TVogZNiGlrDz74YAFg5AgagB6KLX9jmlN8EI41JVlssMEG5c///M/LYYcdVmOgCTFyE5cbi/lPOeWUumvYs88++0f/u7322qv8xV/8RR2ZiTU0iyp2RNttt93qOpibbrppkS7j5ZdfLo888khdE7TEEksUAHpP0AD0UIzKxP/RX9TF6CNh6tSp5Ygjjqg7iTUVMwMiAmIa2kknnVTXt8Qho7F72MAUtzB4ylscZnn00UfXkZmhxMyAWEsTU94WNWhCbPAQU+fiOsWUPAB6S9AA9FCMzsT0qsEf2NsqPpzH1LJYpxKL7gfEdR84tLIJETUxUhO7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9WP0iAMxZ8+eXa699tp6+CXtE9MDDz300LLOOuss9H/zh17zTb+/NK3f3q86ffbzqN9ub9O6fp63iqABaIEllliibL311mWfffYpl156qahpmThA86CDDiprr7126z9oAfQbQQPQEhtvvHHdIOD+++8v99xzT6E9Yie6ww8/vB5UCkC7CBqAlog1GgcccEC57LLLyqxZs+oUNEbWmDFjyhprrFG3ad50000LAO0jaABaZLHFFit/8zd/Uz9In3zyyYWRFetm/v3f/70GDQDtJGgAWmbSpEn1A/Qtt9xSbrzxxsLIWHHFFet5M7vttltZbrnlCgDtJGgAWmibbbYpRx55ZJk5c2Z5/PHHC721+OKLl0984hPl85//vJgBaDlBA9BCa621VjnssMPq2TTnn39+PXST3oiYiR3NjjvuuPLJT36yANBuggagpSZOnFiOP/74MmfOnHL66aeX+fPnF4ZfTPk7+uij6wgNAO0naABaKA5ti/NO4sP1wQcfXKZPn16uuOKKGjcMn8mTJ5dDDjmkxsy4cePeeRwAaC9BA9BCgz9E77HHHmXChAl1K+dbb721vP7664XmxSYAn/3sZ8s//MM/lKWXXrr+npgBaD9BA5BAnIESH7S//e1vl6uuuqrQrDgw84QTTihHHHHEOzEDQA6CBiCB+MC9zz77lGeffbYsWLCgbulsTU0z1lxzzbr4P3Y022STTQoAuQgagCTi0M2pU6fWk+tPOumkMm3atDJ37tzCoouDM2NHs69//ev1nwHIR9AAJDJmzJiyyy67lO985zt1+tnFF19c5s2bV/8s1nvEInYWzrrrrltOPPHEuglAxIz1MgA5CRqAZGKNx/bbb1++8pWvlFVWWaVceeWV5b777hMzC2n8+PHlox/9aB2ZOfTQQ+uIFwB5CRqApGL3s9gsIA7hPO2008qDDz5Y+MPGjh1bR7iOOeaY8oUvfKEAkJ+gAUgspkode+yxdVvnH//4x+W6664rfLDllluuLvyPncx22mmnAsDoIGgAkho49DHOT/n0pz9d42brrbeuYfPCCy8U/p+4jz7+8Y+Xz3zmM2XXXXctW265ZR2pAWB0EDQASQ1exB7rQOIr1obMmTOnXHvttXWL5/jnfhXRsvLKK5eNN964HHfccXWK2cB9NhCDAOQnaIao7T8Qm14k3PTtbfsi5m6fLbLut8e3l6/fXt0XETWnnnpq3SjgzDPPLOeee27pV1tttVU56qij6i5mcdbMYG147277+3Pb3w86ffZ+1Xadln8e8nwZ3QQNwCgSP7Rja+eYWhVrRnbeeec6WnPDDTeUp59+uvSDOBxz//33L7vttludgvfemAFgdBE0AKNM/J/D2Np5hx12KNttt13ZfPPN65kr119/fZk+fXqZPXt2ee2118poMm7cuLLSSivVmPnEJz5RF/+vv/767/y5KWYAo5egARhlBn9wX2yxxcruu+9eR2yeeeaZcv7555ef//zn5aabbiqjxVJLLVW22WabukZm7733LhtssMH7/o6YARi9BA1AH4gF8muvvXY58sgj6zks9957b7n00kvLNddcU5577rmSTUyri93KYhOEGIWKqWXrrLNO3fENgP4iaAD6yGqrrVa/IgRibUmMZtx+++3l5ZdfrruixShOW6ejLb/88nXXsgizyZMnly222KKOzMThossss0wBoD8JGoA+9JGPfKROz9prr73KjBkzyj333FMP5YwNBKZNm1bmzZtXp6u99dZb5e233+75jj7xvQe+4ntHfE2ZMqWuC9pzzz3rPwNAEDQAfWzxxRevWz2vsMIKdbRj6tSp5cknnywPP/xwjZwYvbn77rvLq6++2tPrFdPHNtpoo7rIPw7FnDRpUh2Fic0OJkyYUABggKAB6HMxChKhEF+rrLJKPYgy1qTEaMhjjz1Wt3ueOXNm3R1t7ty5NW5eeuml8uKLL9bpaW+88Ub9/fj1zTffrL++V6zhicuP0ZYYHRo/fnxdzB+/F7/GV+xSFl8xtSymxa2++uo1tmJKWayZAYAP4icEAO8zceLE+hVrbQbEqE2ss3nqqafKQw89VP/9hRdeqIETa29eeeWVGjYRNe+dorbEEkvUBfsxhW3ZZZetsRLxNPAV3ysOwoxRmYgfAFhYggaAhRIbCHzQlsgAMJIEDQAAkJagAeiBNhzs2PROZZ2WH1bZ653ZABgZggYAAEhL0AAAAGkJGgAAIC1BAwAApCVoAACAtAQNAACQlqABAADSEjRD5FyHdnH/tUvTj0fT91/X85kPoe3P56a1/edbt8/eT7s+bwxJx/vpqCZoAACAtAQNAACQlqABAADSEjQAAEBaggYAAEhL0AAAAGkJGgAAIC1BAwAApCVoAACAtAQNAACQlqABAADSEjQA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"

# Ссылка на страницу донатов (СБП).
DONATION_URL = "https://pay.cloudtips.ru/p/61064256"

# Ссылки блока «Обновления и связь».
YANDEX_DISK_FILE = "https://disk.yandex.ru/d/MfIWdGoYsam6qA"
YANDEX_DISK_FOLDER = "https://disk.yandex.ru/d/O-fXEJZTPFi2ew"
GITHUB_REPO = "https://github.com/lemparius1582-lgtm/medical-calc"
GITHUB_DISCUSSIONS = "https://github.com/lemparius1582-lgtm/medical-calc/discussions"

# Опорная дата для обратного расчёта (дни → годы/месяцы/дни).
# Фиксированная, чтобы результат был воспроизводим между запусками.
# Пользователю не показывается.
DAYS_BASE_DATE = datetime(1900, 1, 1).date()

# ---------- Платформо-зависимые настройки ----------

IS_WINDOWS = sys.platform.startswith("win")
IS_LINUX = sys.platform.startswith("linux")
IS_MAC = sys.platform == "darwin"


def _get_settings_path() -> str:
    """
    Возвращает путь к файлу настроек.
      - Linux/macOS: ~/.config/medical_calc/settings.json (XDG-стандарт);
      - Windows:     ~/.medical_calc_settings.json (как было).
    Каталог для Linux/macOS создаётся автоматически.
    """
    if IS_LINUX or IS_MAC:
        cfg_dir = os.path.join(os.path.expanduser("~"), ".config", "medical_calc")
        os.makedirs(cfg_dir, exist_ok=True)
        return os.path.join(cfg_dir, "settings.json")
    return os.path.join(os.path.expanduser("~"), ".medical_calc_settings.json")


SETTINGS_FILE = _get_settings_path()

# Системные темы ttk. Ключ — отображаемое имя, значение — системное.
NATIVE_THEMES = {
    "Windows (системная)":        "vista",
    "Windows классическая":       "winnative",
    "Кроссплатформенная светлая": "clam",
    "Серая минималистичная":      "alt",
    "Windows классика (XP)":      "xpnative",
}

if IS_WINDOWS:
    DEFAULT_THEME_NAME = "Windows (системная)"
else:
    DEFAULT_THEME_NAME = "Кроссплатформенная светлая"

# Маппинг устаревших имён тем на актуальные (обратная совместимость).
THEME_RENAMES = {
    "Системная тёмная": "Windows классика (XP)",
}


# ---------- Проверка поддержки эмодзи ----------

def _supports_emoji() -> bool:
    """
    Грубая проверка: есть ли в системе шрифт с поддержкой эмодзи.
    На Linux без пакета fonts-noto-color-emoji эмодзи в UI
    отображаются как «квадратики», поэтому мы их отключаем.
    """
    try:
        families = tkfont.families()
        return any("emoji" in f.lower() for f in families)
    except Exception:
        return False


# ============================================================
# УТИЛИТЫ
# ============================================================

def pluralize(number, titles):
    """
    Склоняет существительное по числу.
    titles — список из трёх форм: [ед.ч., 2-4, 5+].
    """
    cases = [2, 0, 1, 1, 1, 2]
    idx = 2 if (number % 100 > 4 and number % 100 < 20) else cases[min(number % 10, 5)]
    return f"{number} {titles[idx]}"


def is_leap(year: int) -> bool:
    """
    Проверяет, является ли год високосным по григорианскому календарю.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def make_copyable(label, get_text_fn=None):
    """
    Делает tk/ttk Label копируемым по клику.
    """
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
    """
    Поле ввода даты из трёх отдельных Entry: день, месяц, год.

    Гибридная валидация:
      - <KeyPress> через validatecommand: блокирует нецифровые символы;
      - <KeyRelease>: автопереход, замена при переполнении,
        мгновенная подсветка грубых выходов за диапазон;
      - <FocusOut>: полная проверка диапазонов и существования даты.

    Поддерживает вставку из буфера: ДД.ММ.ГГГГ, ДД/ММ/ГГГГ, ДДММГГГГ.
    Tab-переход между полями.
    """

    MIN_YEAR = 1900
    MAX_YEAR = 2100

    ERROR_FG = "#b00000"
    ERROR_BG = "#ffd6d6"
    NORMAL_STYLE = "TEntry"
    ERROR_STYLE = "Error.TEntry"

    def __init__(self, parent, initial=None, **kw):
        super().__init__(parent, **kw)

        self._style = ttk.Style()
        self._style.configure(
            self.ERROR_STYLE,
            fieldbackground=self.ERROR_BG,
            foreground=self.ERROR_FG,
            bordercolor=self.ERROR_FG,
            lightcolor=self.ERROR_FG,
            darkcolor=self.ERROR_FG,
        )

        self.d = ttk.Entry(self, width=4)
        self.m = ttk.Entry(self, width=4)
        self.y = ttk.Entry(self, width=6)

        self.d.pack(side="left")
        ttk.Label(self, text=".").pack(side="left")
        self.m.pack(side="left")
        ttk.Label(self, text=".").pack(side="left")
        self.y.pack(side="left")

        self._vcmd = (self.register(self._validate_char), "%P", "%S")

        for w in (self.d, self.m, self.y):
            w.configure(validate="key", validatecommand=self._vcmd)
            w.bind("<KeyRelease>", self._on_key)
            w.bind("<FocusOut>", self._validate_ranges)
            w.bind("<<Paste>>", self._on_paste)

        # Tab: переходим на следующее поле, с последнего — выходим.
        self.d.bind("<Tab>", self._tab_next(self.m))
        self.m.bind("<Tab>", self._tab_next(self.y))
        self.y.bind("<Tab>", lambda e: "break")

        self.set_date(initial if initial is not None else datetime.today().date())

    # ---------- валидация ----------

    def _validate_char(self, proposed, char):
        """Разрешаем только цифры (или пустую строку для удаления)."""
        if proposed == "":
            return True
        return proposed.isdigit()

    def _validate_ranges(self, event=None):
        """Полная проверка диапазонов и существования даты (FocusOut)."""
        d = self._safe_int(self.d.get())
        m = self._safe_int(self.m.get())
        y = self._safe_int(self.y.get())

        if d is None and m is None and y is None:
            self._mark_all_ok()
            return

        day_ok = d is not None and 1 <= d <= 31
        month_ok = m is not None and 1 <= m <= 12
        year_ok = y is not None and self.MIN_YEAR <= y <= self.MAX_YEAR

        date_ok = False
        if day_ok and month_ok and year_ok:
            try:
                datetime(y, m, d)
                date_ok = True
            except ValueError:
                date_ok = False

        self._mark(self.d, day_ok or (d is None))
        self._mark(self.m, month_ok or (m is None))
        self._mark(self.y, year_ok or (y is None))

        if day_ok and month_ok and year_ok and not date_ok:
            self._mark(self.d, False)
            self._mark(self.m, False)

    def _mark(self, entry, ok):
        entry.configure(style=self.NORMAL_STYLE if ok else self.ERROR_STYLE)

    def _mark_all_ok(self):
        for w in (self.d, self.m, self.y):
            w.configure(style=self.NORMAL_STYLE)

    @staticmethod
    def _safe_int(s):
        try:
            return int(s)
        except (ValueError, TypeError):
            return None

    # ---------- обработчики событий ----------

    def _tab_next(self, nxt):
        def handler(event):
            nxt.focus_set()
            nxt.select_range(0, tk.END)
            return "break"
        return handler

    def _on_key(self, event):
        """
        - Backspace — обычное поведение внутри поля;
        - автопереход: 2 цифры в дне/месяце → к следующему полю;
        - мгновенная подсветка грубых ошибок.
        """
        w = event.widget

        if event.keysym == "BackSpace":
            return

        if event.keysym in ("Left", "Right", "Up", "Down", "Tab",
                            "Delete", "Home", "End",
                            "Shift_L", "Shift_R",
                            "Control_L", "Control_R", "Alt_L", "Alt_R"):
            return

        max_len = 2 if w in (self.d, self.m) else 4

        if len(w.get()) > max_len:
            w.delete(0, tk.END)
            if event.char.isdigit():
                w.insert(0, event.char)

        if w is self.d and len(w.get()) == 2:
            self.m.focus_set()
            self.m.select_range(0, tk.END)
        elif w is self.m and len(w.get()) == 2:
            self.y.focus_set()
            self.y.select_range(0, tk.END)

        self._highlight_obvious_errors(w)

    def _highlight_obvious_errors(self, w):
        """Мгновенная подсветка грубых выходов за диапазон."""
        val = self._safe_int(w.get())

        if w is self.d:
            if val is not None and val > 31:
                self._mark(w, False)
            elif val is not None and 1 <= val <= 31:
                self._mark(w, True)

        elif w is self.m:
            if val is not None and val > 12:
                self._mark(w, False)
            elif val is not None and 1 <= val <= 12:
                self._mark(w, True)

        elif w is self.y:
            if len(w.get()) == 4 and val is not None:
                if self.MIN_YEAR <= val <= self.MAX_YEAR:
                    self._mark(w, True)
                else:
                    self._mark(w, False)

    def _on_paste(self, event):
        """Вставка из буфера: ДД.ММ.ГГГГ, ДД/ММ/ГГГГ, ДДММГГГГ."""
        try:
            data = event.widget.clipboard_get()
        except Exception:
            return

        nums = re.findall(r"\d+", data)

        if len(nums) >= 3:
            try:
                d, m, y = int(nums[0]), int(nums[1]), int(nums[2])
                if y < 100:
                    y += 2000 if y < 50 else 1900
                self.set_date(datetime(y, m, d).date())
                self._mark_all_ok()
            except Exception:
                self._validate_ranges()
        elif len(nums) == 1 and len(nums[0]) == 8:
            s = nums[0]
            try:
                self.set_date(datetime(int(s[4:]), int(s[2:4]), int(s[:2])).date())
                self._mark_all_ok()
            except Exception:
                self._validate_ranges()

    # ---------- публичный интерфейс ----------

    def get_date(self):
        d = self._safe_int(self.d.get())
        m = self._safe_int(self.m.get())
        y = self._safe_int(self.y.get())
        if d is None or m is None or y is None:
            return None
        try:
            return datetime(y, m, d).date()
        except ValueError:
            return None

    def set_date(self, date_obj):
        self.d.delete(0, tk.END)
        self.d.insert(0, f"{date_obj.day:02d}")
        self.m.delete(0, tk.END)
        self.m.insert(0, f"{date_obj.month:02d}")
        self.y.delete(0, tk.END)
        self.y.insert(0, str(date_obj.year))
        self._mark_all_ok()


# ============================================================
# КАЛЕНДАРЬ-ПОПАП
# ============================================================

def open_calendar_popup(date_input: DateInput):
    """
    Открывает модальное окно с tkcalendar.Calendar.
    В високосные года (февраль) 29-е число подсвечивается голубым.
    """
    popup = tk.Toplevel()
    popup.title("Выбор даты")
    popup.geometry("+%d+%d" % (date_input.winfo_rootx(),
                               date_input.winfo_rooty() + 30))
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
        date_pattern="dd.mm.yyyy",
    )
    cal.pack(padx=10, pady=10)


    def on_date_select(event=None):
        """Выбор даты и закрытие попапа — только по кнопке «Выбрать»."""
        try:
            selected = cal.selection_get()
            date_input.set_date(selected)
            popup.destroy()
        except Exception:
            pass

    ttk.Button(popup, text="Выбрать", command=on_date_select).pack(pady=(0, 10))
    popup.bind("<Escape>", lambda e: popup.destroy())
    popup.protocol("WM_DELETE_WINDOW", popup.destroy)

def set_today(date_input: DateInput):
    """Устанавливает в поле текущую дату."""
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
    title = "Койко-дни"
    settings_key = "medical"

    def __init__(self, parent):
        super().__init__(parent)

        # --- Дата поступления ---
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

        # --- Дата выписки ---
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

        # --- Чекбокс «Дневной стационар» ---
        self.is_day_hospital = tk.BooleanVar(value=False)
        self.chk_day = ttk.Checkbutton(
            self,
            text="Дневной стационар",
            variable=self.is_day_hospital,
            command=self._toggle_day_options,
        )
        self.chk_day.grid(row=2, column=0, columnspan=4,
                          padx=15, pady=(10, 0), sticky="w")

        # --- Блок выбора формулы койко-дней ---
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
        self.day_options_frame.grid(row=3, column=0, columnspan=4,
                                    padx=15, pady=(0, 5), sticky="w")
        self.day_options_frame.grid_remove()

        # --- Кнопка и результат ---
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
            messagebox.showerror("Ошибка",
                                 "Введите корректные даты в формате ДД.ММ.ГГГГ")
            return
        if d1 > d2:
            messagebox.showerror("Ошибка",
                                 "Дата поступления не может быть позже даты выписки")
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
            text=f"• Больничный лист: "
                 f"{pluralize(sick_days, ['календарный день', 'календарных дня', 'календарных дней'])}\n"
                 f"• Койко-дни ({type_str}): "
                 f"{pluralize(hospital_days, ['койко-день', 'койко-дня', 'койко-дней'])}"
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
        if d:
            self.date_start.set_date(d)
        d = parse(data.get("end", ""))
        if d:
            self.date_end.set_date(d)

        if "is_day_hospital" in data:
            self.is_day_hospital.set(data["is_day_hospital"])
            self._toggle_day_options()

        if "day_type" in data and data["day_type"] in self.day_type_combo["values"]:
            self.day_type_var.set(data["day_type"])


# ============================================================
# ВКЛАДКА: Возраст
# ============================================================

class AgeTab(TabBase):
    title = "Возраст"
    settings_key = "age"

    def __init__(self, parent):
        super().__init__(parent)

        # --- Дата рождения ---
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

        # --- Целевая дата ---
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

        # --- Кнопка и результат ---
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
            messagebox.showerror("Ошибка",
                                 "Введите корректные даты в формате ДД.ММ.ГГГГ")
            return
        if d1 > d2:
            messagebox.showerror("Ошибка",
                                 "Дата рождения не может быть позже целевой даты")
            return

        try:
            diff = relativedelta(d2, d1)
        except (ValueError, OverflowError) as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось рассчитать возраст: {e}")
            return

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
        if d:
            self.date_birth.set_date(d)
        d = parse(data.get("target", ""))
        if d:
            self.date_target.set_date(d)


# ============================================================
# ВКЛАДКА: Аналитика (прямой + обратный расчёт)
# ============================================================

class PeriodTab(TabBase):
    title = "Аналитика"
    settings_key = "period"

    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Прямой расчёт (интервал между датами)",
                  font=("", 10, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(10, 5))

        # --- Начало периода ---
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

        # --- Конец периода ---
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

        # --- Кнопка и результат ---
        ttk.Button(self, text="Рассчитать период",
                   command=self.calculate).grid(
            row=3, column=0, columnspan=4, pady=10, sticky="w", padx=15)

        self.lbl_res = ttk.Label(self, text="", justify="left")
        self.lbl_res.grid(row=4, column=0, columnspan=4, padx=15, sticky="w")
        make_copyable(self.lbl_res)
        ttk.Label(self, text="(клик по результату — копировать)",
                  foreground="gray").grid(
            row=5, column=0, columnspan=4, padx=15, sticky="w")

        # ---------- Обратный расчёт: дни → годы/месяцы/дни ----------
        ttk.Separator(self, orient="horizontal").grid(
            row=6, column=0, columnspan=4, sticky="ew", padx=15, pady=(15, 5))

        ttk.Label(self, text="Обратный расчёт (дни → годы/месяцы/дни)",
                  font=("", 10, "bold")).grid(
            row=7, column=0, columnspan=4, sticky="w", padx=15, pady=(5, 5))

        ttk.Label(self, text="Количество дней:").grid(
            row=8, column=0, sticky="w", padx=15, pady=5)
        self.ent_total_days = ttk.Entry(self, width=12)
        self.ent_total_days.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        self.ent_total_days.insert(0, "1000")

        ttk.Button(self, text="Перевести дни",
                   command=self.calculate_reverse).grid(
            row=9, column=0, columnspan=4, pady=10, sticky="w", padx=15)

        self.lbl_res_reverse = ttk.Label(self, text="", justify="left")
        self.lbl_res_reverse.grid(
            row=10, column=0, columnspan=4, padx=15, sticky="w")
        make_copyable(self.lbl_res_reverse)

        ttk.Label(self, text="(клик по результату — копировать)",
                  foreground="gray").grid(
            row=11, column=0, columnspan=4, padx=15, sticky="w")

        ttk.Label(self, text="Возможна погрешность ±1 день.",
                  foreground="gray").grid(
            row=12, column=0, columnspan=4, padx=15, pady=(0, 15), sticky="w")

    def calculate(self):
        """Прямой расчёт: период между двумя датами."""
        d1 = self.date_start.get_date()
        d2 = self.date_end.get_date()

        if not d1 or not d2:
            messagebox.showerror("Ошибка",
                                 "Введите корректные даты в формате ДД.ММ.ГГГГ")
            return
        if d1 > d2:
            messagebox.showerror("Ошибка",
                                 "Дата начала не может быть позже даты окончания")
            return

        try:
            diff = relativedelta(d2, d1)
        except (ValueError, OverflowError) as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось рассчитать период: {e}")
            return

        total_months = diff.years * 12 + diff.months
        total_days = (d2 - d1).days

        self.lbl_res.config(
            text=f"• Перевод: {pluralize(diff.years, ['год', 'года', 'лет'])}, "
                 f"{pluralize(diff.months, ['месяц', 'месяца', 'месяцев'])}, "
                 f"{pluralize(diff.days, ['день', 'дня', 'дней'])}\n"
                 f"• Полных месяцев: {total_months}\n"
                 f"• Всего дней в периоде: {total_days}"
        )

    def calculate_reverse(self):
        """
        Обратный расчёт: N дней → годы/месяцы/дни.
        Опорная дата (01.01.1900) зашита в константу DAYS_BASE_DATE.
        Пользователю не показывается.
        """
        val = self.ent_total_days.get().strip()
        if not val or not val.isdigit():
            messagebox.showerror("Ошибка",
                                 "Введите целое число дней (только цифры)")
            return

        total_days = int(val)

        try:
            target = DAYS_BASE_DATE + timedelta(days=total_days)
            diff = relativedelta(target, DAYS_BASE_DATE)
        except (ValueError, OverflowError) as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось выполнить расчёт: {e}")
            return

        self.lbl_res_reverse.config(
            text=f"• {total_days} дней — это:\n"
                 f"  {pluralize(diff.years, ['год', 'года', 'лет'])}, "
                 f"{pluralize(diff.months, ['месяц', 'месяца', 'месяцев'])}, "
                 f"{pluralize(diff.days, ['день', 'дня', 'дней'])}"
        )

    def get_settings(self):
        d1 = self.date_start.get_date()
        d2 = self.date_end.get_date()
        return {
            "start": d1.strftime("%d.%m.%Y") if d1 else "",
            "end": d2.strftime("%d.%m.%Y") if d2 else "",
            "total_days": self.ent_total_days.get().strip(),
        }

    def apply_settings(self, data):
        def parse(s):
            try:
                return datetime.strptime(s, "%d.%m.%Y").date()
            except (ValueError, TypeError):
                return None

        d = parse(data.get("start", ""))
        if d:
            self.date_start.set_date(d)
        d = parse(data.get("end", ""))
        if d:
            self.date_end.set_date(d)

        if "total_days" in data and str(data["total_days"]).strip():
            self.ent_total_days.delete(0, tk.END)
            self.ent_total_days.insert(0, str(data["total_days"]).strip())


# ============================================================
# ВКЛАДКА: Високосные года (справочник)
# ============================================================

class LeapYearsTab(TabBase):
    title = "Високосные года"
    settings_key = "leap_years"

    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Справочник високосных годов",
                  font=("", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 5))

        text_about = (
            "Високосный год — год, содержащий 366 дней вместо 365. "
            "Добавочный день — 29 февраля.\n\n"
            "Правило григорианского календаря:\n"
            "• год делится на 4 — високосный;\n"
            "• кроме годов, делящихся на 100;\n"
            "• но годы, делящиеся на 400, снова високосные.\n\n"
            "Пример: 2000 — високосный, 1900 — нет, 2024 — високосный."
        )
        ttk.Label(self, text=text_about, justify="left",
                  wraplength=560).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 10))

        ttk.Label(self, text="Список годов 1900–2100:",
                  font=("", 10, "bold")).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 5))

        text_frame = ttk.Frame(self)
        text_frame.grid(row=3, column=0, columnspan=2,
                        sticky="nsew", padx=15, pady=(0, 15))
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        self.txt = tk.Text(text_frame, wrap="word", height=15, width=60)
        vsb = ttk.Scrollbar(text_frame, orient="vertical",
                            command=self.txt.yview)
        self.txt.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.txt.pack(side="left", fill="both", expand=True)

        # Заполняем список високосных годов 1900–2100 (по 10 в строке).
        leap_years = [y for y in range(1900, 2101) if is_leap(y)]
        lines = []
        for i in range(0, len(leap_years), 10):
            chunk = leap_years[i:i + 10]
            lines.append("  ".join(f"{y}" for y in chunk))
        self.txt.insert("1.0", "\n".join(lines))
        self.txt.configure(state="disabled")


# ============================================================
# ВКЛАДКА: О программе
# ============================================================

class AboutTab(TabBase):
    title = "О программе"
    settings_key = "about"

    def __init__(self, parent):
        super().__init__(parent)

        # --- Скроллируемая обёртка ---
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical",
                                 command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = ttk.Frame(self.canvas)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner,
                                                  anchor="nw")

        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(
                            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        self._wrap_labels = []
        padx_side = 20

        # ---------- Заголовок ----------
        ttk.Label(self.inner, text="О программе",
                  font=("", 11, "bold")).pack(padx=padx_side,
                                              pady=(20, 10), anchor="w")

        header_frame = ttk.Frame(self.inner)
        header_frame.pack(padx=padx_side, pady=(0, 15), fill="x", anchor="w")

        text_title = "Медицинский календарный калькулятор\nВерсия: 3.0 (Open Source)"
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
            "• Обратный расчёт: перевод N дней в годы/месяцы/дни.\n"
            "• Справочник високосных годов.\n"
        )
        self._add_wrapped_label(text_description, padx_side, (0, 0))

        # ---------- Обновления и связь ----------
        text_updates = (
            "ОБНОВЛЕНИЯ И СВЯЗЬ:\n"
            "Актуальная версия программы и обсуждение — на GitHub.\n"
            "Скачать последнюю версию можно там же или напрямую:"
        )
        self._add_wrapped_label(text_updates, padx_side, (10, 5))

        links_frame = ttk.Frame(self.inner)
        links_frame.pack(padx=padx_side, pady=(0, 10), anchor="w")

        self.lbl_github = tk.Label(
            links_frame,
            text="→ Страница проекта и обсуждение (GitHub)",
            font=("", 10, "underline"), fg="blue", cursor="hand2")
        self.lbl_github.pack(anchor="w", pady=1)
        self.lbl_github.bind("<Button-1>",
                             lambda e: webbrowser.open_new(GITHUB_DISCUSSIONS))


        self.lbl_disk_folder = tk.Label(
            links_frame,
            text="→ Все файлы: исходник, README, LICENSE (Яндекс.Диск)",
            font=("", 10, "underline"), fg="blue", cursor="hand2")
        self.lbl_disk_folder.pack(anchor="w", pady=1)
        self.lbl_disk_folder.bind("<Button-1>",
                                  lambda e: webbrowser.open_new(YANDEX_DISK_FOLDER))

        # ---------- Email ----------
        text_email = "Нашли баг, есть идея или предложение? Напишите на почту:"
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
            fg="blue", cursor="hand2")
        self.lbl_donate_link.pack(anchor="w", pady=(0, 5))
        self.lbl_donate_link.bind("<Button-1>", self.open_donation)

        ttk.Label(donate_text_frame,
                  text="Наведите камеру телефона на QR-код\nили кликните по ссылке.",
                  justify="left", foreground="gray").pack(anchor="w")

        # ---------- Примечание: дневной стационар ----------
        text_note = (
            "ПРИМЕЧАНИЕ ПО КОЙКО-ДНЯМ ДНЕВНОГО СТАЦИОНАРА:\n"
            "Стандартное правило учёта в дневном стационаре — день поступления "
            "и день выписки считаются каждый за 1 день (формула +2). Однако "
            "в отдельных учреждениях действуют внутренние правила (формула +1). "
            "В спорных случаях ориентируйтесь на локальные нормативные документы."
        )
        self._add_wrapped_label(text_note, padx_side, (5, 10))

        # ---------- Примечание: обратный расчёт ----------
        text_note_reverse = (
            "О ПРИБЛИЗИТЕЛЬНОСТИ ОБРАТНОГО РАСЧЁТА:\n"
            "Перевод «N дней → годы/месяцы/дни» зависит от опорной даты: "
            "годы бывают 365 и 366 дней, месяцы — 28, 29, 30 и 31. "
            "Программа использует календарный расчёт с учётом високосных "
            "годов и разной длины месяцев, но результат может отличаться "
            "на ±1 день при сравнении с другими калькуляторами."
        )
        self._add_wrapped_label(text_note_reverse, padx_side, (5, 10))

        # ---------- Примечание: календарь ----------
        text_note_leap = (
            "О ПОДСВЕТКЕ В КАЛЕНДАРЕ:\n"
            "Полный список високосных годов 1900–2100 — во вкладке "
            "«Високосные года»."
        )
        self._add_wrapped_label(text_note_leap, padx_side, (5, 10))

        # ---------- Дисклеймер ----------
        text_bottom = (
            "ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ:\n"
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
        self.winfo_toplevel().update()
        messagebox.showinfo("Успешно", "Email скопирован в буфер обмена!")

    def apply_theme(self, style):
        bg = style.lookup("TFrame", "background") or self.cget("bg")
        for attr in ("lbl_title", "lbl_email", "lbl_donate_link",
                     "lbl_qr", "lbl_github", "lbl_disk_folder"):
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
        self.geometry("700x560")
        self.minsize(380, 300)

        self.style = ttk.Style()
        self._native_theme_name = self.style.theme_use()

        available = set(self.style.theme_names())
        self.available_themes = {
            name: sys_name
            for name, sys_name in NATIVE_THEMES.items()
            if sys_name in available
        }

        if not self.available_themes:
            self.available_themes = {"Системная": self._native_theme_name}

        # ---------- Верхняя панель (2 строки) ----------
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill="x", padx=15, pady=5)

        # --- Строка 1: тема и размер шрифта ---
        self.top_row1 = ttk.Frame(self.top_frame)
        self.top_row1.pack(fill="x", anchor="w")

        ttk.Label(self.top_row1, text="Тема:").pack(side="left", padx=(0, 5))

        default_theme = (DEFAULT_THEME_NAME
                         if DEFAULT_THEME_NAME in self.available_themes
                         else list(self.available_themes.keys())[0])
        self.theme_var = tk.StringVar(value=default_theme)

        self.theme_combo = ttk.Combobox(
            self.top_row1,
            textvariable=self.theme_var,
            values=list(self.available_themes.keys()),
            state="readonly",
            width=28,
        )
        self.theme_combo.pack(side="left", padx=(0, 15))
        self.theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        ttk.Label(self.top_row1, text="Размер шрифта:").pack(side="left",
                                                              padx=(0, 5))

        self.FONT_PRESETS = {
            "Мелкий (10)": 10,
            "Обычный (12)": 12,
            "Крупный (14)": 14,
            "Очень крупный (16)": 16,
        }
        self.font_var = tk.StringVar(value="Обычный (12)")
        self.font_combo = ttk.Combobox(
            self.top_row1,
            textvariable=self.font_var,
            values=list(self.FONT_PRESETS.keys()),
            state="readonly",
            width=18,
        )
        self.font_combo.pack(side="left")
        self.font_combo.bind("<<ComboboxSelected>>", self.on_font_change)

        # --- Строка 2: галочка «Запоминать размер окна» ---
        self.top_row2 = ttk.Frame(self.top_frame)
        self.top_row2.pack(fill="x", anchor="w", pady=(5, 0))

        self.remember_size_var = tk.BooleanVar(value=False)
        self.chk_remember_size = ttk.Checkbutton(
            self.top_row2,
            text="Запоминать размер окна",
            variable=self.remember_size_var,
            command=self.on_remember_size_toggle,
        )
        self.chk_remember_size.pack(side="left", padx=(0, 10))

        # ---------- Notebook ----------
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.tabs = []
        self._register_default_tabs()

        self.load_settings()
        self.apply_current_theme()
        self.apply_font_size(self.FONT_PRESETS.get(self.font_var.get(), 10))
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _register_default_tabs(self):
        prefixes = {
            "medical":    "🏥 " if _supports_emoji() else "",
            "age":        "👶 " if _supports_emoji() else "",
            "period":     "📅 " if _supports_emoji() else "",
            "leap_years": "📆 " if _supports_emoji() else "",
            "about":      "ℹ "  if _supports_emoji() else "",
        }
        for cls in (MedicalTab, AgeTab, PeriodTab, LeapYearsTab, AboutTab):
            tab = cls(self.notebook)
            self.tabs.append(tab)
            self.notebook.add(tab, text=prefixes[tab.settings_key] + tab.title)

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
        for tab in self.tabs:
            try:
                tab.apply_theme(self.style)
            except Exception:
                pass

    # ---------- Шрифт ----------

    def on_font_change(self, event=None):
        size = self.FONT_PRESETS.get(self.font_var.get(), 10)
        self.apply_font_size(size)

    def on_remember_size_toggle(self):
        try:
            self.save_settings()
        except Exception:
            pass

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
        if self.remember_size_var.get():
            data["window_geometry"] = self.geometry()

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

        saved_theme = data.get("theme")
        if saved_theme in THEME_RENAMES:
            saved_theme = THEME_RENAMES[saved_theme]
        if saved_theme in self.available_themes:
            self.theme_var.set(saved_theme)

        if data.get("font_preset") in self.FONT_PRESETS:
            self.font_var.set(data["font_preset"])

        geom = data.get("window_geometry")
        if isinstance(geom, str) and "x" in geom:
            try:
                self.geometry(geom)
            except Exception:
                pass

        if "remember_size" in data:
            self.remember_size_var.set(bool(data["remember_size"]))

        for tab in self.tabs:
            if tab.settings_key in data and isinstance(data[tab.settings_key], dict):
                try:
                    tab.apply_settings(data[tab.settings_key])
                except Exception as e:
                    print(f"Не удалось загрузить настройки вкладки "
                          f"{tab.settings_key}: {e}")

    def on_close(self):
        self.save_settings()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()