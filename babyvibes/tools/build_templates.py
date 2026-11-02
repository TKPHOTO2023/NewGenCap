#!/usr/bin/env python3
"""Build the BabyVibes Elementor templates.

Writes one Elementor template file per page into the plugin (plugin/babyvibes-store-kit/templates/)
and packs the plugin into dist/babyvibes-store-kit.zip, the file you upload to WordPress.

The WhatsApp number and email below are placeholders: the plugin's setup screen swaps in the real
ones. After changing the design here, run:

    python3 tools/build_templates.py
"""
import hashlib
import json
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent / "plugin" / "babyvibes-store-kit"
OUT = PLUGIN / "templates"
ZIP = HERE.parent / "dist" / "babyvibes-store-kit.zip"

SHOP = {
    "name": "BabyVibes",
    "sku": "BV-TC-001",
    "whatsapp": "27000000000",  # placeholder, replaced by the setup screen
    "email": "hello@babyvibes.co.za",  # placeholder, replaced by the setup screen
    "hours": "Monday to Friday, 08:00 to 17:00",
}

# Brand palette (same values as the plugin's CSS and the README).
INK = "#2E2A3B"
GREEN = "#2F7A4D"  # buttons and links: white text on it passes WCAG AA
GREEN_SOFT = "#E8F6EC"
CORAL = "#FF7F6E"
PEACH = "#FFF1EA"
CREAM = "#FFF8F0"
SUN = "#FFD166"
WHITE = "#FFFFFF"

HEAD_FONT = "Fredoka"
BODY_FONT = "Nunito"

_counter = 0


def _id():
    """Stable 7-character hex ids, so a rebuild without changes produces the same files."""
    global _counter
    _counter += 1
    return hashlib.md5(f"bv{_counter}".encode()).hexdigest()[:7]


def px(size):
    return {"unit": "px", "size": size, "sizes": []}


def box(top, right=None, bottom=None, left=None, unit="px"):
    right = top if right is None else right
    bottom = top if bottom is None else bottom
    left = right if left is None else left
    linked = top == right == bottom == left
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom),
            "left": str(left), "isLinked": linked}


def font(prefix, family, size, weight, mobile=None, line_height=None):
    s = {
        f"{prefix}_typography": "custom",
        f"{prefix}_font_family": family,
        f"{prefix}_font_size": px(size),
        f"{prefix}_font_weight": str(weight),
    }
    if mobile:
        s[f"{prefix}_font_size_mobile"] = px(mobile)
    if line_height:
        s[f"{prefix}_line_height"] = {"unit": "em", "size": line_height, "sizes": []}
    return s


# Widgets ---------------------------------------------------------------------------------

def widget(kind, settings):
    return {"id": _id(), "elType": "widget", "widgetType": kind, "settings": settings,
            "elements": [], "isInner": False}


def heading(text, tag="h2", size=40, mobile=30, color=INK, align="center"):
    return widget("heading", {
        "title": text, "header_size": tag, "align": align, "title_color": color,
        **font("typography", HEAD_FONT, size, 600, mobile, 1.15),
    })


def kicker(text, color=CORAL, align="center"):
    return widget("heading", {
        "title": text.upper(), "header_size": "p", "align": align, "title_color": color,
        **font("typography", BODY_FONT, 14, 800),
        "typography_letter_spacing": px(2),
        "_margin": box(0, 0, 8, 0),
    })


def text(html, align="center", color=INK, size=18):
    return widget("text-editor", {
        "editor": html, "align": align, "text_color": color,
        **font("typography", BODY_FONT, size, 400, None, 1.6),
    })


def button(label, url, primary=True, align="center", size="lg", external=False):
    return widget("button", {
        "text": label,
        "link": {"url": url, "is_external": "on" if external else "", "nofollow": "",
                 "custom_attributes": ""},
        "align": align, "align_mobile": "justify", "size": size,
        "background_color": GREEN if primary else WHITE,
        "button_text_color": WHITE if primary else GREEN,
        "button_background_hover_color": "#25613D" if primary else GREEN_SOFT,
        "hover_color": WHITE if primary else GREEN,
        "border_border": "solid", "border_width": box(2),
        "border_color": GREEN,
        "border_radius": box(999),
        "text_padding": box(16, 34),
        **font("typography", BODY_FONT, 17, 800),
    })


def icon_box(icon, title, desc, color=GREEN):
    return widget("icon-box", {
        "selected_icon": {"value": f"fas fa-{icon}", "library": "fa-solid"},
        "view": "stacked", "shape": "circle",
        "title_text": title, "description_text": desc,
        "position": "top", "text_align": "center", "title_size": "h3",
        "primary_color": color, "secondary_color": WHITE,
        "icon_size": px(26), "icon_padding": {"unit": "em", "size": 0.75, "sizes": []},
        "icon_space": px(14),
        "title_color": INK, "description_color": INK,
        **font("title_typography", HEAD_FONT, 21, 600),
        **font("description_typography", BODY_FONT, 16, 400, None, 1.55),
    })


def icon_list(items, color=GREEN, align="left"):
    return widget("icon-list", {
        "icon_list": [{"_id": _id(), "text": t,
                       "selected_icon": {"value": "fas fa-check-circle", "library": "fa-solid"}}
                      for t in items],
        "icon_color": color, "icon_size": px(20), "text_color": INK,
        "space_between": px(12), "icon_align": align,
        **font("icon_typography", BODY_FONT, 18, 600),
    })


def accordion(items):
    return widget("accordion", {
        "tabs": [{"_id": _id(), "tab_title": q, "tab_content": a} for q, a in items],
        "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
        "title_html_tag": "h3",
        "border_color": "#F1DED3", "title_background": WHITE,
        "title_color": INK, "tab_active_color": GREEN, "icon_color": CORAL,
        "icon_active_color": GREEN, "content_background_color": WHITE, "content_color": INK,
        **font("title_typography", HEAD_FONT, 19, 600),
        **font("content_typography", BODY_FONT, 16, 400, None, 1.6),
    })


def shortcode(code):
    return widget("shortcode", {"shortcode": code})


def html(code):
    return widget("html", {"html": code})


def spacer(height):
    return widget("spacer", {"space": px(height)})


# Layout ----------------------------------------------------------------------------------

def column(size, *widgets, align=None, pad=None, bg=None, radius=None):
    s = {"_column_size": size, "_inline_size": None}
    if align:
        s["content_position"] = align
    if pad is not None:
        s["padding"] = pad
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if radius:
        s["border_radius"] = box(radius)
    return {"id": _id(), "elType": "column", "settings": s, "elements": list(widgets),
            "isInner": False}


STRUCTURE = {1: "10", 2: "20", 3: "30", 4: "40"}


def section(columns, bg=CREAM, pad=(90, 20), pad_mobile=(56, 16), anchor=None, width=1140,
            gap="wider", middle=False):
    s = {
        "layout": "boxed",
        "content_width": px(width),
        "gap": gap,
        "structure": STRUCTURE[len(columns)],
        "background_background": "classic",
        "background_color": bg,
        "padding": box(pad[0], pad[1], pad[0], pad[1]),
        "padding_mobile": box(pad_mobile[0], pad_mobile[1], pad_mobile[0], pad_mobile[1]),
    }
    if middle:
        s["content_position"] = "middle"
    if anchor:
        s["_element_id"] = anchor
    return {"id": _id(), "elType": "section", "settings": s, "elements": columns,
            "isInner": False}


def one(*widgets, **kw):
    return section([column(100, *widgets)], **kw)


def template(title, content):
    return {
        "version": "0.4",
        "title": title,
        "type": "page",
        "page_settings": {"hide_title": "yes"},
        "content": content,
    }


# Pages -----------------------------------------------------------------------------------

SKU = SHOP["sku"]
WA = f"https://wa.me/{SHOP['whatsapp']}"
CACTUS_SVG = (HERE / "cactus.svg").read_text().strip()

FAQ = [
    ("What age is the Talking Cactus for?",
     "<p>Check the age rating on the box of your Talking Cactus before giving it to your little one. "
     "It is a soft toy with a battery inside, so play should always be supervised, and it is not a sleep toy "
     "to leave in a cot.</p>"),
    ("How does it charge?",
     "<p>It charges with the USB cable in the box. Plug it into a phone charger or a laptop, and a full charge "
     "gives hours of play.</p>"),
    ("Can I turn the volume down?",
     "<p>Yes. The switch underneath the pot has a quieter setting for naps and car trips, and an off setting "
     "for when you need some peace.</p>"),
    ("How long does delivery take?",
     "<p>We deliver across South Africa. Orders placed before 12:00 on a weekday are packed the same day, "
     "and most arrive within 2 to 4 working days in the main centres. You'll get a tracking number by email.</p>"),
    ("How do I pay?",
     "<p>Pay securely at checkout by card, Instant EFT or the other options shown there. We never see or "
     "store your card details.</p>"),
    ("What if something is wrong with my order?",
     "<p>Message us on WhatsApp or email within 7 days of delivery and we'll sort it out with a replacement "
     "or a refund. See our <a href='/faq-delivery/'>Delivery &amp; Returns</a> page for the details.</p>"),
]


def home():
    hero = section([
        column(55,
               kicker("New at BabyVibes", align="left"),
               heading("Meet the Talking Cactus, the little friend who talks back",
                       tag="h1", size=54, mobile=36, align="left"),
               text("<p>Say something and the Talking Cactus says it right back in a giggly voice, then wiggles, "
                    "dances and lights up. It's the toy that keeps the giggles going.</p>",
                    align="left", size=19),
               spacer(8),
               shortcode(f'[add_to_cart sku="{SKU}" show_price="true" style=""]'),
               icon_list(["Delivery across South Africa",
                          "Secure checkout",
                          "USB rechargeable, so no batteries to buy"]),
               align="middle"),
        column(45, html(CACTUS_SVG), align="middle"),
    ], bg=PEACH, pad=(80, 20), middle=True)

    features = one(
        kicker("What it does"),
        heading("Talks, dances, sings and glows"),
        text("<p>Everything little ones love, in one cheeky cactus.</p>"),
        spacer(20),
        bg=CREAM)
    features["settings"]["padding"] = box(90, 20, 0, 20)
    features["settings"]["padding_mobile"] = box(56, 16, 0, 16)
    feature_row = section([
        column(25, icon_box("microphone", "Repeats what you say",
                            "Talk, sing or giggle and it copies you in a funny voice.")),
        column(25, icon_box("music", "Sings and dances",
                            "A playlist of catchy songs with a wiggle to match.", color=CORAL)),
        column(25, icon_box("lightbulb", "Lights up",
                            "Soft, colourful lights that catch little eyes.")),
        column(25, icon_box("battery-full", "USB rechargeable",
                            "Charge it like your phone. No batteries to buy.", color=CORAL)),
    ], bg=CREAM, pad=(0, 20), pad_mobile=(0, 16))
    # Close the features block with some room under the row of boxes.
    feature_row["settings"]["padding"] = box(0, 20, 90, 20)
    feature_row["settings"]["padding_mobile"] = box(0, 16, 56, 16)

    why = section([
        column(50, html(CACTUS_SVG), align="middle"),
        column(50,
               kicker("Why moms love it", align="left"),
               heading("More giggles, more chatting, more play", align="left"),
               text("<p>Little ones love hearing their own voice played back. The Talking Cactus turns "
                    "babbling into a game and keeps them busy for longer than most toys.</p>",
                    align="left"),
               icon_list(["Encourages babbling and first words",
                          "Makes tummy time more fun",
                          "A great distraction for car trips and nappy changes",
                          "A gift that gets a reaction at baby showers and birthdays"]),
               align="middle"),
    ], bg=GREEN_SOFT, middle=True)

    steps = section([
        column(33, icon_box("plug", "1. Charge it", "Plug in the USB cable until the light shows it's full.")),
        column(33, icon_box("toggle-on", "2. Switch it on",
                            "Pick talk mode or music mode with the switch under the pot.", color=CORAL)),
        column(33, icon_box("comments", "3. Talk and play",
                            "Say hello and watch it answer back with a dance.")),
    ], bg=CREAM, pad=(0, 20), pad_mobile=(0, 16))
    steps["settings"]["padding"] = box(0, 20, 90, 20)
    steps["settings"]["padding_mobile"] = box(0, 16, 56, 16)
    steps_head = one(kicker("How it works"), heading("Ready to play in three steps"), spacer(10),
                     bg=CREAM)
    steps_head["settings"]["padding"] = box(90, 20, 0, 20)
    steps_head["settings"]["padding_mobile"] = box(56, 16, 0, 16)

    buy = one(
        kicker("Get yours"),
        heading("Bring home the Talking Cactus"),
        text("<p>Add it to your cart and check out in under a minute.</p>"),
        spacer(10),
        shortcode(f'[product_page sku="{SKU}"]'),
        bg=WHITE, anchor="buy")

    faq = section([
        column(100,
               kicker("Questions"),
               heading("Good to know"),
               spacer(10),
               accordion(FAQ)),
    ], bg=PEACH, width=820)

    final = one(
        heading("Ready for the giggles?", size=42, color=WHITE),
        text("<p>Questions before you order? We're a WhatsApp away.</p>", color=WHITE),
        spacer(6),
        button("Buy the Talking Cactus", "#buy", primary=False),
        spacer(6),
        button("Chat on WhatsApp", WA, primary=False, size="md", external=True),
        bg=GREEN, pad=(80, 20))

    return template("BabyVibes: Home",
                    [hero, features, feature_row, why, steps_head, steps, buy, faq, final])


def about():
    intro = one(
        kicker("Our story"),
        heading("Made by moms, for moms", tag="h1", size=50, mobile=34),
        text("<p>BabyVibes started with a simple idea: the best baby toys are the ones that make "
             "you laugh too. We pick fun, good-value toys, test them at home with our own little ones, "
             "and deliver them across South Africa.</p>"),
        bg=PEACH, width=820)

    values = section([
        column(33, icon_box("heart", "Picked with care",
                            "We only stock toys we'd happily give our own kids.")),
        column(33, icon_box("truck", "Delivered to your door",
                            "Fast, tracked delivery across South Africa.", color=CORAL)),
        column(33, icon_box("smile", "Real people, real help",
                            "Message us any time and a real mom will answer.")),
    ], bg=CREAM)

    cta = one(
        heading("Say hello to the Talking Cactus"),
        text("<p>Our first toy, and already a favourite.</p>"),
        button("Shop now", "/#buy"),
        bg=GREEN_SOFT, width=820)
    return template("BabyVibes: About", [intro, values, cta])


def contact():
    intro = one(
        kicker("Contact us"),
        heading("We'd love to hear from you", tag="h1", size=50, mobile=34),
        text("<p>Questions about an order, delivery or the Talking Cactus? The quickest way to reach us is "
             "WhatsApp.</p>"),
        bg=PEACH, width=820)

    ways = section([
        column(50,
               icon_box("comment-dots", "WhatsApp", "Fastest replies during office hours."),
               button("Chat on WhatsApp", WA, external=True),
               bg=WHITE, radius=24, pad=box(32)),
        column(50,
               icon_box("envelope", "Email", f"{SHOP['email']}", color=CORAL),
               button("Send us an email", f"mailto:{SHOP['email']}", primary=False),
               bg=WHITE, radius=24, pad=box(32)),
    ], bg=CREAM)

    hours = one(
        heading("Office hours", size=28),
        text(f"<p>{SHOP['hours']}. Messages sent after hours are answered the next working day.</p>"),
        bg=CREAM, pad=(0, 20), pad_mobile=(0, 16))
    hours["settings"]["padding"] = box(0, 20, 90, 20)
    hours["settings"]["padding_mobile"] = box(0, 16, 56, 16)
    return template("BabyVibes: Contact", [intro, ways, hours])


def faq_page():
    intro = one(
        kicker("Help"),
        heading("FAQ, delivery and returns", tag="h1", size=50, mobile=34),
        bg=PEACH, width=820, pad=(80, 20))

    delivery = [
        ("Where do you deliver?", "<p>Anywhere in South Africa.</p>"),
        ("How much does delivery cost?",
         "<p>The delivery fee is shown at checkout before you pay. Look out for free-delivery offers.</p>"),
        ("How long will it take?",
         "<p>Orders placed before 12:00 on a weekday are packed the same day. Most orders arrive within "
         "2 to 4 working days in the main centres, and a little longer in outlying areas.</p>"),
        ("Can I track my parcel?", "<p>Yes. We email your tracking number as soon as your order ships.</p>"),
    ]
    returns = [
        ("My toy arrived damaged or doesn't work",
         "<p>We're sorry! Contact us within 7 days of delivery with your order number and a photo or video, "
         "and we'll send a replacement or refund you in full, including delivery.</p>"),
        ("Can I return a toy I don't want?",
         "<p>Yes, within 7 days of delivery, if it's unused and in its original packaging. Contact us first "
         "and we'll explain how to send it back. Once we receive it, we refund the price of the toy.</p>"),
        ("How long do refunds take?",
         "<p>We process refunds within 5 working days of receiving the return. Your bank may take a few "
         "more days to show the money.</p>"),
    ]
    body = section([
        column(100,
               heading("Your questions", size=30, align="left"), accordion(FAQ), spacer(30),
               heading("Delivery", size=30, align="left"), accordion(delivery), spacer(30),
               heading("Returns and refunds", size=30, align="left"), accordion(returns)),
    ], bg=CREAM, width=820)

    help_cta = one(
        heading("Still need help?", size=30),
        button("Chat on WhatsApp", WA, external=True),
        bg=GREEN_SOFT, width=820, pad=(70, 20))
    return template("BabyVibes: FAQ and Delivery", [intro, body, help_cta])


def main():
    OUT.mkdir(exist_ok=True)
    for name, build in [("home", home), ("about", about), ("contact", contact),
                        ("faq-delivery", faq_page)]:
        path = OUT / f"babyvibes-{name}.json"
        path.write_text(json.dumps(build(), indent=1, ensure_ascii=False) + "\n")
        print("wrote", path.relative_to(HERE.parent))

    ZIP.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(PLUGIN.rglob("*")):
            if f.is_file():
                info = zipfile.ZipInfo(str(f.relative_to(PLUGIN.parent)), date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, f.read_bytes())
    print("wrote", ZIP.relative_to(HERE.parent))


if __name__ == "__main__":
    main()
